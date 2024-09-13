// frontend/src/components/Login.js
import React, { useState } from 'react';
import authService from '../services/authService';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await authService.login(email, password);
      setMessage('Login successful!');
      window.location.href = '/';  // Redirect after login
    } catch (error) {
      setMessage('Error during login');
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
      <button type="submit">Login</button>
      <p>{message}</p>
    </form>
  );
};

export default Login;
