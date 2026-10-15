"""Periodic queue scheduler; waits for the first interval so system startup is non-destructive."""
import os
import time
import logging
from .worker import run_all_active

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def main():
    interval = max(900, int(os.getenv("SYNC_INTERVAL_SECONDS", "21600")))
    logger.info("Scheduler ready; first automatic enqueue in %s seconds", interval)
    while True:
        time.sleep(interval)
        try:
            ids = run_all_active()
            logger.info("Scheduled sync queued %d sources", len(ids))
        except Exception:
            logger.exception("Scheduled sync enqueue failed")

if __name__ == "__main__":
    main()
