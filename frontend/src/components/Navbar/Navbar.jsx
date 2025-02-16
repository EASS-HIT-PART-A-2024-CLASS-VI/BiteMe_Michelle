import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Navbar.css';

function Navbar({ setShowLogin }) {
    const { isAuthenticated, logout } = useAuth();

    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <Link to="/">BiteMe</Link>
            </div>
            <div className="navbar-menu">
                <Link to="/">Home</Link>
                <Link to="/restaurants">Restaurants</Link>
                {isAuthenticated && (
                    <>
                        <Link to="/orders">Orders</Link>
                        <Link to="/cart">Cart</Link>
                        <Link to="/profile">Profile</Link>
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
