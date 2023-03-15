import './App.css';
import NavigationBar from './components/NavigationBar';
import { useState, useEffect } from 'react';
import axios from "axios";
import JobsList from './components/jobs/JobsList.js';
import DynamicForm from './components/forms/DynamicForm';
import socketIOClient from "socket.io-client";

const notificationsSocket = socketIOClient("http://127.0.0.1:9030");

function App() {
  const [schemas,setSchemas] = useState([]);
  const [showCreateJobForm,setShowCreateJobForm] = useState();

  const toggleCreateJobForm = () => {
      setShowCreateJobForm((state) => !state);
  };

  useEffect(()=>{
    axios.get("http://127.0.0.1:5000/schemas").then((response) => {
        setSchemas(response.data);
    });
  },[]);

  return (
    <>
        <div class="main-content">
            <NavigationBar/>
            <JobsList
                eventListener={notificationsSocket}
                toggleCreateJobForm={toggleCreateJobForm}
            />
        </div>
        {
            showCreateJobForm ?
                <div class="overlay">
                    <div class="container-md">
                        <DynamicForm 
                            schemas={schemas}
                            urlPrefix={"http://127.0.0.1:5000/create"}
                            closeBtn={<button class="btn btn-danger float-end" onClick={toggleCreateJobForm}>X</button>}
                        />
                    </div>
                </div>
            :
            ""
        }
    </>
  );
}

export default App;
