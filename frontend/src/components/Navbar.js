import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAuthenticated, logout } from '../services/authService';

function Navbar() {
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logout();
            navigate('/login');  // Redirect after successful logout
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <div className="navbar">
            <nav>
                <Link to="/home" className="nav-link">Home</Link>
                <Link to="/about" className="nav-link">About</Link>
                {isAuthenticated() ? (
                    <>
                        <Link to="/profile" className="nav-link">Profile</Link>
                        <Link to="/recipe-prompt" className="nav-link">Get a Recipe</Link> {/* New Recipe Prompt Link */}
                        <button onClick={handleLogout} className="nav-button">Logout</button>
                    </>
                ) : (
                    <>
                        <Link to="/login" className="nav-link">Login</Link>
                        <Link to="/signup" className="nav-link">Signup</Link>
                    </>
                )}
            </nav>
        </div>
    );
}

export default Navbar;
