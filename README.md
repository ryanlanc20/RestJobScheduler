# About RestJobScheduler

This project is a distributed job scheduler, which allows engineers to schedule backend tasks (i.e., batch jobs)
by consuming the HTTP RestAPI itself or using the UI provided. It allows engineers to create reusable job scheduling templates,
which define a task, along with its required payload attributes and default values. These templates are used to instantiate and
schedule jobs, as well as assisting with payload validation and the creation of dynamic front-end forms.

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
        docker build ./
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
