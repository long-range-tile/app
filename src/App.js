import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';
import './App.css';
import GaugeChart from 'react-gauge-chart';

const WS_ENDPOINT = "ws://127.0.0.1:5000";
const socket = io(WS_ENDPOINT);

function parsePosition({ coords, timestamp }) {
  return {
    coords: {
      latitude: coords.latitude,
      longitude: coords.longitude,
      accuracy: coords.accuracy,
      heading: coords.heading,
      altitude: coords.altitude,
      altitudeAccuracy: coords.altitudeAccuracy,
    },
    timestamp,
  };
}

function sendPosition(position) {
  const gpsData = parsePosition(position);
  socket.emit('gps_data', gpsData);
}

function sendCurrentGpsData() {
  navigator.geolocation.getCurrentPosition(sendPosition);
}

function setupWatcher() {
  const watchID = navigator.geolocation.watchPosition(sendPosition);
  console.log('setup watcher!');
  return () => {
    navigator.geolocation.clearWatch(watchID);
    console.log('cleaned up watcher!');
  };
}

function App() {
  const [response, setResponse] = useState(null);

  useEffect(() => {
    socket.on("NewData", data => {
      setResponse(data);
    });
  }, []);

  useEffect(() => {
    const clearWatcher = setupWatcher();
    return clearWatcher;
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
      </header>
    </div>
  );
}

export default App;
