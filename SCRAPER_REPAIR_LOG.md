# Scraper repair log

This log records code repairs and verification evidence. A source/ATS URL being verified is **not** the same as the Python scraper passing a live run. Do not mark a scraper PASS until the live audit confirms valid job titles and HTTP(S) application URLs.

## Batch 1 — verified ATS board routing / official URL correction

| Manifest rank | Company | Change | Source evidence | Code status | Live scraper test |
|---:|---|---|---|---|---|
| 84 | Figma | Use Greenhouse board token `figma` instead of generic discovery. | https://www.figma.com/careers/ links open roles to https://job-boards.greenhouse.io/figma/ | Updated | Pending self-hosted audit |
| 85 | Canva | Use SmartRecruiters company slug `Canva`; the adapter expects a slug, not a careers URL. | https://careers.smartrecruiters.com/Canva | Updated | Pending self-hosted audit |
| 91 | Asana | Use Greenhouse board token `asana`. | https://boards.greenhouse.io/asana | Updated | Pending self-hosted audit |
| 97 | Grafana Labs | Use Greenhouse board token `grafanalabs`. | https://boards.greenhouse.io/grafanalabs | Updated | Pending self-hosted audit |
| 156 | Publicis Sapient | Replace stale candidate URL with the current official job-search page. Generic discovery still needs a live test and may need a dedicated parser. | https://careers.publicissapient.com/job-search | URL corrected; parser not yet verified | Pending self-hosted audit |
| 257 | Airbnb | Use Greenhouse board token `airbnb`. | https://boards.greenhouse.io/airbnb | Updated | Pending self-hosted audit |
| 258 | Lyft | Use Greenhouse board token `lyft`. | https://boards.greenhouse.io/lyft | Updated | Pending self-hosted audit |
| 420 | Samsara | Use Greenhouse board token `samsara`. | https://boards.greenhouse.io/samsara | Updated | Pending self-hosted audit |
| 491 | Mozilla | Use Greenhouse board token `mozilla`. | https://boards.greenhouse.io/mozilla | Updated | Pending self-hosted audit |

## Test status

- Static Python syntax compilation was run successfully for the Canva, Figma, and Publicis Sapient module source after the first edits.
- The live audit is **not yet complete**: the existing run is stuck in the old `Set up Python` step and checked out a commit from before the updated self-hosted workflow. Do not infer runtime success from the source verification.
- Next step: run the current manual self-hosted audit against the latest `main`, then fix each reported `ERROR`, `EMPTY`, or invalid-row case and rerun the affected scraper.
