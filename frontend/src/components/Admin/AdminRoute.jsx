import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const AdminRoute = ({ children }) => {
    const { user, isAuthenticated, loading } = useAuth();

    console.log('AdminRoute Debug:');
    console.log('User:', user);
    console.log('Is Authenticated:', isAuthenticated);
    console.log('Is Admin:', user?.isAdmin);
    console.log('Loading:', loading);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!isAuthenticated || !user?.isAdmin) {
        console.log('Access Denied - Redirecting to Home');
        return <Navigate to="/" />;
    }

    return children;
};

export default AdminRoute;