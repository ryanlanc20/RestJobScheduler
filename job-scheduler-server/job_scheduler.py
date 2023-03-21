'''
    This module contains the JobScheduler class.
    You can import JobScheduler using:

    from job_scheduler import JobScheduler
'''
import threading
import time
import schedule


class JobScheduler(threading.Thread):
    '''
        JobScheduler class

        This class provides methods to create and cancel jobs.
        All data relating to jobs is stored and maintained within this class,
        so there is no need to store job data anywhere else.

        The run method of this class runs asynchronously, to allow tasks in the parent thread
        to resume execution.
    '''

    # Jobs datastore
    jobs = {}

    running = threading.Event()

    def run(self):
        '''
            This method is executed asynchronously and runs the jobs.
        '''
        while not JobScheduler.running.is_set():
            schedule.run_pending()
            time.sleep(1)

    @staticmethod
    def create_job_id(job_type):
        '''
            This method returns a unique job id for a given job type.

            Parameters:
                job_type: String describing job type
        '''
        return job_type + "_" + str(time.time())

    @staticmethod
    def schedule_job(execution_delay,job_executer_delegate,job_id,job_type):
        '''
            This method registers a job with the scheduler.

            Parameters:
                execution_delay: Timeout for starting job (Integer)
                job_executor_delegate: Callback method which executes when the job starts (Function)
                job_id: ID for the job (String)
                job_type: Description of job type (String)
        '''
        job = {
            "scheduler_obj": schedule.every(execution_delay).seconds.do(job_executer_delegate),
            "startTime": time.time()*1000,
            "terminateTime": -1,
            "state":"scheduled",
            "job_type":job_type,
            "completion_percentage": 0
        }

        JobScheduler.jobs[job_id] = job

        return {
            "job_id": job_id,
            "startTime":job["startTime"],
            "terminatedTime":job["terminateTime"],
            "state": job["state"],
            "job_type":job_type,
            "completion_percentage": 0
        }

    @staticmethod
    def cancel_job(job_id):
        '''
            This method cancels a job with the specified job id.

            Parameters:
                job_id: Unique identifier for job (String)
        '''

        # Job does not exist
        if not job_id in JobScheduler.jobs:
            return False

        # Terminate job
        job = JobScheduler.jobs[job_id]
        schedule.cancel_job(job["scheduler_obj"])
        job["terminateTime"] = time.time() * 1000
        job["state"] = "terminated"

        return {
            "job_id":job_id,
            "startTime":job["startTime"],
            "terminateTime": job["terminateTime"],
            "state":job["state"],
            "job_type": job["job_type"]
        }

    @staticmethod
    def get_active_jobs():
        '''
            This method returns a list of jobs.
        '''
        return {
            job_id:{
                "startTime":job["startTime"],
                "terminatedTime":job["terminateTime"],
                "state":job["state"],
                "job_type":job["job_type"],
                "completion_percentage": job["completion_percentage"]
            }
            for (job_id,job) in JobScheduler.jobs.items()
        }

    @staticmethod
    def update_job_progress(job_id,progress):
        job = JobScheduler.jobs[job_id]
        job["completion_percentage"] = progress
    
        return {
            "job_id": job_id,
            "startTime": job["startTime"],
            "terminateTime": job["terminateTime"],
            "state": job["state"],
            "job_type": job["job_type"],
            "completion_percentage": job["completion_percentage"]
        }