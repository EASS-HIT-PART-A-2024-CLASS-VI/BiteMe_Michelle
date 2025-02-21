import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

const BASE_URL = 'http://localhost:8000';

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

interface RestaurantData {
  name: string;
  address: string;
  cuisine_type?: string;
  rating?: number;
  description?: string;
}

interface MenuItemData {
  name: string;
  description: string;
  price: number;
  category?: string;
  spiciness_level?: number;
  is_vegetarian?: boolean;
  available?: boolean;
}

// Ensure getAuthHeaders returns a valid object even when no token exists
const getAuthHeaders = () => {
  const token = localStorage.getItem('token');
  return {
    Authorization: token ? `Bearer ${token}` : '',
    'Content-Type': 'application/json'
  };
};

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

export const userService = {
  async getProfile() {
    try {
      const response = await axios.get(`${BASE_URL}/users/me`, {
        headers: getAuthHeaders()
      });
      console.log('Profile Response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Failed to fetch profile:', error);
      throw error;
    }
  },

  async updateProfile(userData: UpdateProfileData) {
    try {
      const updateData: any = {
        full_name: userData.name,
        phone_number: userData.phone
      };

      if (userData.password) {
        updateData.password = userData.password;
      }

      console.log('Sending to backend:', updateData);

      const response = await axios.put(`${BASE_URL}/users/me`, updateData, {
        headers: getAuthHeaders()
      });

      console.log('Response from backend:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Failed to update profile:', error);
      throw error;
    }
  }
};

// Restaurant-related services
export const restaurantService = {
  // In api.ts, add to restaurantService
  async createRestaurantWithImage(formData: FormData) {
    try {
      console.log('Creating restaurant with image...');
      const token = localStorage.getItem('token');

      // Log the FormData contents for debugging
      for (let [key, value] of formData.entries()) {
        console.log(`${key}:`, value);
      }

      const response = await axios.post(
          `${BASE_URL}/restaurants/add`,  // This matches the FastAPI route
          formData,
          {
            headers: {
              'Authorization': token ? `Bearer ${token}` : '',
            }
          }
      );

      console.log('Restaurant creation response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Restaurant Creation Error:', error.response?.data || error);
      throw error;
    }
  },

  async getRestaurants() {
    try {
      const response = await axios.get(`${BASE_URL}/restaurants/`, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error: any) {
      console.error('Failed to fetch restaurants:', error);
      throw error;
    }


  },

  async createRestaurant(restaurantData: RestaurantData) {
    try {
      console.log('Restaurant Creation Request:', restaurantData);

      // Ensure all required fields are present with proper types
      const completeRestaurantData = {
        name: restaurantData.name,
        cuisine_type: restaurantData.cuisine_type,
        rating: parseFloat(restaurantData.rating?.toString() || '0'),
        address: restaurantData.address,
        description: restaurantData.description || '',
        menu: [] // Always start with an empty menu
      };

      // Use the properly constructed endpoint with trailing slash
      const response = await axios.post(
          `${BASE_URL}/restaurants/add`,
          completeRestaurantData,
          {
            headers: getAuthHeaders()
          }
      );

      console.log('Restaurant Creation Response:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Restaurant Creation Error:', error.response?.data || error.message);
      throw error;
    }
  },

  async updateRestaurant(restaurantId: string, formData: FormData) {
    try {
      const token = localStorage.getItem('token');
      console.log('Updating restaurant:', { restaurantId, formData });

      const response = await axios.put(
          `${BASE_URL}/restaurants/${restaurantId}`,
          formData,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          }
      );

      console.log('Restaurant updated successfully:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error updating restaurant:', error);
      throw error;
    }
  },

  async deleteMenuItem(restaurantId: string, menuItemName: string) {
    try {
      console.log('Delete Menu Item Request:', {
        url: `${BASE_URL}/restaurants/${restaurantId}/menu/${encodeURIComponent(menuItemName)}`,
        restaurantId,
        menuItemName,
        headers: getAuthHeaders()
      });

      if (!menuItemName) {
        throw new Error('Menu item name is required');
      }

      const response = await axios.delete(
          `${BASE_URL}/restaurants/${restaurantId}/menu/${encodeURIComponent(menuItemName)}`,
          {
            headers: getAuthHeaders()
          }
      );

      console.log('Delete Menu Item Response:', {
        status: response.status,
        data: response.data
      });

      return response.data;
    } catch (error: any) {
      console.error('Delete Menu Item Complete Error:', {
        errorName: error.name,
        errorMessage: error.message,
        errorResponse: error.response?.data,
        errorStatus: error.response?.status
      });
      throw error;
    }
  },

  async deleteRestaurant(restaurantId: string) {
    try {
      console.log('Delete Restaurant - Restaurant ID:', restaurantId);
      const response = await axios.delete(`${BASE_URL}/restaurants/${restaurantId}`, {
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error: any) {
      console.error('Error deleting restaurant:', error.response?.data || error.message);
      throw error;
    }
  },
  async addMenuItem(restaurantId: string, menuItemData: any) {
    try {
      const token = localStorage.getItem('token');
      console.log('Adding menu item:', { restaurantId, menuItemData });

      // Create FormData
      const formData = new FormData();
      formData.append('name', menuItemData.name);
      formData.append('description', menuItemData.description);
      formData.append('price', menuItemData.price.toString());
      formData.append('category', menuItemData.category);
      formData.append('spiciness_level', menuItemData.spiciness_level?.toString() || '1');
      formData.append('is_vegetarian', menuItemData.is_vegetarian?.toString() || 'false');
      formData.append('available', menuItemData.available?.toString() || 'true');

      const response = await axios.post(
          `${BASE_URL}/restaurants/${restaurantId}/add-item`,
          formData,
          {
            headers: {
              'Authorization': `Bearer ${token}`,
            }
          }
      );

      console.log('Menu item added successfully:', response.data);
      return response.data;
    } catch (error: any) {
      console.error('Error adding menu item:', error);
      throw error;
    }
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
    } catch (error: any) {
      console.error('Failed to fetch orders:', error);
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
        headers: getAuthHeaders()
      });
      return response.data;
    } catch (error: any) {
      console.error('Order creation failed:', error.response?.data || error.message);
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