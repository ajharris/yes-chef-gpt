// src/components/Logout.js

import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { logout } from '../services/authService';

function Logout() {
    const navigate = useNavigate();

    useEffect(() => {
        const performLogout = async () => {
            await logout();
            navigate('/login'); // Redirect to login page after logout
        };
        performLogout();
    }, [navigate]);

    return <div>Logging out...</div>;
}

export default Logout;
