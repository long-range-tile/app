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
  return () => {
    navigator.geolocation.clearWatch(watchID);
  };
}

function diffToNowSec(stamp) {
    const d = new Date(stamp);
    const now = new Date();
    const diff = now - d;
    return diff / 1000;
}

function DispResponse({ response }) {
  const [ago, setAgo] = useState(0);
  useEffect(() => {
    setAgo(diffToNowSec(response));
    const t = setInterval(() => {
      setAgo(diffToNowSec(response));
    }, 100);
    return () => {
      clearInterval(t);
    };
  }, [response]);

  if (!response) {
    return 'Waiting for initial response...';
  }
  let color = 'red';
  if (ago < 20) {
    color = 'yellow';
  }
  if (ago < 10) {
    color = 'green';
  }
  return (
    <p style={{color}}>
      GPS data received {ago}s ago
    </p>
  );
}

function App() {
  const [response, setResponse] = useState(null);

  useEffect(() => {
    socket.on("got_gps", data => {
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
        <div align="left">
          <pre>
            <DispResponse response={response} />
          </pre>
        </div>
        {/* <div id="chart">
          {response && <GaugeChart
            percent={(response.counter / 100.0)}
            animate={false}
          />}
        </div> */}
      </header>
    </div>
  );
}

export default App;
