import {useState} from "react";
import axios from "axios";
import { apiUrl } from "../../constants";

const JobListItem = (props) => {
    const [,setStatus] = useState(props.state);

    const terminateAction = () => {
        // Cancel job
        axios.post(`${apiUrl}/job/${props.job_id}/terminate`,{"type":props.type},{"headers":{"Content-Type":"multipart/form-data"}}).then((response) => {
            setStatus("Terminated");
        }).catch(() => {
            props.addError("Unable to terminate job");
        });
    };

    return (
        <tr>
            <td>{props.job_id}</td>
            <td>{props.type}</td>
            <td>{new Date(props.startTime).toUTCString()}</td>
            <td>{props.terminatedTime === -1 ? "N/A" : new Date(props.terminatedTime).toUTCString()}</td>
            <td>{props.state}</td>
            <td>
                {
                    props.state !== "terminated" ? 
                        <button className="btn btn-danger" onClick={terminateAction}>Terminate</button>
                    :
                        ""
                }
            </td>
        </tr>
    )
};

export default JobListItem;