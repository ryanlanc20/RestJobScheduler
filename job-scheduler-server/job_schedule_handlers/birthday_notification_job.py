import schedule

def birthday_notification_job(data):
    # Submit job here
    print(f"[BIRTHDAY_NOTIFICATION_JOB] Payload => {data}")
    return schedule.CancelJob
