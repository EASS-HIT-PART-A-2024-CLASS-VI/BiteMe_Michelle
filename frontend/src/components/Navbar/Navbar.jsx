import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Navbar.css';
import logo from '../../assets/biteme_logo.gif'; // Adjusted import path

function Navbar({ setShowLogin }) {
    const { isAuthenticated, logout, user } = useAuth();

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/">
                    <img src={logo} alt="BiteMe Logo" className="navbar-logo" />
                </Link>
            </div>
            <div className="navbar-menu">
                <Link to="/">Home</Link>
                <Link to="/restaurants">Restaurants</Link>
                {isAuthenticated && (
                    <>
                        <Link to="/orders">Orders</Link>
                        <Link to="/cart">Cart</Link>
                        <Link to="/profile">Profile</Link>

                        {/* Admin Dashboard Link */}

                        {user?.is_admin && ( // Changed from isAdmin to is_admin
                            <Link to="/admin-dashboard">Admin Dashboard</Link>
                        )}
                    </>
                )}
            </div>
            <div className="navbar-auth">
                {isAuthenticated ? (
                    <button onClick={logout}>Logout</button>
                ) : (
                    <button onClick={() => setShowLogin(true)}>Login</button>
                )}
            </div>
        </nav>
    );
}

export default Navbar;
