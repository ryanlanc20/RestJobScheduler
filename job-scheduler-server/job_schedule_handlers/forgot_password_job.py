import schedule
from job_scheduler import JobScheduler
from messaging_helpers.submit_notification import submit_notification
import time

def forgot_password_job(data):
    print(f"[FORGOT_PASSWORD_JOB] Payload => {data}")
    time.sleep(3)
    result = JobScheduler.cancelJob(data["job_id"])
    submit_notification({"notification_type": "job_terminated","data":result})
    return schedule.CancelJob