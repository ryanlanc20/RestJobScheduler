import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import NavigationBar from './components/NavigationBar';
import CreateJobPage from './pages/CreateJobPage.js';
import { useState, useEffect } from 'react';
import axios from "axios";
import JobsList from './components/jobs/JobsList.js';
import DynamicForm from './components/forms/DynamicForm';
import socketIOClient from "socket.io-client";

const notificationsSocket = socketIOClient("http://127.0.0.1:9030");

function App() {
  const [schemas,setSchemas] = useState([]);
  const [lastUpdateTime,setLastUpdateTime] = useState();

  useEffect(()=>{
    axios.get("http://127.0.0.1:5000/schemas").then((response) => {
        setSchemas(response.data);
    });
  },[]);

  return (
    <div className="App">
        <i>Last update: {lastUpdateTime}</i>
        <JobsList eventListener={notificationsSocket}/>
        <div class="container-md">
        <DynamicForm 
            schemas={schemas}
            urlPrefix={"http://127.0.0.1:5000/create"}
        />
        </div>
    </div>
  );
}

export default App;
