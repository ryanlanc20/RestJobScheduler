import schedule

def profile_stats_aggregator_job(data):
    print(f"[PROFILE_STATS_AGGREGATOR_JOB] Payload => {data}")
    return schedule.CancelJob
