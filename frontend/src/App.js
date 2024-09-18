import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import RecipePromptPage from './components/RecipePromptPage';  // Import RecipePromptPage
import Home from './components/Home';
import About from './components/About';
import Signup from './components/Signup';  // Import Signup component
import Login from './components/Login';    // Import Login component
import './App.css';

function App() {
  return (
    <Router>
      <div>
        <Navbar />
        <Routes>
          <Route path="/home" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/signup" element={<Signup />} />  {/* Signup route */}
          <Route path="/login" element={<Login />} />    {/* Login route */}
          <Route path="/recipe-prompt" element={<RecipePromptPage />} />  {/* Recipe Prompt Query route */}
          <Route path="/" element={<Home />} />  {/* Default Route */}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
