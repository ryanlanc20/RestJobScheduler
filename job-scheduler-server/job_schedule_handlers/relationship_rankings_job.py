import schedule
import time
from job_scheduler import JobScheduler
from messaging_helpers.submit_notification import submit_notification

def relationship_rankings_job(data):
    # Submit job here
    print(f"[RELATIONSHIP_RANKINGS_JOB] Payload => {data}")
    time.sleep(5)
    return schedule.CancelJob
