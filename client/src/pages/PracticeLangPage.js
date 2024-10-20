import React, { useRef, useState } from 'react';
import { getCookie } from '../cookieUtils.js'; // Assuming you have a utility to get cookies
import { FaMicrophone } from 'react-icons/fa'; // Import microphone icon
import './pages.css'; // Import the custom styles

const PracticeLangPage = () => {
  const [language, setLanguage] = useState('');
  const [langCode, setLangCode] = useState('');
  const [foreignphrase, setFPhrase] = useState('');
  const [englishphrase, setEPhrase] = useState('');
  const [exampleAudioUrl, setExAudioUrl] = useState('');
  const [isVisible, setIsVisible] = useState(true);
  const [audioUrl, setAudioUrl] = useState('');
  const [feedback, setFeedback] = useState('');
  const [exAudioPlayed, setExAudioPlayed] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const practiceRef = useRef(null); // Create a ref to scroll to
  const [recorder, setRecorder] = useState(null);

  const handleLanguageSelect = async (lang) => {
    setLanguage(lang);
    const newLangCode = lang === 'Spanish' ? 'es' : 'fr'; // Set langCode for use later
    setLangCode(newLangCode);

    // Fetch the phrase and audio clip from the backend
    try {
      const formData = new FormData();
      formData.append('language', newLangCode); // Use newLangCode immediately

      console.log("getting next phrase");
      const response = await fetch('http://localhost:5000/api/nextphrase', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setFPhrase(data.phrase); // Assuming the API response contains a 'phrase'
      setEPhrase(data.phrase_en);
      console.log("retrieved next phrase");

      // After setting the phrases, we can call the next fetch
      await fetchExampleSpeech(newLangCode, data.phrase); // Call new function to fetch example audio

      // Check if the practiceRef is defined before scrolling
      if (practiceRef.current) {
        practiceRef.current.scrollIntoView({ behavior: 'smooth' });
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // Function to fetch example speech using the updated foreignphrase
  const fetchExampleSpeech = async (langCode, foreignphrase) => {
    const formData2 = new FormData();
    const user_id = getCookie("user_id"); // Corrected cookie retrieval
    formData2.append('user_id', user_id);
    formData2.append('language', langCode);
    formData2.append('words', foreignphrase); // Use the latest foreignphrase

    console.log("getting example speech");
    const speak_response = await fetch('http://localhost:5000/api/speak', {
      method: 'POST',
      body: formData2,
    });

    const AudioBlob = await speak_response.blob();  // Get the audio as a Blob
    const AudioURL = URL.createObjectURL(AudioBlob);  // Create an object URL
    setExAudioUrl(AudioURL);  // Set the URL so it can be played
    console.log(AudioURL);
    console.log("retrieved example speech");
  };

  const handlePlayAudio = () => {
    if (exampleAudioUrl) {
      const audio = new Audio(exampleAudioUrl);
      audio.play();
      setExAudioPlayed(true);
    }
  };

  // Start or stop recording
  const toggleRecording = async () => {
    if (isRecording) {
      // Stop recording
      recorder.stop();

      const audio_response = await fetch(audioUrl);
      const audioBlob = await audio_response.blob(); // Get the audio file as a Blob
      const formData = new FormData();
      formData.append('audio', audioBlob, 'audio.mp3');

      const response = await fetch('http://localhost:5000/api/upload_get_feedback', {
        method: 'POST',
        body: formData,
      });

      setFeedback(await response.json()); // Await the response.json()
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
          setAudioUrl(audioUrl); // Store the URL to play back
        };
        mediaRecorder.start();
        setIsRecording(true);
      } else {
        recorder.start();
        setIsRecording(true);
      }
    }
  };

  return (
    <div className="page-container">
      {/* Conditional rendering for the language selection prompt */}
      {!language && (
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
      )}

      {/* New text section that appears after a language is selected */}
      {language && (
        <div ref={practiceRef} className="core-text">
          {exampleAudioUrl && (
            <div>
              <h3>Alright, let's practice some {language} pronunciation.</h3>
              Try to say "{englishphrase}" in {language}: <br /> {foreignphrase}
              <br />
              <span>Here's how you should sound: </span>
              <button className="play-button" onClick={handlePlayAudio}>Play</button>
            </div>
          )}
          {exAudioPlayed && (
            <div>
              Now it's your turn:
              <b></b>
              Click the microphone icon to start recording:
              <span className={`mic-icon ${isRecording ? 'recording' : ''}`} onClick={toggleRecording}>
                <FaMicrophone size={30} />
              </span>
            </div>
          )}
          {audioUrl && !isRecording && (
            <div>
              Here's how you did: {feedback}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PracticeLangPage;
