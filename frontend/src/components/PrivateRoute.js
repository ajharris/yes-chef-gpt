// src/components/PrivateRoute.js

import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from '../services/authService';

function PrivateRoute({ element: Component, ...rest }) {
    return (
        <Route
            {...rest}
            element={isAuthenticated() ? <Component {...rest} /> : <Navigate to="/login" />}
        />
    );
}

export default PrivateRoute;
