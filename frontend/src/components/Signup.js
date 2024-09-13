// frontend/src/components/Signup.js
import React, { useState } from 'react';
import authService from '../services/authService'

const Signup = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      await authService.signup(email, username, password);
      setMessage('Signup successful! You can now log in.');
    } catch (error) {
      setMessage('Error during signup');
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" required />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
      <button type="submit">Signup</button>
      <p>{message}</p>
    </form>
  );
};

export default Signup;
