// src/App.js

import React from 'react';
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
        <div className="App">
            <h1>Welcome to YesChefGPT</h1>
            <TestConnection testConnection={testConnection} />
        </div>
    );
}

export default App;
