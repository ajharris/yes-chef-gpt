import axios from 'axios';

const API_URL = "http://localhost:5000/auth";  // Adjust the base URL if needed

// Log in the user and store the token in localStorage
export const login = async (email, password) => {
    try {
        const response = await axios.post(`${API_URL}/login`, { email, password });
        if (response.data.token) {
            const expirationTime = Date.now() + response.data.expires_in * 1000; // Assuming `expires_in` is in seconds
            localStorage.setItem('authToken', response.data.token);
            localStorage.setItem('tokenExpiration', expirationTime);
            localStorage.setItem('user', JSON.stringify(response.data.user)); 
        }
        return response.data;
    } catch (error) {
        console.error('Login error:', error);
        throw new Error('Login failed. Please check your credentials.');
    }
};

export const isAuthenticated = () => {
    const token = localStorage.getItem('authToken');
    const tokenExpiration = localStorage.getItem('tokenExpiration');
    if (token && tokenExpiration && Date.now() < tokenExpiration) {
        return true;
    }
    return false;
};

export const logout = async () => {
    try {
        await axios.post(`${API_URL}/logout`);
        localStorage.removeItem('authToken');
        localStorage.removeItem('tokenExpiration');
        localStorage.removeItem('user');
    } catch (error) {
        console.error('Logout error:', error);
        throw new Error('Logout failed. Please try again.');
    }
};


// Sign up the user and store the token in localStorage

export const signup = async (email, username, password) => {
    try {
        const response = await axios.post(`${API_URL}/signup`, {
            email,
            username,
            password
        });
        if (response.data.token) {
            localStorage.setItem('authToken', response.data.token);
            localStorage.setItem('user', JSON.stringify(response.data.user));
        }
        return response.data;
    } catch (error) {
        // Log the entire error object for better debugging
        console.error('Signup error:', error.response ? error.response.data : error);
        throw new Error('Signup failed. Please try again.');
    }
};




// Optionally, get the logged-in user data
export const getUser = () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
};
