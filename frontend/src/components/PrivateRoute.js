// src/components/PrivateRoute.js

import React from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../services/authService';  // Assume this checks if the user is authenticated

function PrivateRoute({ element: Component }) {
    return isAuthenticated() ? <Component /> : <Navigate to="/login" />;
}

export default PrivateRoute;
