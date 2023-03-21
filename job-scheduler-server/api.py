'''
    This module contains a method to retrieve an instance of the API controller.
'''
from flask import Flask,request
from flask_cors import CORS
from lazy_initializors.get_handler import getHandler
from job_scheduler import JobScheduler
from messaging_helpers.submit_notification import submit_notification

def get_api_object(job_templates,handler_mappings):
    '''
        This method returns a FLASK web server object, with all required routes attached.

        Parameters:
            job_templates: Dictionary containing job templates
            handler_mappings: Dictionary mapping job types onto their respective callbacks

        Returns:
            Flask object
    '''

    app = Flask(__name__)
    CORS(app)

    @app.route("/schemas",methods=["GET"])
    def get_schemas():
        # Only retrieve form schemas for user triggered jobs
        filtered_schemas = filter(lambda item: item[1]["userTriggered"],job_templates.items())
        return {job_type: template["payload_schema"] for (job_type,template) in filtered_schemas}

    @app.route("/create",methods=["POST"])
    def create_job():
        req_body = dict(request.form)

        # Check job_type is specified
        if "job_type" not in req_body:
            return {"msg": "Job type must be specified in request body"},400

        # Check if specified job type belongs to a template
        if req_body["job_type"] not in job_templates:
            return {"msg": "Couldn't find job template"},404

        # Get required payload fields for job; also provides default values for fields.
        job_type = req_body["job_type"]
        template = job_templates[job_type]
        payload_template = None if "payload" not in template else template["payload"]
        payload_data = {}

        # Check payload template fields are present in form data
        if payload_template:
            # TODO: Refactor field presence checks and validate in accordance with schema
            common_fields = set(req_body.keys()).intersection(set(payload_template.keys()))
            if not len(common_fields) == len(set(req_body.keys())) == len(set(payload_template.keys())):
                return {"msg": "Payload fields do not match schema."},400
            payload_data = req_body

        # Create and schedule job
        job_id = JobScheduler.create_job_id(job_type)
        payload_data["job_id"] = job_id
        job_metadata = JobScheduler.schedule_job(
            template["startInSeconds"],
            getHandler(handler_mappings[job_type],payload_data),
            job_id,
            job_type
        )

        # Dispatch notification
        did_submit_notification = submit_notification({
            "notification_type": "job_created",
            "data":job_metadata
        })

        return {
            "msg": "Job created",
            "job_id": job_metadata["job_id"],
            "pollForChanges":not did_submit_notification
        }

    @app.route("/jobs",methods=["GET"])
    def get_all_jobs():
        return JobScheduler.get_active_jobs()

    @app.route("/job/<jobid>/terminate",methods=["POST"])
    def teminate_job(jobid):

        # Check if job exists
        if jobid not in JobScheduler.jobs:
            return {"msg": "Job not found"},404

        payload = dict(request.form)

        # Type is important when determining what type of job to reschedule
        if not "type" in payload.keys():
            return {"msg": "Payload must contain job type"},400

        if not payload["type"] in job_templates.keys():
            return {"msg": "No job template exists for the specified type"},400

        # Cancel job
        result = JobScheduler.cancel_job(jobid)

        # Reschedule job if job template permits
        job_template = job_templates[payload["type"]]
        if job_template["rescheduleAfterTermination"]:
            job_id = JobScheduler.create_job_id(payload["type"])
            new_job = JobScheduler.schedule_job(
                job_template["startInSeconds"],
                getHandler(handler_mappings[payload["type"]],job_template["payload"]),
                job_id,
                payload["type"]
            )

            # Dispatch job creation notification
            submit_notification({"notification_type": "job_created","data":new_job})

        # Dispatch job termination notification
        did_submit_notification = submit_notification({
            "notification_type": "job_terminated",
            "data":result
        })

        return {"msg": "Job terminated","pollForChanges": not did_submit_notification}
    
    @app.route("/job/<jobid>/progress",methods=["POST"])
    def update_job_progress(jobid):
        # Check if job exists
        if jobid not in JobScheduler.jobs:
            return {"msg": "Job not found"},404
        
        # Validate form data
        form_data = dict(request.form)

        if "completion_percent" not in form_data:
            return {"msg": "Completion percent must be specified"},400
        
        percent = float(form_data["completion_percent"])
        if percent < 0 or percent > 100:
            return {"msg": "Percentage out of range"},400
        
        JobScheduler.update_job_progress(jobid,percent)

        did_submit_notification = submit_notification({
            "notification_type": "job_progress",
            "data": {
                "job_id": jobid,
                "completion_percentage": percent
            }
        })

        return {"msg": "Updated job progress"}
        

    return app
