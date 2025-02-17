import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';

// Components
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import LoginPopup from './components/LoginPopup/LoginPopup';

// Pages
import Home from './pages/Home/Home';
import RestaurantList from './pages/Restaurant/RestaurantList';
import OrderList from './pages/Orders/OrderList';
import Profile from './pages/Profile/Profile';
import Cart from './pages/Cart/Cart';

function App() {
    const [showLogin, setShowLogin] = useState(false);
    const { isAuthenticated } = useAuth();

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

            <div className="content">
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/restaurants" element={<RestaurantList />} />

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
                </Routes>
            </div>

            <Footer />
        </div>
    );
}

export default App;