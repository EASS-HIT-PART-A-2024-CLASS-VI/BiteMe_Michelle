import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

const BASE_URL = 'http://localhost:8000';
const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    const verifyToken = async (token) => {
        try {
            console.log('Verifying Token:', token);
            const response = await axios.get(`${BASE_URL}/users/me`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });

            console.log('User Verification Response:', response.data);

            const userData = {
                ...response.data,
                isAdmin: response.data.is_admin || false
            };

            console.log('Processed User Data:', userData);

            setUser(userData);
            setIsAuthenticated(true);
            return userData;
        } catch (error) {
            console.error('Token Verification Error:', {
                error: error.message,
                response: error.response?.data
            });
            localStorage.removeItem('token');
            setUser(null);
            setIsAuthenticated(false);
            throw error;
        }
    };

    useEffect(() => {
        const token = localStorage.getItem('token');
        if (token) {
            verifyToken(token)
                .catch(() => localStorage.removeItem('token'))
                .finally(() => setLoading(false));
        } else {
            setLoading(false);
        }
    }, []);

    const login = async (email, password) => {
        try {
            const formData = new FormData();
            formData.append('username', email);
            formData.append('password', password);

            const response = await axios.post(`${BASE_URL}/users/token`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            localStorage.setItem('token', response.data.access_token);

            const userData = await verifyToken(response.data.access_token);

            toast.success('Login successful');
            return userData;
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Login failed');
            throw error;
        }
    };

    const register = async (userData) => {
        try {
            const response = await axios.post(`${BASE_URL}/users/register`, {
                email: userData.email,
                password: userData.password,
                full_name: userData.name || ''
            });
            toast.success('Registration successful');
            return response.data;
        } catch (error) {
            toast.error(error.response?.data?.detail || 'Registration failed');
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        setUser(null);
        setIsAuthenticated(false);
        toast.info('Logged out successfully');
        navigate('/');
    };

    const contextValue = {
        user,
        isAuthenticated,
        loading,
        login,
        register,
        logout
    };

    return (
        <AuthContext.Provider value={contextValue}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};