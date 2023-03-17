# About RestJobScheduler

This project is a distributed job scheduler, which allows engineers to schedule backend tasks (i.e., batch jobs)
by consuming the HTTP RestAPI itself or using the UI provided. It allows engineers to create reusable job scheduling templates,
which define a task, along with its required payload attributes and default values. These templates are used to instantiate and
schedule jobs, as well as assisting with payload validation and the creation of dynamic front-end forms.

## Features
* HTTP Rest API
* Web browser based UI to view jobs, create jobs and terminate jobs
* Dynamic frontend form rendering (creates forms based on payload schema defined in job templates)
* Real-time notifications (consumed by socket.io client)
* Reusable job templates

## Notes on configurations

### Updating RestAPI url and notifications push url in job-scheduler-frontend
To modify the URLS for these services, navigate to ./job-scheduler-frontend/src/constants.js.
If you are running the application in docker, you will need to run docker-compose down and then docker-compose up for changes to take effect.

### Adding a new job template
There are several example job templates already provided in ./job-scheduler-server/job_templates.json.
You can choose to duplicate an existing template and modify the values to suit your needs. Alternatively, you can make a job template from scratch. In either case, you job template must adhere to the following schema.

```
"<job-type>": {
        "type": "<job-type>",
        "startInSeconds": <uint>,
        "userTriggered": <bool>,
        "rescheduleAfterTermination": <bool>,
        "payload_schema": {
            "<field-name-1>": {"type": "uint","minValue": <uint>, "maxValue": <uint>,"required":<bool>,"label": <string>},
            "<field-name-2>": {"type": "options","options":<array-of-strings>,"required":<bool>,"label":<string>},
            <add more fields here>
        },
        "payload": {
            "profiles": <uint>
        }
}
```

#### Important notes on schema
* &lt;job-type&gt; must be the same value in both instances
* The userTriggered value determines the event type (i.e., true = user event, false = system event). User events can be triggered from the front-end application, but system events cannot. This means that the drop down box in the 'Create Job' form on the frontend only lists user triggered job types.
* The rescheduleAfterTermination value determines if a job with the specified job type will be scheduled again. This might be suitable for periodic tasks (i.e., batch jobs), but not for sending one time passcodes.
* If the userTriggered and rescheduleAfterTermination values are both set to true, this will allow users to run certain jobs (i.e., sending OTP) in an infinite loop. To avoid this situation, set rescheduleAfterTermination = false for user triggered jobs.
* API payload data is not yet validated against the payload schema, but this is coming soon. However, the request body must currently contain the keys listed in the payload definition.

#### Creating a job executor delegate function
For any job template you define in job_templates.json, you also need to provide a callback function, which will be executed when your job is running. Simply create a function similar to the following:

```python

   import schedule
   from job_scheduler import JobScheduler
   from messaging_helpers.submit_notification import submit_notification
   
   def <job-type>(data):
       # Do work here
       
       # Always end with the following three lines
       result = JobScheduler.cancel_job(data["job_id"])
       submit_notification({"notification_type": "job_terminated","data":result})
       return schedule.CancelJob
```

This file must be named <job-type>.py and stored inside ./job-scheduler-server/job_schedule_handlers. The scheduling server will load these functions dynamically using the &lt;job-type&gt; value defined in your job templates. The server must be restarted for changes to take effect.

## Architecture
![architecture](https://user-images.githubusercontent.com/32577906/225432070-efe31df8-8b78-4502-a371-a50a9bc57d5f.jpg)

The entire application can be launched by:
```bash
   cd ./RestJobScheduler
   docker-compose up
```

### Frontend UI
The Frontend UI is written in React. It uses axios and socket.io to retrieve data from the backend. Axios is used to perform job scheduling operations (i.e., creating a job), whereas socket.io is used to push real-time notifications to clients (i.e., job_terminated, job_created). The frontend app will run without these services running, but there will be no data to populate in the UI (i.e., jobs list). You can use the following methods to run the app.

* Running on localhost:
    ```bash
        cd ./job-scheduler-frontend
        npm install
        npm start
    ```
* Running as a standalone docker container
    ```bash
        cd ./job-scheduler-frontend
        docker build ./ -t job-scheduler-frontend
        docker run -p 3000:3000 job-scheduler-frontend
    ```
    
Note: When starting the frontend using either docker or docker-compose, a production build is created automatically with source mapping disabled. Currently, it is not possible to use hot-reloading whilst the react app is running inside the container. For development purposes, a development Dockerfile will be created soon to allow for hot-reloading and will ultimately keep the app in development mode. Alternatively, the frontend can be decoupled and simply run on localhost, whilst the rest of the application can run in docker.

### JobScheduler
The JobScheduler service exposes a HTTP Rest API, which can be used to create, view and terminate jobs. It uses the pika library to communicate with the message queue (used for job notifications). Just like with the frontend UI, it can also run as a standalone application on localhost, without other services running, since connection errors will not terminate the application. You can use the following methods to run the app.

* Running on localhost
    ```bash
        cd ./job-scheduler-server
        pip install pipenv
        pipenv install
        pipenv run <python-interpreter> scheduler.py
    ```
* Running as a standalone docker container
    ```bash
        cd ./job-scheduler-server
        docker build ./ -t job-scheduler-server
        docker run -p 5000:5000 job-scheduler-server
    ```
    
### Notifications Push Service
The Notifications Push Service receives dispatched notifications from the JobScheduler service and pushes them to the frontend. This cannot run as a standalone service and depends on a RabbitMQ instance. To run this service, it is best to run the entire application, using:

```bash
   cd ./RestJobScheduler
   docker-compose up
```

### Notifications Queue Service
The Notifications Queue Service is a RabbitMQ instance, running an extended version of the image, and this image enables the management plugins.
