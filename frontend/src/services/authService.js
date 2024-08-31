// src/services/authService.js

import axios from 'axios';

const API_URL = "http://localhost:5000"; // Adjust the URL according to your backend

export const login = async (email, password) => {
    const response = await axios.post(`${API_URL}/login`, { email, password });
    return response.data;
};

export const signup = async (email, username, password) => {
    const response = await axios.post(`${API_URL}/signup`, { email, username, password });
    return response.data;
};

export const logout = async () => {
    await axios.get(`${API_URL}/logout`);
};

export const isAuthenticated = () => {
    // Implement your logic to check if the user is authenticated
    return !!localStorage.getItem('user');
};
