import schedule
from job_scheduler import JobScheduler
from messaging_helpers.submit_notification import submit_notification
import time

def otp_send_job(data):
    print(f"[OTP_JOB] Payload => {data}")
    time.sleep(3)
    result = JobScheduler.cancelJob(data["job_id"])
    submit_notification({"notification_type": "job_terminated","data":result})
    return schedule.CancelJob