import React, { useRef } from 'react';
import './pages.css'; // Import the custom styles

const PracticeLangPage = () => {
  const [language, setLanguage] = React.useState('');
  const practiceRef = useRef(null); // Create a ref to scroll to

  const handleLanguageSelect = (lang) => {
    setLanguage(lang);
    // Check if the practiceRef is defined before scrolling
    if (practiceRef.current) {
      practiceRef.current.scrollIntoView({ behavior: 'smooth' });
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
          EN
        </button>
        <button className="language-btn" onClick={() => handleLanguageSelect('French')}>
          FR
        </button>
      </div>

      {/* New text section */}
      {language && (
        <div ref={practiceRef} className="core-text">
          <h3>Alright, let's practice some {language} pronunciation.</h3>
        </div>
      )}
    </div>
  );
};

export default PracticeLangPage;
