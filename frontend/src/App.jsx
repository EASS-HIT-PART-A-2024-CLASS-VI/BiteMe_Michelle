import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

// Components
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import LoginPopup from './components/LoginPopup/LoginPopup';
import AdminRoute from './components/Admin/AdminRoute';

// Pages
import Home from './pages/Home/Home';
import RestaurantList from './pages/Restaurant/RestaurantList';
import OrderList from './pages/Orders/OrderList';
import Profile from './pages/Profile/Profile';
import Cart from './pages/Cart/Cart';
import AdminDashboard from './components/Admin/AdminDashboard';

// Styles
import './App.css';

function App() {
    console.log("App component rendering");
    const [showLogin, setShowLogin] = useState(false);
    const { isAuthenticated, user } = useAuth();

    // Handle global login modal trigger
    useEffect(() => {
        const openLoginModal = () => {
            setShowLogin(true);
        };

        window.addEventListener('open-login-modal', openLoginModal);

        // Cleanup event listener
        return () => {
            window.removeEventListener('open-login-modal', openLoginModal);
        };
    }, []);

    return (
        <div className="app">
            {showLogin && <LoginPopup setShowLogin={setShowLogin} />}

            <Navbar setShowLogin={setShowLogin} />

            <div className="main-content">
                <Routes>
                    {/* Public Routes */}
                    <Route path="/" element={<Home />} />
                    <Route path="/restaurants" element={<RestaurantList />} />

                    {/* Protected Routes */}
                    <Route
                        path="/orders"
                        element={isAuthenticated ? <OrderList /> : <Navigate to="/" />}
                    />
                    <Route
                        path="/profile"
                        element={isAuthenticated ? <Profile /> : <Navigate to="/" />}
                    />
                    <Route
                        path="/cart"
                        element={isAuthenticated ? <Cart /> : <Navigate to="/" />}
                    />

                    {/* Admin Routes */}
                    <Route
                        path="/admin-dashboard"  // Ensure this matches exactly
                        element={
                            <AdminRoute>
                                <AdminDashboard />
                            </AdminRoute>
                        }
                    />
                    <Route
                        path="/admin/restaurants"
                        element={
                            <AdminRoute>
                                <AdminDashboard />
                            </AdminRoute>
                        }
                    />

                    {/* Catch-all route for 404 */}
                    <Route
                        path="*"
                        element={
                            <div className="not-found">
                                <h1>404: Page Not Found</h1>
                                <p>The page you're looking for doesn't exist.</p>
                            </div>
                        }
                    />
                </Routes>
            </div>

            {/* Show admin menu item only for admin users */}
            {isAuthenticated && user?.is_admin && (
                <div className="admin-indicator">
                    Admin Mode
                </div>
            )}

            <Footer />
        </div>
    );
}

export default App;