# About RestJobScheduler

This project is a distributed job scheduler, which allows engineers to schedule backend tasks (i.e., batch jobs)
by consuming the HTTP RestAPI itself or using the UI provided. It allows engineers to create reusable job scheduling templates,
which define a task, along with its required payload attributes and default values. These templates are used to instantiate and
schedule jobs, as well as assisting with payload validation and the creation of dynamic front-end forms.

## Architecture
![architecture](https://user-images.githubusercontent.com/32577906/225432070-efe31df8-8b78-4502-a371-a50a9bc57d5f.jpg)
