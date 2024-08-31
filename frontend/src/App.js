// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginAbout from './components/LoginAbout';
import Signup from './components/Signup';
import Logout from './components/Logout';
import PrivateRoute from './components/PrivateRoute';
import Home from './components/Home';
import TestConnection from './components/TestConnection';

function App() {
    const testConnection = async () => {
        try {
            const response = await fetch('/api/server-info');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    };

    return (
        <Router>
            <div className="App">
                <h1>Welcome to YesChefGPT</h1>
                <TestConnection testConnection={testConnection} />
                <Routes>
                    <Route path="/login" element={<LoginAbout />} />
                    <Route path="/signup" element={<Signup />} />
                    <Route path="/logout" element={<Logout />} />
                    <PrivateRoute path="/home" element={<Home />} />
                    <Route path="/" element={<LoginAbout />} /> {/* Default route */}
                </Routes>
            </div>
        </Router>
    );
}

export default App;
