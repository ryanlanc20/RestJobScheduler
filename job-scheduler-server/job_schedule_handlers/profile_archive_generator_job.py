import schedule

def profile_archive_generator_job(data):
    print(f"[PROFILE_ARCHIVE_GENERATOR_JOB] Payload => {data}")
    return schedule.CancelJob
