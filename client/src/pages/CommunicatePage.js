import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './pages.css'; // Import the custom styles
import { FaMicrophone, FaPlay } from 'react-icons/fa'; // Import microphone and play button icons

const CommunicatePage = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [recorder, setRecorder] = useState(null);
  const [dots, setDots] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [showLanguageSelection, setShowLanguageSelection] = useState(false);
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

        mediaRecorder.onstop = () => {
          const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
          const audioUrl = URL.createObjectURL(audioBlob);
          setAudioURL(audioUrl); // Store the URL to play back

          // Send the audio to backend and get translated audio
          fetch('your-backend-endpoint', {
            method: 'POST',
            body: audioBlob,
            headers: {
              'Content-Type': 'audio/mp3',
            },
          })
          .then(response => response.json())
          .then(data => {
            setTranslatedAudioURL(data.translatedAudioUrl); // Get the translated audio URL
          });
        };

        mediaRecorder.start();
        setIsRecording(true);
      } else {
        recorder.start();
        setIsRecording(true);
      }
    }
  };

  // Function to handle language selection
  const handleLanguageSelect = (language) => {
    setSelectedLanguage(language);
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

  // Function to show language selection after "Done" is pressed
  const handleDone = () => {
    setShowLanguageSelection(true);
  };

  return (
    <div className="page-container">
      <div className="core-text">
        Let's talk in another language! In your <span className="highlight-bold">native language</span>, 
        record yourself saying what you want to translate.
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
          <button className="action-btn done-btn" onClick={handleDone}>Done</button>
        </div>
      )}

      {/* Language Selection */}
      {showLanguageSelection && (
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
                disabled={selectedLanguage} // Disable if a language is already selected
              >
                {lang}
              </button>
            ))}
          </div>

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
