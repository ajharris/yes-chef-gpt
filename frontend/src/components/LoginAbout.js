// src/components/LoginAbout.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../services/authService';

function LoginAbout() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(email, password);
            navigate('/home'); // Redirect to home page after successful login
        } catch (error) {
            alert("Login failed. Please check your credentials.");
        }
    };

    return (
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '20px' }}>
            <div style={{ flex: 1, padding: '20px' }}>
                <h2>About YesChefGPT</h2>
                <p>
                    YesChefGPT is your personal AI-powered kitchen assistant, helping you make the most of the ingredients you have at home. Whether you want to find a recipe for tonight's dinner or just need some inspiration, YesChefGPT has you covered.
                </p>
                <p>
                    By simply entering what ingredients you have, YesChefGPT will suggest delicious recipes tailored to your preferences. We are committed to promoting healthy eating habits and making your cooking experience enjoyable and stress-free.
                </p>
            </div>
            <div style={{ flex: 1, padding: '20px', borderLeft: '1px solid #ccc' }}>
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                        style={{ display: 'block', width: '100%', marginBottom: '10px', padding: '10px' }}
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ display: 'block', width: '100%', marginBottom: '10px', padding: '10px' }}
                    />
                    <button type="submit" style={{ padding: '10px 20px', cursor: 'pointer' }}>Login</button>
                </form>
            </div>
        </div>
    );
}

export default LoginAbout;
