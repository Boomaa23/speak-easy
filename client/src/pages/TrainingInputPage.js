import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './pages.css'; // Import the custom styles
import { FaMicrophone } from 'react-icons/fa'; // Import microphone icon

const TrainingInputPage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [recorder, setRecorder] = useState(null);
  const [dots, setDots] = useState('');
  const navigate = useNavigate();

  // Handle the "recording ..." dot animation
  useEffect(() => {
    if (isRecording) {
      const dotInterval = setInterval(() => {
        setDots((prev) => (prev.length < 3 ? prev + '.' : ''));
      }, 500);
      return () => clearInterval(dotInterval);
    } else {
      setDots('');
    }
  }, [isRecording]);

  // Start or stop recording
  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording
      recorder.stop();
      setIsRecording(false);
    } else {
      // Start recording
      if (!recorder) {
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
          setAudioURL(audioUrl); // Store the URL to play back
        };

        mediaRecorder.start();
        setIsRecording(true);
      } else {
        recorder.start();
        setIsRecording(true);
      }
    }
  };

  // Handle navigation to the next page and sending data to backend
  const handleNext = () => {
    // if (audioURL) {
    //   // Send audio to backend (example: using fetch)
    //   fetch('your-backend-endpoint', {
    //     method: 'POST',
    //     body: JSON.stringify({ audio: audioURL }),
    //     headers: { 'Content-Type': 'application/json' },
    //   });

    //   // Navigate to output page
    //   navigate('/output');
    // }

    navigate('/choosetool');
  };

  return (
    <div className="page-container">
      <div className="core-text">
        First, we're going to need to know how you sound. Please record a 10-20 second sample of yourself 
        speaking. You can say whatever you want, just make sure that you speak in your 
        <span className="highlight-bold"> native language</span>. Please speak as clearly as possible, 
        avoiding background noises and long pauses.
        <br />
        <br />
        Click the microphone icon to start recording:
        <span className={`mic-icon ${isRecording ? 'recording' : ''}`} onClick={toggleRecording}>
          <FaMicrophone size={30} />
        </span>
      </div>
      {isRecording && (
        <div className="recording-status">Recording{dots}</div>
      )}
      {audioURL && !isRecording && (
        <div className="actions">
          <button className="action-btn" onClick={handleNext}>Next</button>
          <button className="action-btn" onClick={toggleRecording}>Record Again</button>
        </div>
      )}
    </div>
  );
};

export default TrainingInputPage;
