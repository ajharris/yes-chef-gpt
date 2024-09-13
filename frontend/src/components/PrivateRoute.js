// frontend/src/components/PrivateRoute.js
import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import authService from '../services/authService';

const PrivateRoute = ({ component: Component, ...rest }) => (
  <Route
    {...rest}
    render={(props) =>
      authService.getCurrentUser() ? <Component {...props} /> : <Navigate to="/login" />
    }
  />
);

export default PrivateRoute;
