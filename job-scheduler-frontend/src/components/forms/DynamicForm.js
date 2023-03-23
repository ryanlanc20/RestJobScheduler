import OptionsField from "./OptionsField";
import UnsignedIntField from "./UnsignedIntField"
import AlertsBox from "../alerts/AlertsBox.js";
import { useState } from "react";
import axios from "axios";
import {apiUrl} from "../../constants.js";

const DynamicForm = (props) => {

    const [formName,setFormName] = useState(null);
    const [errors,setErrors] = useState([]);
    const [successMsgs,setSuccessMsgs] = useState([]);

    const addError = (error) => {
        setErrors((errorList) => {
            let newErrorList = [...errorList];
            newErrorList.push(error);
            return newErrorList;
        });
    };

    const addSuccessMessage = (successMsg) => {
        setSuccessMsgs((msgs) => {
            let new_msgs = [...msgs];
            new_msgs.push(successMsg);
            return new_msgs;
        })
    }

    const selectComponent = (schema,fieldName) => {
        if (schema.type === "uint")
            return <UnsignedIntField isRequired={schema.isRequired} minValue={schema.minValue} maxValue={schema.maxValue} name={fieldName}/>
        if (schema.type === "options")
            return <OptionsField values={schema.options} name={fieldName}/>
    };

    const switchForm = (e) => {
        setFormName(e.target.value);
    };

    const submitForm = (e) => {

        // Reset error tracking
        setErrors([]);
        setSuccessMsgs([]);

        // Prevent request to server
        e.preventDefault();
        
        let body = {};

        // Get form data
        Object.keys(props.schemas[formName]).forEach((field) => {
            body[field] = e.target.elements[field].value;
        });

        // Create job
        axios.post(`${apiUrl}/create`,body,{"headers":{"Content-Type":"multipart/form-data"}}).then((response) => {
            addSuccessMessage("Successfully submitted form.");
        }).catch(() => {
            addError("Failed to submit form. Please try again soon.");
        });
    };

    return(
        <div className="card">
            <div className="card-header">
                Create new job
                {
                    "closeBtn" in props ? props.closeBtn : ""
                }
            </div>
            <div class="card-body">
                <AlertsBox items={errors} type="error"/>
                <AlertsBox items={successMsgs} type="success"/>
                <form action="#" method="POST" onSubmit={submitForm}>
                <div class="row mt-2">
                    <label>Select job type</label>
                </div>
                <div class="row mt-2">
                    <div class="col">
                        <OptionsField values={Object.keys(props.schemas)} onChange={switchForm} name="job_type"/>
                    </div>
                </div>
                {
                    formName === null ?
                        ""
                    : 
                        <>
                            {
                                Object.entries(props.schemas[formName]).map(([job_type,control]) => {
                                    return control ? <>
                                                <div class="row mt-4">
                                                    <div class="col"><label for={control.label}>{control.label}</label></div>
                                                </div>
                                                <div class="row mt-2">
                                                    <div class="col">{selectComponent(control,job_type)}</div>
                                                </div>
                                        </> : ""
                                })
                            }
                            <div class="row mt-5">
                                <div class="col">
                                    <input type="submit" className="btn btn-primary w-100" value="Create job"/>
                                </div>
                            </div>
                        </>
                }
                </form>
            </div>
        </div>
    )
};

export default DynamicForm;