import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaMicrophone, FaPlay, FaSpinner } from 'react-icons/fa'; // Import spinner icon
import { getCookie } from '../cookieUtils.js';
import './pages.css';
import HomeButton from '../components/HomeButton';

const CommunicatePage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [recorder, setRecorder] = useState(null);
  const [hintText, setHintText] = useState('');
  const [showHint, setShowHint] = useState(false);
  const [playingAudio, setPlayingAudio] = useState(false);
  const [translatedAudioURL, setTranslatedAudioURL] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [showRecordingSection, setShowRecordingSection] = useState(false);
  const [loading, setLoading] = useState(false); // State to manage loading
  const navigate = useNavigate();

  // Start recording 1 second after the component mounts
  useEffect(() => {
    if (showRecordingSection) {
      const timeout = setTimeout(() => startRecording(), 1000);
      return () => clearTimeout(timeout);
    }
  }, [showRecordingSection]);

  // Display hint text after 5 seconds of recording
  useEffect(() => {
    let hintTimeout;
    if (isRecording) {
      setShowHint(false);
      hintTimeout = setTimeout(() => {
        setHintText('Stop Recording');
        setShowHint(true);
      }, 5000);
    } else {
      setHintText('Start Recording');
      setShowHint(true);
    }

    return () => clearTimeout(hintTimeout);
  }, [isRecording]);

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
    };

    mediaRecorder.start();
    setIsRecording(true);
  };

  const toggleRecording = () => {
    if (isRecording) {
      recorder.stop();
      setIsRecording(false);
    } else {
      startRecording();
    }
  };

  const handleLanguageSelect = (language) => {
    setSelectedLanguage(language);
    setShowRecordingSection(true);
  };

  const handlePlayAudio = () => {
    if (translatedAudioURL) {
      const audio = new Audio(translatedAudioURL);
      setPlayingAudio(true);
      audio.play();
      audio.onended = () => setPlayingAudio(false);
    }
  };

  const handleTranslate = async () => {
    if (audioURL) {
      setLoading(true); // Set loading to true when starting translation
      const audioResponse = await fetch(audioURL);
      const audioBlob = await audioResponse.blob();
      const formData = new FormData();
      const userId = getCookie('user_id');
      formData.append('audio', audioBlob, 'audio.mp3');
      formData.append('user_id', userId);
      formData.append('language', selectedLanguage);

      const response = await fetch('http://localhost:5000/api/upload_get_translate', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error(`Error: ${response.statusText}`);

      const translatedAudioBlob = await response.blob();
      const translatedAudioURL = URL.createObjectURL(translatedAudioBlob);
      setTranslatedAudioURL(translatedAudioURL);
      setLoading(false); // Set loading to false when translation is complete
    }
  };

  return (
    <div className="page-container">
      <HomeButton />
      {!selectedLanguage && (
        <>
          <div className="core-text">Which language would you like to speak in?</div>
          <div className="language-buttons">
            {['ES', 'FR'].map((lang) => (
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

      {showRecordingSection && (
        <>
          <div className="core-text">
            Let's talk! Record yourself saying what you want to translate. <br />
          </div>

          <div className="mic-container1">
            <span className="hint-text">{hintText}</span> 
            <div
              className={`mic-icon1 ${isRecording ? 'recording' : ''}`}
              onClick={toggleRecording}
            >
              <FaMicrophone size={80} />
            </div>
          </div>

          {audioURL && !isRecording && (
            <div className="actions">
              <button className="action-btn" onClick={handleTranslate}>
                Translate Audio
              </button>
              {loading && (
                <div className="loading-icon">
                  <FaSpinner className="spinner" />
                </div>
              )}
            </div>
          )}

          {translatedAudioURL && (
            <div className="translated-audio">
              <div className="core-text">Click the Play button below to hear your translated voice!</div>
              <div className="actions">
                <div className="play-button-wrapper">
                  <span className={`play-icon ${playingAudio ? 'playing' : ''}`} onClick={handlePlayAudio}>
                    <FaPlay />
                  </span>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default CommunicatePage;
