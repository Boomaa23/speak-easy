import React, { useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import WelcomePage from './pages/WelcomePage'; 
import TraningInputPage from './pages/TrainingInputPage'; 
import ChooseToolPage from './pages/ChooseToolPage';
import CommunicatePage from './pages/CommunicatePage';
import PracticeLangPage from './pages/PracticeLangPage';

const RoutesComponent = () => {
  return (
    <Routes>
      <Route path="/" element={<WelcomePage />} />
      <Route path="/traininginput" element={<TraningInputPage />} />
      <Route path="/choosetool" element={<ChooseToolPage />} />
      <Route path="/communicate" element={<CommunicatePage />} />
      <Route path="/practicelang" element={<PracticeLangPage />} />
    </Routes>
  );
};

export default RoutesComponent;
