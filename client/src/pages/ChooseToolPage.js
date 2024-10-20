import React from 'react';
import { useNavigate } from 'react-router-dom';
import './pages.css'; // Import the custom styles

const ChooseToolPage = () => {
    const navigate = useNavigate();

    const selectCommunicate = () => {
        navigate('/communicate');
    }; 

    const selectPractice = () => {
        navigate('/practicelang');
    }; 

    return (
        <div className="page-container">
        <div className="core-text">
            Awesome! Now for  the fun part. What do you want to use <span className="highlight-bold"> SpeakEasy</span> for? 
            <br />
            <br />
        </div>
        <div className="actions">
            <button className="action-btn" onClick={selectCommunicate}>Communicate With Foreigners</button>
            <button className="action-btn" onClick={selectPractice}>Practice Pronunciation</button>
        </div>
        </div>
    );
};

export default ChooseToolPage;
