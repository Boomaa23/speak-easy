// src/components/HomeButton.js

import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomeButton = () => {
  const navigate = useNavigate();

  // Function to handle the home button click
  const handleHomeClick = () => {
    navigate('/choosetool'); // Update this path as needed for routing
  };

  return (
    <button
      style={{
        fontSize: '1.5rem',
        padding: '10px 20px',
        backgroundColor: 'var(--tertiary-color)',
        color: 'var(--primary-color)',
        border: 'none',
        borderRadius: '10px',
        cursor: 'pointer',
        transition: 'background-color 0.3s, color 0.3s, transform 0.2s',
        position: 'absolute', // Positioning the button absolutely
        top: '20px', // Adjust as needed for vertical spacing
        left: '20px', // Adjust as needed for horizontal spacing
        zIndex: 1000, // Ensures it stays on top of other elements
      }}
      onClick={handleHomeClick}
      onMouseEnter={(e) => {
        e.currentTarget.style.backgroundColor = 'var(--primary-color)';
        e.currentTarget.style.color = 'var(--secondary-color)';
        e.currentTarget.style.transform = 'scale(1.1)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.backgroundColor = 'var(--tertiary-color)';
        e.currentTarget.style.color = 'var(--primary-color)';
        e.currentTarget.style.transform = 'scale(1)';
      }}
    >
      Home
    </button>
  );
};

export default HomeButton;



/* import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomeButton = () => {
  const navigate = useNavigate();

  const handleHomeClick = () => {
    navigate('/choosetool');
  };

  return (
    <button
      onClick={handleHomeClick}
      style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        padding: '10px 20px',
        backgroundColor: '#2c2213', 
        color: '#e6d6c3', 
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontSize: '16px',
        zIndex: 1000, // Ensure it is on top of other elements
      }}
    >
      Home
    </button>
  );
}; */

