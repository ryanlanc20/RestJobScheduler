import {useState,useEffect} from "react";
import axios from "axios";
import JobListItem from "./JobListItem.js";
const JobsList = (props) => {
    const [jobs,setJobs] = useState({});
    const [errors,setErrors] = useState({});
    const [lastUpdateTime,setLastUpdateTime] = useState();

    const addError = (type,msg) => {
        setErrors((errorMessages) => {
            let newErrors = {...errorMessages};
            newErrors[type] = msg;
            return newErrors;
        });
    };

    const updateJobListItem = (job_data) => {
        setJobs((jobs) => {
            let newJobs = {...jobs};
            newJobs[job_data["job_id"]] = {"startTime":job_data["startTime"],"terminatedTime":job_data["terminateTime"],"state":job_data["state"],"job_type":job_data["job_type"],"job_id": job_data["job_id"]}
            console.log(job_data);
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
        axios.get("http://127.0.0.1:5000/jobs").then((response) => {
            setJobs(response.data);
        }).catch(() => {
            addError("failedFetchJobs","Failed to fetch jobs list from server");
        });
        props.eventListener.on("notification",(msg) => {
            console.log(msg);
            msg = JSON.parse(msg);
            if (msg.notification_type === "job_terminated")
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
        <div class="container-md">
            <i>Last update: {lastUpdateTime}</i>
            {
                Object.keys(errors).length > 0 ? Object.values(errors).map((error) => error) : ""
            }
            <table className="table table-striped">
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
                        
                    }
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
                                />
                            )
                        :
                            "No jobs available"
                    }
                </tbody>
            </table>
        </div>
    )
};

export default JobsList;