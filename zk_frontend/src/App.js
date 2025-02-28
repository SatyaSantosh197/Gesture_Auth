import React, { useRef } from 'react';
import Webcam from 'react-webcam';

function App() {
  const webcamRef = useRef(null);

  const captureGesture = async () => {
    if (webcamRef.current) {
      const imageData = webcamRef.current.getScreenshot();
      try {
        const response = await fetch('http://localhost:5000/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: imageData }),
        });
        const data = await response.json();
        alert(data.message);
      } catch (error) {
        console.error('Error during registration:', error);
      }
    }
  };

  const authenticateGesture = async () => {
    if (webcamRef.current) {
      const imageData = webcamRef.current.getScreenshot();
      try {
        const response = await fetch('http://localhost:5000/authenticate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ image: imageData }),
        });
        const data = await response.json();
        if (data.success) {
          alert('Authentication Successful!');
        } else {
          alert('Authentication Failed!');
        }
      } catch (error) {
        console.error('Error during authentication:', error);
      }
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '20px' }}>
      <h1>Zero-Knowledge Hand Gesture Authentication</h1>
      <Webcam
        audio={false}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        videoConstraints={{ width: 640, height: 480, facingMode: "user" }}
      />
      <div style={{ marginTop: '20px' }}>
        <button onClick={captureGesture} style={{ marginRight: '10px', padding: '10px 20px' }}>
          Register Gesture
        </button>
        <button onClick={authenticateGesture} style={{ padding: '10px 20px' }}>
          Authenticate
        </button>
      </div>
      <p>Ensure your hand gesture is clearly visible.</p>
    </div>
  );
}

export default App;