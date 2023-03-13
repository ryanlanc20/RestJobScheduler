const UnsignedIntField = (props) => {
    const required = props.isRequired ? "required" : "";

    return (
        <>
            <input type="number" className="form-control" id={props.fieldName} min={props.minValue} max={props.maxValue} required={required} name={props.name}/>
        </>
    )
};

export default UnsignedIntField;