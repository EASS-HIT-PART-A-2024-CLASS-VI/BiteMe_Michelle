import React, { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-toastify';
import { restaurantService } from '../../services/api';
import { useCart } from '../../context/CartContext';
import { useAuth } from '../../context/AuthContext';
import './RestaurantList.css';
import MenuRecommendations from './MenuRecommendations';



import burgerHeavenLogo from "../../assets/burgerheaven.png";
import pizzaParadiseLogo from "../../assets/pizzaparadise.png";
import sushiMasterLogo from "../../assets/sushimaster.png";
import taqueriaLogo from "../../assets/taqueria.png";
import tandoorLogo from "../../assets/tandoor.jpg";
import goldenLogo from "../../assets/golden.jpeg";
// Base URL for static images
const BASE_URL = 'http://localhost:8000';

// Combine hardcoded logos with dynamic backend images
const restaurantLogos = {
    'Burger Heaven': burgerHeavenLogo,
    'Pizza Paradise': pizzaParadiseLogo,
    'Sushi Master': sushiMasterLogo,
    'Taqueria Deliciosa': taqueriaLogo,
    'Tandoor': tandoorLogo,
    'Golden Dragon': goldenLogo

};

function RestaurantModal({ restaurant, onClose, onAddToCart, isAuthenticated }) {
    if (!restaurant) return null;

    const openLoginModal = () => {
        toast.error('Please login to add items to cart', {
            toastId: 'login-required',
            onClick: () => window.dispatchEvent(new Event('open-login-modal'))
        });
    };

    const restaurantImage =
        (restaurant.image_url
            ? `${BASE_URL}${restaurant.image_url}`
            : restaurantLogos[restaurant.name] || '/api/placeholder/250/250');

    console.log('Restaurant Image URL:', restaurantImage);
    console.log('Restaurant Image URL Details:', {
        baseUrl: BASE_URL,
        imageUrl: restaurant.image_url,
        fullImageUrl: `${BASE_URL}${restaurant.image_url}`
    });

    return (
        <div className="restaurant-modal-overlay">
            <div className="restaurant-modal">
                <div className="modal-header">
                    <h2>{restaurant.name}</h2>
                    <button onClick={onClose} className="close-modal-btn">×</button>
                </div>
                <MenuRecommendations
                    restaurant={restaurant}
                    onAddToCart={onAddToCart}
                />
                <div className="modal-content">
                    <div className="restaurant-modal-image">
                        <img
                            src={restaurantImage}
                            alt={restaurant.name}
                            className="restaurant-logo"
                            onError={(e) => {
                                e.target.src = '/api/placeholder/250/250';
                            }}
                        />
                    </div>
                    <p>{restaurant.cuisine_type} Cuisine</p>
                    <p>Rating: {restaurant.rating}</p>
                    <p>Address: {restaurant.address}</p>

                    <h3>Menu</h3>
                    <div className="menu-items">
                        {restaurant.menu && restaurant.menu.length > 0 ? (
                            restaurant.menu.map((item) => (
                                <div key={item.id || item.name} className="menu-item">
                                    <div className="menu-item-details">
                                        <span className="item-name">{item.name}</span>
                                        <span className="item-description">{item.description}</span>
                                        <div className="item-info">
                                            <span className="item-price">${Number(item.price).toFixed(2)}</span>
                                            {item.spiciness_level && (
                                                <span className={`spiciness-level spiciness-${item.spiciness_level}`}>
                                                     Spiciness: {item.spiciness_level}
                                                </span>
                                            )}
                                            {item.is_vegetarian && (
                                                <span className="menu-item-tag">Vegetarian</span>
                                            )}
                                            {!item.available && (
                                                <span className="menu-item-tag unavailable">Not Available</span>
                                            )}
                                        </div>
                                    </div>
                                    <button
                                        className="add-to-cart-btn"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            if (!isAuthenticated) {
                                                openLoginModal();
                                                return;
                                            }
                                            const cartItem = {
                                                id: `${restaurant.id}-${item.id || item.name}`,
                                                name: item.name,
                                                price: item.price,
                                                restaurantId: restaurant.id,
                                                quantity: 1
                                            };
                                            onAddToCart(cartItem);
                                        }}
                                    >
                                        Add to Cart
                                    </button>
                                </div>
                            ))
                        ) : (
                            <p>No menu items available</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

function RestaurantList() {
    const [restaurants, setRestaurants] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedRestaurant, setSelectedRestaurant] = useState(null);
    const [searchTerm, setSearchTerm] = useState("");
    const [cuisineFilter, setCuisineFilter] = useState("");

    const { addToCart } = useCart();
    const { isAuthenticated } = useAuth();

    useEffect(() => {
        fetchRestaurants();
    }, []);

    const fetchRestaurants = async () => {
        try {
            setLoading(true);
            setError(null);
            const data = await restaurantService.getRestaurants();
            console.log('Restaurant data:', data);
            setRestaurants(Array.isArray(data) ? data : []);
        } catch (error) {
            console.error('Failed to fetch restaurants:', error);
            setError('Failed to load restaurants. Please try again later.');
            toast.error('Failed to load restaurants');
        } finally {
            setLoading(false);
        }
    };

    const handleRestaurantClick = (restaurant) => {
        console.log('Selected Restaurant:', restaurant);
        setSelectedRestaurant(restaurant);
    };

    const handleAddToCart = useCallback((item) => {
        if (!item) return;
        const toastId = `cart-${item.id}`;
        if (!toast.isActive(toastId)) {
            addToCart(item);
            toast.success(`${item.name} added to cart!`, {
                toastId: toastId,
            });
        }
    }, [addToCart]);

    const filteredRestaurants = restaurants.filter((restaurant) =>
        restaurant?.name?.toLowerCase().includes(searchTerm.toLowerCase()) &&
        (cuisineFilter === "" || restaurant?.cuisine_type?.toLowerCase().includes(cuisineFilter.toLowerCase()))
    );

    if (loading) return <div>Loading restaurants...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="restaurant-list">
            <h1>Restaurants</h1>
            <div className="search-filters">
                <input
                    type="text"
                    placeholder="🔍 Search by name"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="search-input"
                />
                <input
                    type="text"
                    placeholder="🍽️ Search by cuisine"
                    value={cuisineFilter}
                    onChange={(e) => setCuisineFilter(e.target.value)}
                    className="search-input"
                />
            </div>

            {filteredRestaurants.length === 0 ? (
                <p className="no-restaurants">
                    {searchTerm || cuisineFilter
                        ? "No restaurants match your search criteria"
                        : "No restaurants available"}
                </p>
            ) : (
                <div className="restaurants-grid">
                    {filteredRestaurants.map((restaurant) => {
                        // Prioritize backend image, fallback to hardcoded logo, then placeholder
                        const restaurantImage =
                            (restaurant.image_url ? `${BASE_URL}${restaurant.image_url}` : null) ||
                            restaurantLogos[restaurant.name] ||
                            '/api/placeholder/250/250';

                        return (
                            <div
                                key={restaurant.id}
                                className="restaurant-card"
                                onClick={() => handleRestaurantClick(restaurant)}
                            >
                                <div className="restaurant-image">
                                    <img
                                        src={restaurantImage}
                                        alt={restaurant.name}
                                        className="restaurant-logo"
                                        onError={(e) => {
                                            e.target.src = '/api/placeholder/250/250';
                                        }}
                                    />
                                </div>
                                <h2>{restaurant.name}</h2>
                                <p>{restaurant.cuisine_type}</p>
                                <p>⭐ Rating: {restaurant.rating}</p>
                                <p>{restaurant.address}</p>
                            </div>
                        );
                    })}
                </div>
            )}

            {selectedRestaurant && (
                <RestaurantModal
                    restaurant={selectedRestaurant}
                    onClose={() => setSelectedRestaurant(null)}
                    onAddToCart={handleAddToCart}
                    isAuthenticated={isAuthenticated}
                />
            )}
        </div>
    );
}

export default RestaurantList;