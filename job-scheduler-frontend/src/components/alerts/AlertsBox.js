const AlertsBox = (props) => {
    let type;

    if(props.type === "error")
        type = "alert-danger";

    if(props.type === "success")
        type = "alert-success";

    return (
        props.items.length > 0 ? 
            <div class={`alert ${type}`}>
            {
                props.items.map((item) => {return <li>{item}</li>})
            }
            </div> 
        : 
            ""
    )
};

export default AlertsBox;