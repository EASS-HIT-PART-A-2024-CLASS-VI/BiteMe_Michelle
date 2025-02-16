import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

// Base URL for your backend
const BASE_URL = 'http://localhost:8000';

// Helper function to get auth headers
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return token
      ? { Authorization: `Bearer ${token}` }
      : {};
};

// Authentication services
export const authService = {
  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);

    const response = await axios.post(`${BASE_URL}/users/token`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },

  async register(userData) {
    const response = await axios.post(`${BASE_URL}/users/register`, {
      email: userData.email,
      password: userData.password,
      full_name: userData.name,
      phone_number: userData.phone || null
    });
    return response.data;
  }
};

// User-related services
export const userService = {
  async getProfile() {
    const response = await axios.get(`${BASE_URL}/users/me`, {
      headers: getAuthHeaders()
    });
    return response.data;
  },

  async updateProfile(userData) {
    const response = await axios.put(`${BASE_URL}/users/me`, userData, {
      headers: getAuthHeaders()
    });
    return response.data;
  }
};

// Restaurant-related services
export const restaurantService = {
  async getRestaurants(filters = {}) {
    const response = await axios.get(`${BASE_URL}/restaurants/`, {
      params: filters
    });
    return response.data;
  },

  async getRestaurantById(restaurantId) {
    const response = await axios.get(`${BASE_URL}/restaurants/${restaurantId}`);
    return response.data;
  }
};

// Order-related services
export const orderService = {
  async getOrders() {
    try {
      const response = await axios.get(`${BASE_URL}/orders/`, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error) {
      console.error('Failed to fetch orders from backend', error);

      // If backend fails, return empty array instead of local storage
      return [];
    }
  },

  async createOrder(orderData) {
    // Simulate payment processing
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Prepare comprehensive order data
    const completeOrderData = {
      id: uuidv4(), // Generate unique order ID using UUID
      items: orderData.items,
      total_price: orderData.total_price,
      status: 'PENDING',
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      payment_method: 'credit_card',
      special_instructions: orderData.special_instructions || '',
      restaurant_id: orderData.items[0]?.restaurant_id || null
    };

    try {
      // Attempt to create order via backend
      const response = await axios.post(`${BASE_URL}/orders/`, completeOrderData, {
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json'
        }
      });

      // Return the created order
      return response.data;
    } catch (error) {
      console.error('Backend order creation failed', error);

      // Rethrow the error to be handled by the caller
      throw error;
    }
  },

  async getOrderById(orderId) {
    try {
      const response = await axios.get(`${BASE_URL}/orders/${orderId}`, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch order ${orderId}`, error);
      return null;
    }
  }
};

// Cart-related services (optional, for persistent cart)
export const cartService = {
  saveCart(cartItems) {
    localStorage.setItem('cart', JSON.stringify(cartItems));
  },

  getCart() {
    const savedCart = localStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : [];
  },

  clearCart() {
    localStorage.removeItem('cart');
  }
};

// Export a unified API object
export default {
  auth: authService,
  user: userService,
  restaurant: restaurantService,
  order: orderService,
  cart: cartService
};