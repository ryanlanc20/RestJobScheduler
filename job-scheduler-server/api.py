from flask import Flask,request
from flask_cors import CORS
from lazy_initializors.get_handler import getHandler
from job_scheduler import JobScheduler
import json
from messaging_helpers.submit_notification import submit_notification

def getAPIObject(job_templates,handlerMappings):

    app = Flask(__name__)
    cors = CORS(app)

    @app.route("/schemas",methods=["GET"])
    def getSchemas():
        filteredSchemas = filter(lambda item: item[1]["userTriggered"],job_templates.items())
        return {job_type: template["payload_schema"] for (job_type,template) in filteredSchemas}
    
    @app.route("/create",methods=["POST"])
    def createJob():
        reqBody = dict(request.form)

        if not "job_type" in reqBody:
            return {"msg": "Job type must be specified in request body"},400
        
        if not (reqBody["job_type"] in job_templates):
            return {"msg": "Couldn't find job template"},404
        
        jobtype = reqBody["job_type"]
        
        template = job_templates[jobtype]
        payloadTemplate = None if "payload" not in template else template["payload"]
        payloadData = {}

        # Check payload template fields are present in form data
        if payloadTemplate:
            commonFields = set(reqBody.keys()).intersection(set(payloadTemplate.keys()))
            if not (len(commonFields) == len(set(reqBody.keys())) == len(set(payloadTemplate.keys()))):
                return {"msg": "Payload fields do not match schema."},400
            payloadData = reqBody

        job_id = JobScheduler.createJobId(jobtype)
        payloadData["job_id"] = job_id
        jobMetadata = JobScheduler.scheduleJob(template["startInSeconds"],getHandler(handlerMappings[jobtype],payloadData),job_id,jobtype)

        didSubmitNotification = submit_notification({"notification_type": "job_created","data":jobMetadata})

        return {"msg": "Job created","job_id": jobMetadata["job_id"],"pollForChanges":not didSubmitNotification}
    
    @app.route("/jobs",methods=["GET"])
    def getAllJobs():
        return JobScheduler.getActiveJobs()
    
    @app.route("/job/<jobid>/terminate",methods=["POST"])
    def teminateJob(jobid):

        if not jobid in JobScheduler.jobs.keys():
            return {"msg": "Job not found"},404

        payload = dict(request.form)

        if not "type" in payload.keys():
            return {"msg": "Payload must contain job type"},400
        
        if not payload["type"] in job_templates.keys():
            return {"msg": "No job template exists for the specified type"},400
        
        result = JobScheduler.cancelJob(jobid)
        job_template = job_templates[payload["type"]]
        if job_template["rescheduleAfterTermination"]:
            job_id = JobScheduler.createJobId(payload["type"])
            newJob = JobScheduler.scheduleJob(job_template["startInSeconds"],getHandler(handlerMappings[payload["type"]],job_template["payload"]),job_id,payload["type"])
            submit_notification({"notification_type": "job_created","data":newJob})

        didSubmitNotification = submit_notification({"notification_type": "job_terminated","data":result})
        return {"msg": "Job terminated","pollForChanges": not didSubmitNotification}

    
    return app
