import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

// Base URL for your backend
const BASE_URL = 'http://localhost:8000';

// Define interfaces for type safety
interface AuthHeaders {
  Authorization?: string;
}

interface LoginData {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  name?: string;
  phone?: string;
}

interface UpdateProfileData {
  name?: string;
  phone?: string;
  password?: string;
}

interface OrderData {
  items: any[];
  total_price: number;
  special_instructions?: string;
}

// Helper function to get auth headers
const getAuthHeaders = (): AuthHeaders => {
  const token = localStorage.getItem('token');
  return token
      ? { Authorization: `Bearer ${token}` }
      : {};
};

// Authentication services
export const authService = {
  async login(email: string, password: string) {
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

  async register(userData: RegisterData) {
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

  async updateProfile(userData: UpdateProfileData) {
    const updateData: any = {};

    if (userData.name) {
      updateData.full_name = userData.name;
    }

    if (userData.phone) {
      updateData.phone_number = userData.phone;
    }

    if (userData.password) {
      updateData.password = userData.password;
    }

    console.log('Sending update data:', updateData);

    const response = await axios.put(`${BASE_URL}/users/me`, updateData, {
      headers: {
        ...getAuthHeaders(),
        'Content-Type': 'application/json'
      }
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
      console.error('Failed to fetch orders', error);
      return [];
    }
  },

  async createOrder(orderData: OrderData) {
    const completeOrderData = {
      id: uuidv4(),
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
      const response = await axios.post(`${BASE_URL}/orders/`, completeOrderData, {
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json'
        }
      });

      return response.data;
    } catch (error) {
      console.error('Order creation failed', error);
      throw error;
    }
  }
};

// Cart-related services
export const cartService = {
  saveCart(cartItems: any[]) {
    localStorage.setItem('cart', JSON.stringify(cartItems));
  },

  getCart(): any[] {
    const savedCart = localStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : [];
  },

  clearCart() {
    localStorage.removeItem('cart');
  }
};

export default {
  auth: authService,
  user: userService,
  restaurant: restaurantService,
  order: orderService,
  cart: cartService
};