import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { clearCookies } from '../cookieUtils.js';
import './pages.css';

const WelcomePage = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const handleKeyPress = (event) => {
      // Navigate to the Home page on any key press
      navigate('/traininginput');
    };

    // Add keydown event listener
    window.addEventListener('keydown', handleKeyPress);

    // Cleanup the event listener on unmount
    return () => {
      window.removeEventListener('keydown', handleKeyPress);
    };
  }, [navigate]);

  return (
    <div className="page-container">
      <div className="core-text">
        Welcome to <span className="highlight-bold">SpeakEasy</span>! We'll help you{' '}
        <span className="hover-highlight">perfect your pronunciation of foreign languages</span> and{' '}
        <span className="hover-highlight">communicate with locals in foreign countries</span>.
        <br />
        <br />
        Press any key to get started
        <br />
        <br />
            {/* Button to clear cookies */}
            <button onClick={clearCookies} className="clear-cookies-button">
          Clear Cookies
        </button>
      </div>
    </div>
  );
};

export default WelcomePage;