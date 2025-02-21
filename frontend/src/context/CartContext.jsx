import React, { createContext, useState, useContext, useEffect } from 'react';
import { toast } from 'react-toastify';
import { useAuth } from './AuthContext';


const CartContext = createContext(null);

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState([]);
  const { isAuthenticated } = useAuth();

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
    if (isAuthenticated && cartItems.length > 0) {
      localStorage.setItem('cart', JSON.stringify(cartItems));
    }
  }, [cartItems, isAuthenticated]);


  const addToCart = (item) => {
    if (!isAuthenticated) {
      toast.error('Please login to add items to cart', {
        toastId: 'login-required', // Unique ID to prevent duplicates
        onClick: () => window.dispatchEvent(new Event('open-login-modal'))
      });
      return false;
    }

    // Use a unique identifier for preventing duplicate additions
    const existingItemIndex = cartItems.findIndex(cartItem => cartItem.id === item.id);

    if (existingItemIndex > -1) {
      // Item already exists, update quantity
      const updatedCartItems = [...cartItems];
      updatedCartItems[existingItemIndex].quantity += item.quantity || 1;

      setCartItems(updatedCartItems);

      // Only show toast if it's a new addition
      if (item.quantity === 1) {
        toast.success(`${item.name} added to cart`, {
          toastId: `cart-${item.id}`, // Unique ID
        });
      }

      return true;
    }

    // New item
    setCartItems(prevCart => [...prevCart, { ...item, quantity: item.quantity || 1 }]);

    toast.success(`${item.name} added to cart`, {
      toastId: `cart-${item.id}`, // Unique ID
    });

    return true;
  };


  const removeFromCart = (itemId) => {
    setCartItems((prevCart) => prevCart.filter(item => item.id !== itemId));
  };

  const updateQuantity = (itemId, newQuantity) => {
    setCartItems((prevCart) =>
        newQuantity <= 0
            ? prevCart.filter(item => item.id !== itemId)
            : prevCart.map(item =>
                item.id === itemId ? { ...item, quantity: newQuantity } : item
            )
    );
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
