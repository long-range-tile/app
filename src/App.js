import React, { useState, useEffect } from 'react';
import socketIOClient from "socket.io-client";
import './App.css';

const WS_ENDPOINT = "http://127.0.0.1:5000";

function App() {
  const [response, setResponse] = useState("None yet...");

  useEffect(() => {
    const socket = socketIOClient(WS_ENDPOINT, {});
    socket.on("NewData", data => {
      setResponse(data);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data from server:</h1>
        <p><pre>{JSON.stringify(response, 2)}</pre></p>
      </header>
    </div>
  );
}

export default App;
