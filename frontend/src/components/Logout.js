// frontend/src/components/Logout.js
import React, { useEffect } from 'react';
import authService from '../services/authService';

const Logout = () => {
  useEffect(() => {
    authService.logout();
    window.location.href = '/login';  // Redirect to login after logout
  }, []);

  return <div>Logging out...</div>;
};

export default Logout;
