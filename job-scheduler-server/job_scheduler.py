import threading
import schedule
import time

class JobScheduler(threading.Thread):
    jobs = {}

    running = threading.Event()

    def run(cls):
        while not JobScheduler.running.is_set():
            schedule.run_pending()
            time.sleep(1)

    def createJobId(type):
        return type + "_" + str(time.time())
    
    def scheduleJob(executionDelay,jobExecuterDelegate,job_id,jobtype):
        job = {"scheduler_obj": schedule.every(executionDelay).seconds.do(jobExecuterDelegate),"startTime": time.time()*1000,"terminateTime": -1,"state":"scheduled","job_type":jobtype}
        JobScheduler.jobs[job_id] = job
        return {"job_id": job_id,"startTime":job["startTime"],"terminatedTime":job["terminateTime"],"state": job["state"],"job_type":jobtype}

    def cancelJob(job_id):
        if not job_id in JobScheduler.jobs:
            return False
        job = JobScheduler.jobs[job_id]
        schedule.cancel_job(job["scheduler_obj"])
        job["terminateTime"] = time.time() * 1000
        job["state"] = "terminated"

        return {"job_id":job_id,"startTime":job["startTime"], "terminateTime": job["terminateTime"],"state":job["state"],"job_type": job["job_type"]}

    def getActiveJobs():
        return {job_id:{"startTime":job["startTime"],"terminatedTime":job["terminateTime"],"state":job["state"],"job_type":job["job_type"]} for (job_id,job) in JobScheduler.jobs.items()}
