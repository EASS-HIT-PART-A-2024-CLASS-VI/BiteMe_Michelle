import React, { createContext, useState, useContext, useEffect } from 'react';
import { toast } from 'react-toastify';
import { useAuth } from './AuthContext';

const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const { isAuthenticated, user } = useAuth();

  // Load cart from localStorage when authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const savedCart = localStorage.getItem('cart');
      if (savedCart) {
        setCartItems(JSON.parse(savedCart));
      }
    } else {
      // Clear cart when logged out
      setCartItems([]);
      localStorage.removeItem('cart');
    }
  }, [isAuthenticated]);

  // Save cart to localStorage whenever it changes
  useEffect(() => {
    if (isAuthenticated) {
      localStorage.setItem('cart', JSON.stringify(cartItems));
    }
  }, [cartItems, isAuthenticated]);

  const addToCart = (item) => {
    // Check if user is authenticated
    if (!isAuthenticated) {
      toast.error('Please login to add items to cart', {
        onClick: () => {
          // You might want to create a global method to open login modal
          window.dispatchEvent(new Event('open-login-modal'));
        }
      });
      return false;
    }

    // Check if item already exists in cart
    const existingItemIndex = cartItems.findIndex(
        cartItem => cartItem.id === item.id
    );

    if (existingItemIndex > -1) {
      // If item exists, increase quantity
      const updatedCart = [...cartItems];
      updatedCart[existingItemIndex].quantity += item.quantity || 1;
      setCartItems(updatedCart);
    } else {
      // If item doesn't exist, add new item
      setCartItems([...cartItems, {
        ...item,
        quantity: item.quantity || 1
      }]);
    }

    toast.success(`${item.name} added to cart`);
    return true;
  };

  const removeFromCart = (itemId) => {
    setCartItems(cartItems.filter(item => item.id !== itemId));
  };

  const updateQuantity = (itemId, newQuantity) => {
    if (newQuantity <= 0) {
      // Remove item if quantity is 0 or less
      removeFromCart(itemId);
    } else {
      const updatedCart = cartItems.map(item =>
          item.id === itemId
              ? { ...item, quantity: newQuantity }
              : item
      );
      setCartItems(updatedCart);
    }
  };

  const clearCart = () => {
    setCartItems([]);
    localStorage.removeItem('cart');
  };

  const calculateTotal = () => {
    return cartItems.reduce(
        (total, item) => total + (item.price * item.quantity),
        0
    );
  };

  return (
      <CartContext.Provider value={{
        cartItems,
        addToCart,
        removeFromCart,
        updateQuantity,
        clearCart,
        calculateTotal
      }}>
        {children}
      </CartContext.Provider>
  );
};

// Custom hook to use the CartContext
export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};