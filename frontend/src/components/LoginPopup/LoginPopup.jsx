import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { Mail, Lock, User, Phone, X } from 'lucide-react';
import './LoginPopup.css';

function LoginPopup({ setShowLogin }) {
    const [isLogin, setIsLogin] = useState(true);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [phone, setPhone] = useState('');

    const { login, register } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            if (isLogin) {
                await login(email, password);
            } else {
                await register({
                    email,
                    password,
                    name,
                    phone
                });
                setIsLogin(true);
            }
            setShowLogin(false);
        } catch (error) {
            console.error('Authentication error', error);
        }
    };

    return (
        <div className="login-popup" onClick={(e) => {
            if (e.target === e.currentTarget) setShowLogin(false);
        }}>
            <div className="login-popup-content">
                <h2>{isLogin ? 'Welcome Back!' : 'Create Account'}</h2>
                <form onSubmit={handleSubmit}>
                    {!isLogin && (
                        <>
                            <div className="input-group">
                                <input
                                    type="text"
                                    placeholder="Full Name"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                    required
                                />
                            </div>
                            <div className="input-group">
                                <input
                                    type="tel"
                                    placeholder="Phone Number (Optional)"
                                    value={phone}
                                    onChange={(e) => setPhone(e.target.value)}
                                />
                            </div>
                        </>
                    )}
                    <div className="input-group">
                        <input
                            type="email"
                            placeholder="Email Address"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="submit-btn">
                        {isLogin ? 'Sign In' : 'Create Account'}
                    </button>
                </form>

                <p
                    onClick={() => setIsLogin(!isLogin)}
                    className="toggle-login"
                >
                    {isLogin
                        ? "Don't have an account? Sign Up"
                        : 'Already have an account? Sign In'}
                </p>

                <button
                    className="close-btn"
                    onClick={() => setShowLogin(false)}
                >
                    Close
                </button>
            </div>
        </div>
    );
}

export default LoginPopup;