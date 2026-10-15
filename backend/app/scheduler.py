import os,time,logging
from .worker import run_all_active
logging.basicConfig(level=logging.INFO)
def main():
    interval=max(900,int(os.getenv("SYNC_INTERVAL_SECONDS","21600")))
    while True:
        try: logging.info("Enqueued %d sources",len(run_all_active()))
        except Exception: logging.exception("Scheduled sync enqueue failed")
        time.sleep(interval)
if __name__=="__main__": main()
