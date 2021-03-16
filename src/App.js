import React, { useState, useEffect } from 'react';
import socketIOClient from 'socket.io-client';
import './App.css';
import GaugeChart from 'react-gauge-chart';

const WS_ENDPOINT = "ws://127.0.0.1:5000";
const socket = socketIOClient(WS_ENDPOINT);

function App() {
  const [response, setResponse] = useState(null);

  useEffect(() => {
    socket.on("NewData", data => {
      setResponse(data);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Data from server:</h1>
        <div align="left"><pre>{response ? JSON.stringify(response, null, 2) : 'Waiting for initial data...'}</pre></div>
        {response && <GaugeChart
          percent={(response.counter / 100.0)}
          animate={false}
        />}
      </header>
    </div>
  );
}

export default App;
