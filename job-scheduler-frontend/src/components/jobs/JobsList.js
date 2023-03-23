import {useState,useEffect} from "react";
import axios from "axios";
import JobListItem from "./JobListItem.js";
import AlertsBox from "../alerts/AlertsBox.js";
import {apiUrl} from "../../constants.js";

const JobsList = (props) => {
    const [jobs,setJobs] = useState({});
    const [errors,setErrors] = useState([]);
    const [lastUpdateTime,setLastUpdateTime] = useState();

    const addError = (msg) => {
        setErrors((errorMessages) => {
            let newErrors = [...errorMessages];
            newErrors.push(msg);
            return newErrors;
        });
    };

    const updateJobListItem = (job_data) => {
        setJobs((jobs) => {
            let newJobs = {...jobs};
            newJobs[job_data["job_id"]] = {
                "startTime":job_data["startTime"],
                "terminatedTime":job_data["terminateTime"],
                "state":job_data["state"],
                "job_type":job_data["job_type"],
                "job_id": job_data["job_id"],
                "completion_percentage": job_data["completion_percentage"]
            }
            return newJobs;
        });
    };

    const addJobListItem = (job_data) => {
        setJobs((jobs) => {
            let newJobs = {...jobs};
            newJobs[job_data["job_id"]] = job_data;
            return newJobs;
        })
    }

    useEffect(() => {

        axios.get(`${apiUrl}/jobs`).then((response) => {
            setJobs(response.data);
        }).catch(() => {
            addError("Failed to fetch jobs list from server");
        });

        props.eventListener.on("notification",(msg) => {
            msg = JSON.parse(msg);
            if (msg.notification_type === "job_terminated" || msg.notification_type === "job_progress")
            {
                setLastUpdateTime((new Date()).toUTCString());
                updateJobListItem(msg["data"]);
            }
            if (msg.notification_type === "job_created")
            {
                setLastUpdateTime((new Date()).toUTCString());
                addJobListItem(msg["data"]);
            }
        });
    },[]);

    return (
        <div class="container-md mt-4">
            <div className="card">
                <div className="card-header">
                    All jobs
                    <button className="btn btn-primary float-end" onClick={props.toggleCreateJobForm}>Create job</button>
                </div>
                <div class="card-body">
                        <AlertsBox items={errors} type="error"/>
                        <i>Last update: {lastUpdateTime}</i>
                        <table className="table table-striped mt-4">
                            <thead>
                                <tr>
                                    <th scope="col">Job Id</th>
                                    <th scope="col">Job Type</th>
                                    <th scope="col">Start Time</th>
                                    <th scope="col">End Time</th>
                                    <th scope="col">Status</th>
                                    <th scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {
                                    Object.keys(jobs).length > 0 ?
                                        Object.entries(jobs).map(([job_id,job]) => 
                                            <JobListItem
                                                job_id={job_id}
                                                startTime={job["startTime"]}
                                                terminatedTime={job["terminatedTime"]}
                                                state={job["state"]}
                                                addError={addError}
                                                key={"job_"+job_id}
                                                type={job.job_type}
                                                progress={job["completion_percentage"]}
                                            />
                                        )
                                    :
                                        "No jobs available"
                                }
                            </tbody>
                        </table>
                </div>
            </div>
        </div>
    )
};

export default JobsList;