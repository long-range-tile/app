import React, { useState, useEffect } from 'react';
import socketIOClient from "socket.io-client";
import './App.css';

const WS_ENDPOINT = "ws://127.0.0.1:5000";
const socket = socketIOClient(WS_ENDPOINT);

function App() {
  const [response, setResponse] = useState("Request some data.");

  useEffect(() => {
    socket.on("NewData", data => {
      setResponse(data);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data from server:</h1>
        <button
          onClick={() => {
            setResponse("Loading...");
            socket.emit("DataRequest");
          }}
        >
          Send message
        </button>
        <div><pre>{JSON.stringify(response, 2)}</pre></div>
      </header>
    </div>
  );
}

export default App;
