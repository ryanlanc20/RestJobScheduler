'''
   Entrypoint script for job scheduling server.
   Optional CLI arguments:

   -f or --file: File path of job templates
   -i or --ipaddress: IP address for API controller
   -p or --port: Port number for API controller
'''
if __name__ == "__main__":

    import json
    from job_scheduler import JobScheduler
    from lazy_initializors.get_handler import getHandler
    from api import getAPIObject
    from optparse import OptionParser
    from inspect import getmembers,isfunction

    # Define CLI arguments parser
    parser = OptionParser()
    parser.add_option(
        "-f",
        "--file",
        dest="filename",
        help="File to load job templates from",
        default="./job_templates.json"
    )
    parser.add_option(
        "-i",
        "--ipaddress",
        dest="apiIp",
        help="IP address for RestAPI",
        default="127.0.0.1"
    )
    parser.add_option(
        "-p",
        "--port",
        dest="apiport",
        help="Port number for RestAPI",
        default=5000
    )

    # Get parsed CLI arguments
    (options, args) = parser.parse_args()

    # Try to convert port number string to integer
    port = int(options.apiport)

    # Check if port number is positive
    if port < 0:
        raise AssertionError("Port number must be a positive integer")

    # Load job templates
    job_templates = json.load(open(options.filename,"r",encoding="UTF-8"))

    # Load handlers
    handlerMappings = {}
    for job_type in job_templates.keys():
        moduleFunctions = __import__(f"job_schedule_handlers.{job_type}",fromlist=[""])
        for (funcName,funcHandler) in getmembers(moduleFunctions,isfunction):
            if funcName == job_type:
                handlerMappings[job_type] = funcHandler

    # TODO: Check if all handlers were loaded. Throw exception otherwise

    # Schedule periodic jobs
    for (job_type,job_tpl) in job_templates.items():
        if not job_tpl["userTriggered"]:
            job_id = JobScheduler.createJobId(job_type)
            payload = job_tpl["payload"].copy()
            payload["job_id"] = job_id
            JobScheduler.scheduleJob(
                job_tpl["startInSeconds"],
                getHandler(handlerMappings[job_type],payload),
                job_id,
                job_type
            )

    scheduler = JobScheduler()
    scheduler.start()
    api = getAPIObject(job_templates,handlerMappings)
    api.run("0.0.0.0",port)
