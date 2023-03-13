const OptionsField = (props) => {
    return (
    <>
        <select name={props.name} className="form-control" onChange={props.onChange}>
            {
                props.values.map((option) => {
                    return <option value={option}>{option}</option>
                })
            }
        </select>
    </>
    )
};

export default OptionsField;