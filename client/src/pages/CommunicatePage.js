import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './pages.css'; // Import the custom styles
import { FaMicrophone, FaPlay } from 'react-icons/fa'; // Import microphone and play button icons
import { getCookie } from '../cookieUtils.js';

const CommunicatePage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [recorder, setRecorder] = useState(null);
  const [dots, setDots] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [showRecordingSection, setShowRecordingSection] = useState(false);
  const [playingAudio, setPlayingAudio] = useState(false);
  const [translatedAudioURL, setTranslatedAudioURL] = useState(''); // URL for translated audio
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

        // Store the audio chunks when recording stops
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

  const handleTranslate = async () => {
    if (audioURL) {
      const audio_response = await fetch(audioURL);
      const audioBlob = await audio_response.blob(); // Get the audio file as a Blob

      const formData = new FormData(); // Create FormData here

      const user_id = getCookie("user_id"); // Corrected cookie retrieval

      formData.append('audio', audioBlob, 'audio.mp3');
      formData.append('user_id', user_id);
      formData.append('language', selectedLanguage);

      // Send audio to backend (example: using fetch)
      const response = await fetch('http://localhost:5000/api/upload_get_translate', {
        method: 'POST',
        body: formData,
      });

      // Check if request was successful
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      const data = await response.json();  // Parse JSON response
      console.log(data)
    //   setTranslatedAudioURL(data.translatedAudioUrl); // Assuming you want to save the translated audio URL
    }
  };

  // Function to handle language selection
  const handleLanguageSelect = (language) => {
    setSelectedLanguage(language);
    setShowRecordingSection(true); // Show the recording section after language selection
  };

  // Function to play the translated audio
  const handlePlayAudio = () => {
    if (translatedAudioURL) {
      const audio = new Audio(translatedAudioURL);
      setPlayingAudio(true);
      audio.play();

      audio.onended = () => {
        setPlayingAudio(false); // Reset when audio finishes
      };
    }
  };

  return (
    <div className="page-container">
      {/* Language Selection */}
      {!selectedLanguage && (
        <>
          <div className="core-text">
            Which language would you like to speak in?
          </div>
          <div className="language-buttons">
            {['EN', 'ES', 'FR'].map((lang) => (
              <button 
                key={lang} 
                className={`language-btn ${selectedLanguage === lang ? 'selected' : ''}`} 
                onClick={() => handleLanguageSelect(lang)}
              >
                {lang}
              </button>
            ))}
          </div>
        </>
      )}

      {/* Show recording section only after a language is selected */}
      {showRecordingSection && (
        <>
          <div className="core-text">
            Let's talk in a different language! In <span className="highlight-bold">English</span>, 
            please record yourself saying what you want to translate.
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
              <button className="action-btn" onClick={toggleRecording}>Record Again</button>
              <button className="action-btn" onClick={handleTranslate}>Translate Audio</button>
            </div>
          )}

          {/* Translated Text Section */}
          {translatedAudioURL && (
            <div className="translated-audio">
              <div className="core-text">
                Translated text with your tone:
              </div>
              <span 
                className={`play-icon ${playingAudio ? 'playing' : ''}`} 
                onClick={handlePlayAudio}
              >
                <FaPlay size={30} />
              </span>
              {playingAudio && <div className="playing-status">Playing{dots}</div>}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default CommunicatePage;
