// src/components/Navbar.js

import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAuthenticated, logout } from '../services/authService';

function Navbar() {
    const navigate = useNavigate();

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    return (
        <nav style={{ padding: '10px', borderBottom: '1px solid #ccc' }}>
            <Link to="/home" style={{ marginRight: '15px' }}>Home</Link>
            <Link to="/about" style={{ marginRight: '15px' }}>About</Link>
            {isAuthenticated() ? (
                <>
                    <Link to="/profile" style={{ marginRight: '15px' }}>Profile</Link>
                    <button onClick={handleLogout} style={{ marginRight: '15px' }}>Logout</button>
                </>
            ) : (
                <>
                    <Link to="/login" style={{ marginRight: '15px' }}>Login</Link>
                    <Link to="/signup" style={{ marginRight: '15px' }}>Signup</Link>
                </>
            )}
        </nav>
    );
}

export default Navbar;
