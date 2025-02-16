import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
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
        <div className="login-popup">
            <div className="login-popup-content">
                <h2>{isLogin ? 'Login' : 'Register'}</h2>
                <form onSubmit={handleSubmit}>
                    {!isLogin && (
                        <>
                            <input
                                type="text"
                                placeholder="Name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                            />
                            <input
                                type="tel"
                                placeholder="Phone (Optional)"
                                value={phone}
                                onChange={(e) => setPhone(e.target.value)}
                            />
                        </>
                    )}
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button type="submit">
                        {isLogin ? 'Login' : 'Register'}
                    </button>
                </form>
                <p
                    onClick={() => setIsLogin(!isLogin)}
                    className="toggle-login"
                >
                    {isLogin
                        ? 'Need an account? Register'
                        : 'Already have an account? Login'}
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