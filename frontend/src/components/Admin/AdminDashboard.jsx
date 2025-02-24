import React, { useState, useEffect } from 'react';
import { restaurantService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';
import './AdminDashboard.css';

const BASE_URL = 'http://localhost:8000';

const AdminDashboard = () => {
    const { user, isAuthenticated } = useAuth();
    const [restaurants, setRestaurants] = useState([]);
    const [selectedRestaurant, setSelectedRestaurant] = useState(null);
    const [loading, setLoading] = useState(true);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);
    const [isAddMenuItemModalOpen, setIsAddMenuItemModalOpen] = useState(false);

    const [restaurantForm, setRestaurantForm] = useState({
        name: '',
        cuisine_type: '',
        rating: 0,
        address: '',
        description: '',
        image: null
    });

    const [menuItemForm, setMenuItemForm] = useState({
        name: '',
        description: '',
        price: '',
        category: 'Main Course',
        spiciness_level: 1,
        is_vegetarian: false,
        available: true
    });


    useEffect(() => {
        if (!isAuthenticated || !user?.isAdmin) {
            toast.error('Unauthorized access');
            return;
        }
        fetchRestaurants();
    }, [isAuthenticated, user]);

    const fetchRestaurants = async () => {
        try {
            setLoading(true);
            const response = await restaurantService.getRestaurants();
            setRestaurants(response);
        } catch (error) {
            console.error('Error fetching restaurants:', error);
            toast.error('Failed to load restaurants');
        } finally {
            setLoading(false);
        }
    };

    // In AdminDashboard.jsx

    const handleAddRestaurant = async (e) => {
        e.preventDefault();
        try {
            // Validate required fields
            if (!restaurantForm.name || !restaurantForm.cuisine_type || !restaurantForm.address || !restaurantForm.image) {
                toast.error('Name, cuisine type, address, and image are required');
                return;
            }

            // Create FormData object
            const formData = new FormData();
            formData.append('name', restaurantForm.name);
            formData.append('cuisine_type', restaurantForm.cuisine_type);
            formData.append('rating', restaurantForm.rating.toString());
            formData.append('address', restaurantForm.address);
            formData.append('description', restaurantForm.description || '');
            formData.append('image', restaurantForm.image);

            // Call the API
            const response = await restaurantService.createRestaurantWithImage(formData);

            // Update local state
            setRestaurants(prevRestaurants => [...prevRestaurants, response.restaurant]);

            // Reset form and close modal
            setIsAddModalOpen(false);
            resetRestaurantForm();

            // Show success message
            toast.success('Restaurant added successfully');

            // Refresh the restaurants list
            fetchRestaurants();
        } catch (error) {
            console.error('Error adding restaurant:', error);
            toast.error(error.response?.data?.detail || 'Failed to add restaurant');
        }
    };

    const handleUpdateRestaurant = async (e) => {
        e.preventDefault();
        if (!selectedRestaurant) return;

        try {
            const formData = new FormData();
            formData.append('name', restaurantForm.name);
            formData.append('cuisine_type', restaurantForm.cuisine_type);
            formData.append('rating', restaurantForm.rating.toString());
            formData.append('address', restaurantForm.address);
            formData.append('description', restaurantForm.description || '');
            if (restaurantForm.image) {
                formData.append('image', restaurantForm.image);
            }

            const response = await restaurantService.updateRestaurant(
                selectedRestaurant.id,
                formData
            );

            setRestaurants(prevRestaurants =>
                prevRestaurants.map(rest =>
                    rest.id === selectedRestaurant.id ? response : rest
                )
            );

            setIsEditModalOpen(false);
            resetRestaurantForm();
            toast.success('Restaurant updated successfully');
        } catch (error) {
            console.error('Error updating restaurant:', error);
            toast.error(error.response?.data?.detail || 'Failed to update restaurant');
        }
    };

    const handleEditClick = (restaurant) => {
        setSelectedRestaurant(restaurant);
        setRestaurantForm({
            name: restaurant.name || '',
            cuisine_type: restaurant.cuisine_type || '',
            rating: restaurant.rating || 0,
            address: restaurant.address || '',
            description: restaurant.description || '',
            image: null,
            image_url: restaurant.image_url || ''
        });
        setIsEditModalOpen(true);
    };

    const handleAddMenuItem = async (e) => {
        e.preventDefault();
        if (!selectedRestaurant) return;

        try {
            // Validate required fields
            if (!menuItemForm.name || !menuItemForm.description || !menuItemForm.price) {
                toast.error('Name, description, and price are required');
                return;
            }

            const response = await restaurantService.addMenuItem(
                selectedRestaurant.id,
                {
                    name: menuItemForm.name,
                    description: menuItemForm.description,
                    price: parseFloat(menuItemForm.price),
                    category: menuItemForm.category,
                    spiciness_level: parseInt(menuItemForm.spiciness_level),
                    is_vegetarian: Boolean(menuItemForm.is_vegetarian),
                    available: Boolean(menuItemForm.available)
                }
            );

            // Update the restaurants list to include the new menu item
            setRestaurants(prevRestaurants =>
                prevRestaurants.map(rest =>
                    rest.id === selectedRestaurant.id
                        ? {
                            ...rest,
                            menu: [...(rest.menu || []), response.menu_item]
                        }
                        : rest
                )
            );

            // Close modal and reset form
            setIsAddMenuItemModalOpen(false);
            resetMenuItemForm();
            toast.success('Menu item added successfully');
        } catch (error) {
            console.error('Error adding menu item:', error);
            toast.error(error.response?.data?.detail || 'Failed to add menu item');
        }
    };

    const handleDeleteMenuItem = async (restaurantId, menuItemName) => {
        if (!window.confirm(`Are you sure you want to delete "${menuItemName}"?`)) return;

        try {
            await restaurantService.deleteMenuItem(restaurantId, menuItemName);
            setRestaurants(prevRestaurants =>
                prevRestaurants.map(rest => {
                    if (rest.id === restaurantId) {
                        return {
                            ...rest,
                            menu: rest.menu.filter(item => item.name !== menuItemName)
                        };
                    }
                    return rest;
                })
            );
            toast.success(`${menuItemName} deleted successfully`);
        } catch (error) {
            console.error('Delete Menu Item Error:', error);
            toast.error(error.response?.data?.detail || 'Failed to delete menu item');
        }
    };

    const handleDeleteRestaurant = async (restaurantId) => {
        if (!window.confirm('Are you sure you want to delete this restaurant?')) return;

        try {
            await restaurantService.deleteRestaurant(restaurantId);
            setRestaurants(prevRestaurants =>
                prevRestaurants.filter(rest => rest.id !== restaurantId)
            );
            toast.success('Restaurant deleted successfully');
        } catch (error) {
            console.error('Error deleting restaurant:', error);
            toast.error(error.response?.data?.detail || 'Failed to delete restaurant');
        }
    };

    const resetRestaurantForm = () => {
        setRestaurantForm({
            name: '',
            cuisine_type: '',
            rating: 0,
            address: '',
            description: '',
            image: null
        });
    };

    const resetMenuItemForm = () => {
        setMenuItemForm({
            name: '',
            description: '',
            price: '',
            category: 'Main Course',
            spiciness_level: 1,
            is_vegetarian: false,
            available: true
        });
    };

    if (loading) {
        return <div className="loading-spinner">Loading...</div>;
    }

    return (
        <div className="admin-dashboard">
            <div className="admin-header">
                <h1 className="admin-title">Restaurant Management</h1>
                <button
                    className="admin-button admin-button-primary"
                    onClick={() => setIsAddModalOpen(true)}
                >
                    Add New Restaurant
                </button>
            </div>

            <div className="admin-content">
                {restaurants.map(restaurant => (
                    <div key={restaurant.id} className="restaurant-card">
                        <div className="restaurant-header">
                            <h2 className="restaurant-name">{restaurant.name}</h2>
                            <div className="admin-actions">
                                <button
                                    className="admin-button admin-button-primary"
                                    onClick={() => {
                                        setSelectedRestaurant(restaurant);
                                        setRestaurantForm({
                                            name: restaurant.name,
                                            cuisine_type: restaurant.cuisine_type,
                                            rating: restaurant.rating,
                                            address: restaurant.address,
                                            description: restaurant.description,
                                        });
                                        setIsEditModalOpen(true);
                                    }}
                                >
                                    Edit
                                </button>
                                <button
                                    className="admin-button admin-button-danger"
                                    onClick={() => handleDeleteRestaurant(restaurant.id)}
                                >
                                    Delete
                                </button>
                                <button
                                    className="admin-button admin-button-primary"
                                    onClick={() => {
                                        setSelectedRestaurant(restaurant);
                                        setIsAddMenuItemModalOpen(true);
                                    }}
                                >
                                    Add Menu Item
                                </button>
                            </div>
                        </div>



                        <div className="restaurant-details">
                            <p className="restaurant-info">
                                <strong>Cuisine:</strong> {restaurant.cuisine_type}
                            </p>
                            <p className="restaurant-info">
                                <strong>Rating:</strong> {restaurant.rating}
                            </p>
                            <p className="restaurant-info">
                                <strong>Address:</strong> {restaurant.address}
                            </p>
                            {restaurant.description && (
                                <p className="restaurant-info">
                                    <strong>Description:</strong> {restaurant.description}
                                </p>
                            )}
                        </div>

                        <div className="menu-items">
                            <h3>Menu Items</h3>
                            {restaurant.menu?.length > 0 ? (
                                restaurant.menu.map(item => (
                                    <div key={item.id || item.name} className="menu-item">
                                        <div className="menu-item-details">
                                            <div className="menu-item-info">
                                                <span className="menu-item-name">{item.name}</span>
                                                <span className="menu-item-price">
                                                    ${parseFloat(item.price).toFixed(2)}
                                                </span>
                                                <span className={`spiciness-level spiciness-${item.spiciness_level}`}>
                                                    Spiciness: {item.spiciness_level}
                                                </span>
                                            </div>
                                            {item.description && (
                                                <p className="menu-item-description">{item.description}</p>
                                            )}
                                            <div className="menu-item-tags">
                                                {item.is_vegetarian && (
                                                    <span className="menu-item-tag">Vegetarian</span>
                                                )}
                                                {!item.available && (
                                                    <span className="menu-item-tag unavailable">
                                                        Not Available
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                        <button
                                            className="admin-button admin-button-danger"
                                            onClick={() => handleDeleteMenuItem(restaurant.id, item.name)}
                                        >
                                            Delete
                                        </button>
                                    </div>
                                ))
                            ) : (
                                <p className="empty-menu-message">No menu items yet</p>
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Add Restaurant Modal */}
            {isAddModalOpen && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h2 className="modal-title">Add New Restaurant</h2>
                        </div>
                        <form onSubmit={handleAddRestaurant}>
                            <div className="form-group">
                                <label htmlFor="restaurant-name">Restaurant Name</label>
                                <input
                                    id="restaurant-name"
                                    type="text"
                                    value={restaurantForm.name}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        name: e.target.value
                                    })}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="cuisine-type">Cuisine Type</label>
                                <select
                                    id="cuisine-type"
                                    value={restaurantForm.cuisine_type}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        cuisine_type: e.target.value
                                    })}
                                    required
                                >
                                    <option value="">Select Cuisine Type</option>
                                    <option value="Italian">Italian</option>
                                    <option value="Japanese">Japanese</option>
                                    <option value="Mexican">Mexican</option>
                                    <option value="Indian">Indian</option>
                                    <option value="American">American</option>
                                    <option value="Chinese">Chinese</option>
                                </select>
                            </div>

                            <div className="form-group">
                                <label htmlFor="rating">Rating</label>
                                <input
                                    id="rating"
                                    type="number"
                                    min="0"
                                    max="5"
                                    step="0.1"
                                    value={restaurantForm.rating}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        rating: e.target.value
                                    })}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label htmlFor="address">Address</label>
                                <input
                                    id="address"
                                    type="text"
                                    value={restaurantForm.address}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        address: e.target.value
                                    })}
                                    required
                                />
                            </div>



                            {/* Description */}
                            <div className="form-group">
                                <label htmlFor="description">Description</label>
                                <textarea
                                    id="description"
                                    value={restaurantForm.description}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        description: e.target.value
                                    })}
                                />
                            </div>

                            {/* Image Upload */}
                            <div className="form-group">
                                <label htmlFor="restaurant-image">Restaurant Image</label>
                                <input
                                    id="restaurant-image"
                                    type="file"
                                    accept="image/*"
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        image: e.target.files[0]
                                    })}
                                />
                                {restaurantForm.image && (
                                    <div className="image-preview">
                                        <p>Selected: {restaurantForm.image.name}</p>
                                    </div>
                                )}
                            </div>

                            {/* Display Existing Image */}
                            {restaurantForm.image_url && (
                                <div className="restaurant-image">
                                    <img
                                        src={`${BASE_URL}${restaurantForm.image_url}`}
                                        alt={`${restaurantForm.name}`}
                                        className="restaurant-thumbnail"
                                    />
                                </div>
                            )}

                            {/* Form Actions */}
                            <div className="form-actions">
                                <button type="submit" className="admin-button admin-button-primary">
                                    Add Restaurant
                                </button>
                                <button
                                    type="button"
                                    className="admin-button"
                                    onClick={() => setIsAddModalOpen(false)}
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Edit Restaurant Modal */}
            {isEditModalOpen && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h2 className="modal-title">Edit Restaurant</h2>
                        </div>
                        <form onSubmit={handleUpdateRestaurant}>
                            <div className="form-group">
                                <label>Restaurant Name</label>
                                <input
                                    type="text"
                                    value={restaurantForm.name}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        name: e.target.value
                                    })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Cuisine Type</label>
                                <select
                                    value={restaurantForm.cuisine_type}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        cuisine_type: e.target.value
                                    })}
                                    required
                                >
                                    <option value="">Select Cuisine Type</option>
                                    <option value="Italian">Italian</option>
                                    <option value="Japanese">Japanese</option>
                                    <option value="Mexican">Mexican</option>
                                    <option value="Indian">Indian</option>
                                    <option value="American">American</option>
                                    <option value="Chinese">Chinese</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label>Rating</label>
                                <input
                                    type="number"
                                    min="0"
                                    max="5"
                                    step="0.1"
                                    value={restaurantForm.rating}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        rating: e.target.value
                                    })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Address</label>
                                <input
                                    type="text"
                                    value={restaurantForm.address}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        address: e.target.value
                                    })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Description</label>
                                <textarea
                                    value={restaurantForm.description}
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        description: e.target.value
                                    })}
                                />
                            </div>
                            <div className="form-group">
                                <label>Restaurant Image</label>
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={(e) => setRestaurantForm({
                                        ...restaurantForm,
                                        image: e.target.files[0]
                                    })}
                                />
                                {restaurantForm.image && (
                                    <div className="image-preview">
                                        <p>Selected: {restaurantForm.image.name}</p>
                                    </div>
                                )}
                            </div>

                            <div className="form-actions">
                                <button type="submit" className="admin-button admin-button-primary">
                                    Update Restaurant
                                </button>
                                <button
                                    type="button"
                                    className="admin-button"
                                    onClick={() => setIsEditModalOpen(false)}
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* Add Menu Item Modal */}
            {isAddMenuItemModalOpen && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h2 className="modal-title">Add Menu Item</h2>
                        </div>
                        <form onSubmit={handleAddMenuItem}>
                            <div className="form-group">
                                <label>Item Name</label>
                                <input
                                    type="text"
                                    value={menuItemForm.name}
                                    onChange={(e) => setMenuItemForm({
                                        ...menuItemForm,
                                        name: e.target.value
                                    })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Description</label>
                                <textarea
                                    value={menuItemForm.description}
                                    onChange={(e) => setMenuItemForm({
                                        ...menuItemForm,
                                        description: e.target.value
                                    })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Price</label>
                                <input
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    value={menuItemForm.price}
                                    onChange={(e) => setMenuItemForm({
                                        ...menuItemForm,
                                        price: e.target.value
                                    })}
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <label>Category</label>
                                <select
                                    value={menuItemForm.category}
                                    onChange={(e) => setMenuItemForm({
                                        ...menuItemForm,
                                        category: e.target.value
                                    })}
                                    required
                                >
                                    <option value="">Select Category</option>
                                    <option value="Appetizer">Appetizer</option>
                                    <option value="Main Course">Main Course</option>
                                    <option value="Dessert">Dessert</option>
                                    <option value="Beverage">Beverage</option>
                                </select>
                            </div>
                            {/* Add this inside the form in the Add Menu Item Modal */}
                            <div className="form-group">
                                <label>Spiciness Level</label>
                                <select
                                    value={menuItemForm.spiciness_level}
                                    onChange={(e) => setMenuItemForm({
                                        ...menuItemForm,
                                        spiciness_level: parseInt(e.target.value)
                                    })}
                                    required
                                >
                                    <option value="1">1 (Mild)</option>
                                    <option value="2">2</option>
                                    <option value="3">3 (Medium)</option>
                                    <option value="4">4</option>
                                    <option value="5">5 (Very Spicy)</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label className="checkbox-label">
                                    <input
                                        type="checkbox"
                                        checked={menuItemForm.is_vegetarian}
                                        onChange={(e) => setMenuItemForm({
                                            ...menuItemForm,
                                            is_vegetarian: e.target.checked
                                        })}
                                    />
                                    Vegetarian
                                </label>
                            </div>

                            <div className="form-actions">
                                <button type="submit" className="admin-button admin-button-primary">
                                    Add Item
                                </button>
                                <button
                                    type="button"
                                    className="admin-button"
                                    onClick={() => setIsAddMenuItemModalOpen(false)}
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
};
export default AdminDashboard;