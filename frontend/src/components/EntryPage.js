// src/components/EntryPage.js

import React from 'react';
import { useNavigate } from 'react-router-dom';

function EntryPage() {
    const navigate = useNavigate();

    const handleLogin = () => {
        navigate('/login');
    };

    const handleSignup = () => {
        navigate('/signup');
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '100px' }}>
            <h1>Welcome to YesChefGPT</h1>
            <p>Your personal AI-powered kitchen assistant is here to help you make delicious meals.</p>
            <div style={{ marginTop: '20px' }}>
                <button
                    onClick={handleLogin}
                    style={{
                        padding: '10px 20px',
                        marginRight: '10px',
                        cursor: 'pointer',
                        fontSize: '16px',
                    }}
                >
                    Log In
                </button>
                <button
                    onClick={handleSignup}
                    style={{
                        padding: '10px 20px',
                        marginLeft: '10px',
                        cursor: 'pointer',
                        fontSize: '16px',
                    }}
                >
                    Sign Up
                </button>
            </div>
        </div>
    );
}

export default EntryPage;
