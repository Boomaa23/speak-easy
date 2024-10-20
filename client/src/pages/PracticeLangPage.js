import React, { useRef, useState, useEffect } from 'react';
import './pages.css'; // Import the custom styles

const PracticeLangPage = () => {
  const [language, setLanguage] = useState('');
  const [phrase, setPhrase] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const practiceRef = useRef(null); // Create a ref to scroll to

  const handleLanguageSelect = async (lang) => {
    setLanguage(lang);

    // Fetch the phrase and audio clip from the backend
    try {
      const response = await fetch(`your-backend-endpoint/${lang}`); // Adjust the endpoint as needed
      const data = await response.json();
      setPhrase(data.phrase); // Assuming the API response contains a 'phrase'
      setAudioUrl(data.audioUrl); // Assuming the API response contains an 'audioUrl'
      
      // Check if the practiceRef is defined before scrolling
      if (practiceRef.current) {
        practiceRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  const handlePlayAudio = () => {
    if (audioUrl) {
      const audio = new Audio(audioUrl);
      audio.play();
    }
  };

  return (
    <div className="page-container">
      <div className="core-text">
        Cool, let's practice some pronunciation! What language are you trying to learn?
        <br />
        <br />
        {/* Language buttons */}
        <button className="language-btn" onClick={() => handleLanguageSelect('Spanish')}>
          ES
        </button>
        <button className="language-btn" onClick={() => handleLanguageSelect('French')}>
          FR
        </button>
      </div>

      {/* New text section */}
      {language && (
        <div ref={practiceRef} className="core-text">
          <h3>Alright, let's practice some {language} pronunciation.</h3>
          <p>{phrase}</p>
          {audioUrl && (
            <div>
              <span>Here's how you should sound: </span>
              <button className="play-button" onClick={handlePlayAudio}>Play</button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PracticeLangPage;
