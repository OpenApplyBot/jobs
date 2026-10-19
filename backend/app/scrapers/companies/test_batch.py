"""Run generated company scrapers in bounded batches and write real outcomes to JSONL.

Run from backend:
  python -m app.scrapers.companies.test_batch --offset 0 --limit 50
Continue with offsets 50, 100, ... 450. This does not create mock jobs or write to the DB.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import importlib
import json
import multiprocessing
from queue import Empty
from pathlib import Path
from time import monotonic
import os
import tempfile

MANIFEST = json.loads(
    (Path(__file__).resolve().parents[1] / "manifest.json").read_text(encoding="utf-8")
)


def _scrape_in_worker(module_name, result_queue):
    """Run a scraper and send only a small status message through the IPC queue.

    Job lists can be large enough to fill multiprocessing.Queue's pipe and block
    the child while it serializes the payload. Persist the result to a temporary
    JSON file instead; the queue carries only the file path.
    """
    result_path = None
    try:
        module = importlib.import_module(".." + module_name, package=__package__)
        jobs = module.scrape()
        fd, result_path = tempfile.mkstemp(prefix="openapplybot-scrape-", suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(jobs, stream, ensure_ascii=False, default=str)
        result_queue.put(("ok_file", result_path))
    except Exception as exc:
        if result_path:
            try:
                os.unlink(result_path)
            except OSError:
                pass
        result_queue.put(("error", type(exc).__name__, str(exc)))


def _run_scraper(module_name, timeout):
    result_queue = multiprocessing.Queue()
    process = multiprocessing.Process(target=_scrape_in_worker, args=(module_name, result_queue))
    process.start()
    result_path = None

    try:
        try:
            result = result_queue.get(timeout=max(1, timeout))
        except Empty as exc:
            process.join(timeout=0.2)
            if process.is_alive():
                process.terminate()
                process.join(2)
                raise TimeoutError(f"scraper exceeded {timeout}s execution timeout") from exc
            raise RuntimeError(
                f"scraper worker exited with code {process.exitcode} without a result"
            ) from exc

        process.join(timeout=2)
        if process.is_alive():
            process.terminate()
            process.join(2)

        if result[0] == "error":
            raise RuntimeError(f"{result[1]}: {result[2]}")
        if result[0] != "ok_file":
            raise RuntimeError(f"Unexpected scraper worker result: {result[0]!r}")

        result_path = result[1]
        with open(result_path, "r", encoding="utf-8") as stream:
            return json.load(stream)
    finally:
        if result_path:
            try:
                os.unlink(result_path)
            except OSError:
                pass
        result_queue.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--report", default="company_scraper_test_report.jsonl")
    parser.add_argument("--timeout", type=int, default=30, help="Maximum seconds per scraper")
    parser.add_argument("--workers", type=int, default=8, help="Concurrent scraper processes")
    parser.add_argument("--resume", action="store_true", help="Skip companies already passing with at least one valid job in the report")
    parser.add_argument("--retries", type=int, default=1, help="Retries for errors/timeouts (0 disables retries)")
    args = parser.parse_args()
    start = max(0, args.offset)
    selected = [item for item in MANIFEST[start:start + max(0, args.limit)]]
    if args.resume:
        previous_successes = set()
        previous_report = Path(args.report)
        if previous_report.exists():
            for line in previous_report.read_text(encoding="utf-8").splitlines():
                try:
                    previous = json.loads(line)
                    if previous.get("status") == "success" and int(previous.get("jobs", 0)) > 0:
                        previous_successes.add(previous.get("company"))
                except (ValueError, TypeError):
                    continue
        selected = [item for item in selected if item.get("company_name") not in previous_successes]
    if not selected:
        if args.resume:
            print(json.dumps({"offset": start, "limit": 0, "skipped": "all selected companies already passed", "report": str(Path(args.report).resolve())}, indent=2))
            return
        raise SystemExit("No companies selected; generate modules from the 500-row CSV first.")

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    counts = {"with_jobs": 0, "empty": 0, "invalid": 0, "errors": 0}

    def run_one(index_item):
        i, item = index_item
        t0 = monotonic()
        result = {
            "rank": item["rank"],
            "company": item["company_name"],
            "url": item["official_careers_url"],
            "status": "error",
            "jobs": 0,
        }
        try:
            last_error = None
            jobs = None
            for attempt in range(max(0, args.retries) + 1):
                try:
                    jobs = _run_scraper(Path(item["module"]).stem, args.timeout)
                    last_error = None
                    break
                except Exception as exc:
                    last_error = exc
                    if attempt < max(0, args.retries):
                        continue
            if last_error is not None:
                raise last_error
            result["jobs"] = len(jobs or [])
            seen = set()
            invalid = []
            for index, job in enumerate(jobs or []):
                if not isinstance(job, dict):
                    invalid.append({"index": index, "reason": "row is not an object"})
                    continue
                missing = [field for field in ("source_job_id", "title", "url") if not job.get(field)]
                url = str(job.get("url") or "")
                if missing:
                    invalid.append({"index": index, "reason": f"missing: {', '.join(missing)}"})
                elif not url.startswith(("http://", "https://")):
                    invalid.append({"index": index, "reason": "url is not absolute HTTP(S)"})
                if job.get("source_job_id") in seen:
                    invalid.append({"index": index, "reason": "duplicate source_job_id"})
                seen.add(job.get("source_job_id"))
            result["invalid_jobs"] = len(invalid)
            if invalid:
                result["invalid_examples"] = invalid[:5]
                result["status"] = "invalid"
            else:
                result["status"] = "success" if result["jobs"] else "empty"
        except Exception as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"[:1500]
        result["elapsed_seconds"] = round(monotonic() - t0, 2)
        return i, result

    with report_path.open("a", encoding="utf-8") as report:
        with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
            pending = [executor.submit(run_one, pair) for pair in enumerate(selected, start=1)]
            for future in as_completed(pending):
                i, result = future.result()
                if result["status"] == "success":
                    counts["with_jobs"] += 1
                elif result["status"] == "empty":
                    counts["empty"] += 1
                elif result["status"] == "invalid":
                    counts["invalid"] += 1
                else:
                    counts["errors"] += 1
                report.write(json.dumps(result, ensure_ascii=False, default=str) + "\n")
                report.flush()
                print(f'[{i}/{len(selected)}] {result["company"]}: {result["status"]} jobs={result["jobs"]}')
    print(json.dumps({
        "offset": start,
        "limit": len(selected),
        "resume": args.resume,
        "retries": max(0, args.retries),
        **counts,
        "report": str(report_path.resolve()),
        "note": "Success with zero jobs means the request/parser completed but returned no listings; inspect before classifying the source as working."
    }, indent=2))


if __name__ == "__main__":
    main()
