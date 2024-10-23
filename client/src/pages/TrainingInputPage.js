import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './training.css';
import { FaMicrophone } from 'react-icons/fa';
import { getCookie, setCookie } from '../cookieUtils.js';

const TrainingInputPage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [recorder, setRecorder] = useState(null);
  const [showHint, setShowHint] = useState(false); // Control hint visibility
  const [hintText, setHintText] = useState(''); // Manage dynamic hint text
  const navigate = useNavigate();

  // Hide hint text when recording starts, show after 5 seconds
  useEffect(() => {
    let hintTimeout;
    if (isRecording) {
      setShowHint(false); // Hide hint when recording starts

      // Show the "Click the mic to stop recording!" hint after 5 seconds
      hintTimeout = setTimeout(() => {
        setHintText('Click the mic to stop recording!');
        setShowHint(true);
      }, 5000);
    }

    return () => clearTimeout(hintTimeout); // Clean up timeout on unmount or stop
  }, [isRecording]);

  // Start recording 1 second after the component mounts
  useEffect(() => {
    const timeout = setTimeout(() => {
      startRecording();
    }, 1000);

    return () => {
      clearTimeout(timeout); // Clean up timeout
      if (recorder) recorder.stop(); // Stop recorder on unmount
    };
  }, []);

  // Function to start recording
  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    setRecorder(mediaRecorder);

    const audioChunks = [];
    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioURL(audioUrl);

      // Update hint text after stopping recording
      setHintText('Click the mic to start recording again!');
      setShowHint(true);
    };

    mediaRecorder.start();
    setIsRecording(true);
  };

  // Toggle recording when the mic icon is clicked
  const toggleRecording = () => {
    if (isRecording) {
      recorder.stop();
      setIsRecording(false);
    } else {
      startRecording();
    }
  };

  const handleNext = async () => {
    if (audioURL) {
      const audioResponse = await fetch(audioURL);
      const audioBlob = await audioResponse.blob();

      const formData = new FormData();
      formData.append('audio', audioBlob, 'audio.mp3');

      const response = await fetch('http://localhost:5000/api/train', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error(`Error: ${response.statusText}`);

      const data = await response.json();
      if (!getCookie("user_id")) {
        setCookie("user_id", data["user_id"])
      }
      console.log(data);
      navigate('/choosetool');
    }
  };

  return (
    <div className="page-container">
      <div className="core-text">
        <span className="highlight-bold">Read the following out loud:</span><br />
        "I agree to train my voice for the purposes of the best CalHacks demo, and I
        agree to give this team the best score. This recording is about 15 to 20 seconds 
        in order to train the model optimally."
      </div>

      {/* Microphone icon container */}
      <div
        className={`mic-icon-container ${isRecording ? 'recording' : ''}`}
        onClick={toggleRecording}
      >
        <FaMicrophone className="mic-icon" />
      </div>

      {/* Smooth hint text transition */}
      {showHint && (
        <div className={`hint-text ${showHint ? 'visible' : ''}`}>
          <br />{hintText}
        </div>
      )}

      {audioURL && !isRecording && (
        <div className="actions">
          <button className="action-btn" onClick={handleNext}>
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default TrainingInputPage;
