import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import RecipePromptPage from './components/RecipePromptPage';  // Import RecipePromptPage
import Home from './components/Home';
import About from './components/About';
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <Navbar />
        <RecipePromptPage />  {/* Replace PromptInput and ChatResponse with RecipePromptPage */}
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/" element={<Home />} />  {/* Default Route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
