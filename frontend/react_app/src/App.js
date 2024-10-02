import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import FormPage from './pages/formPage';
import ResponsePage from './pages/responsePage';
import 'bootstrap/dist/css/bootstrap.min.css';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FormPage />} />
        <Route path="/response" element={<ResponsePage />} />
      </Routes>
    </Router>
  );
}

export default App;
