import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import './App.css';
import GaugeChart from 'react-gauge-chart';

const WS_ENDPOINT = "ws://127.0.0.1:5000";
const socket = io(WS_ENDPOINT);

async function sendGpsData() {
  navigator.geolocation.getCurrentPosition(function ({ coords, timestamp }) {
    socket.emit('gps_data', {
      coords: {
        latitude: coords.latitude,
        longitude: coords.longitude,
      },
      timestamp,
    });
  });
}

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
        <div align="left">
          <pre>{response ? JSON.stringify(response, null, 2) : 'Waiting for initial data...'}</pre>
        </div>
        <div id="chart">
          {response && <GaugeChart
            percent={(response.counter / 100.0)}
            animate={false}
          />}
        </div>
        <div>
          <button onClick={sendGpsData}>
            Send GPS data
          </button>
        </div>
      </header>
    </div>
  );
}

export default App;
