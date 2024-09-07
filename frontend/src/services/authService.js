import axios from 'axios';

const API_URL = "http://localhost:5000"; // Adjust the URL according to your backend

// Log in the user and store the token in localStorage
export const login = async (email, password) => {
    try {
        const response = await axios.post(`${API_URL}/login`, { email, password });
        if (response.data.token) {
            localStorage.setItem('authToken', response.data.token); // Save token to localStorage
            localStorage.setItem('user', JSON.stringify(response.data.user)); // Save user data (optional)
        }
        return response.data;
    } catch (error) {
        console.error('Login error:', error); // Log the error for debugging
        throw new Error('Login failed. Please check your credentials.');
    }
};

// Sign up the user and store the token in localStorage
export const signup = async (email, username, password) => {
    try {
        const response = await axios.post(`${API_URL}/signup`, { email, username, password });
        if (response.data.token) {
            localStorage.setItem('authToken', response.data.token); // Save token to localStorage
            localStorage.setItem('user', JSON.stringify(response.data.user)); // Save user data (optional)
        }
        return response.data;
    } catch (error) {
        console.error('Signup error:', error); // Log the error for debugging
        throw new Error('Signup failed. Please try again.');
    }
};

// Log out the user and clear localStorage
export const logout = async () => {
    try {
        await axios.post(`${API_URL}/logout`); // Adjust this if your API requires POST for logout
        localStorage.removeItem('authToken'); // Clear token from localStorage
        localStorage.removeItem('user'); // Clear user data
    } catch (error) {
        console.error('Logout error:', error); // Log the error for debugging
        throw new Error('Logout failed. Please try again.');
    }
};

// Check if the user is authenticated
export const isAuthenticated = () => {
    // Check if there's a valid token in localStorage
    const token = localStorage.getItem('authToken');
    return !!token; // Returns true if token exists, false otherwise
};

// Optionally, get the logged-in user data
export const getUser = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
};
