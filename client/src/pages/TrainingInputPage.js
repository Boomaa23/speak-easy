import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './pages.css';
import { FaMicrophone } from 'react-icons/fa';

const TrainingInputPage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [recorder, setRecorder] = useState(null);
  const [dots, setDots] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (isRecording) {
      const interval = setInterval(() => {
        setDots((prev) => (prev.length < 3 ? prev + '.' : ''));
      }, 500);
      return () => clearInterval(interval);
    } else {
      setDots('');
    }
  }, [isRecording]);

  const toggleRecording = async () => {
    if (isRecording) {
      recorder.stop();
      setIsRecording(false);
    } else {
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
      };

      mediaRecorder.start();
      setIsRecording(true);
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
      console.log(data);
      navigate('/choosetool');
    }
  };

  return (
    <div className="page-container">
      <div className="core-text">
        First, we're going to need to know how you sound. Please record a 10-20 second sample of yourself 
        speaking. You can say whatever you want, just make sure that you speak in your 
        <span className="highlight-bold"> native language</span>. Please speak as clearly as possible, 
        avoiding background noises and long pauses.
      </div>

      {/* Microphone icon container */}
      <div
        className={`mic-icon-container ${isRecording ? 'recording' : ''}`}
        onClick={toggleRecording}
      >
        <FaMicrophone className="mic-icon" />
      </div>

      {isRecording && <div className="recording-status">Recording{dots}</div>}

      {audioURL && !isRecording && (
        <div className="actions">
          <button className="action-btn" onClick={handleNext}>
            Next
          </button>
          <button className="action-btn" onClick={toggleRecording}>
            Record Again
          </button>
        </div>
      )}
    </div>
  );
};

export default TrainingInputPage;
