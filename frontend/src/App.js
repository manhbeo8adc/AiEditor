import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const checkBackendStatus = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:5000/api/status');
      setStatus(`Backend Status: ${response.data.message}`);
    } catch (error) {
      setStatus('Backend connection failed');
      console.error('Error:', error);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Video Editor</h1>
        <p>Merge videos with AI-generated transitions</p>
        
        <div className="status-section">
          <button onClick={checkBackendStatus} disabled={loading}>
            {loading ? 'Checking...' : 'Check Backend Status'}
          </button>
          {status && <p className="status-message">{status}</p>}
        </div>

        <div className="upload-section">
          <h2>Upload Videos</h2>
          <p>Video upload functionality will be implemented here</p>
          {/* TODO: Add video upload components */}
        </div>

        <div className="processing-section">
          <h2>Processing</h2>
          <p>Video processing controls will be implemented here</p>
          {/* TODO: Add processing controls */}
        </div>
      </header>
    </div>
  );
}

export default App; 