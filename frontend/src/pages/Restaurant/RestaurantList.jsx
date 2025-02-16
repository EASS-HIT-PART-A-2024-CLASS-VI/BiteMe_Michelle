import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { restaurantService } from '../../services/api';
import { useCart } from '../../context/CartContext';
import './RestaurantList.css';

function RestaurantModal({ restaurant, onClose, onAddToCart }) {
    return (
        <div className="restaurant-modal-overlay">
            <div className="restaurant-modal">
                <div className="modal-header">
                    <h2>{restaurant.name}</h2>
                    <button onClick={onClose} className="close-modal-btn">×</button>
                </div>
                <div className="modal-content">
                    <p>{restaurant.cuisine_type} Cuisine</p>
                    <p>Rating: {restaurant.rating}</p>
                    <p>Address: {restaurant.address}</p>

                    <h3>Menu</h3>
                    <div className="menu-items">
                        {restaurant.menu.map((item) => (
                            <div key={item.name} className="menu-item">
                                <div className="menu-item-details">
                                    <span className="item-name">{item.name}</span>
                                    <span className="item-description">{item.description}</span>
                                    <span className="item-price">${item.price.toFixed(2)}</span>
                                </div>
                                <button
                                    onClick={() => onAddToCart({
                                        id: `${restaurant.id}-${item.name}`,
                                        name: item.name,
                                        price: item.price,
                                        restaurantId: restaurant.id
                                    })}
                                    className="add-to-cart-btn"
                                >
                                    Add to Cart
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

function RestaurantList() {
    const [restaurants, setRestaurants] = useState([]);
    const [loading, setLoading] = useState(true);
    const [selectedRestaurant, setSelectedRestaurant] = useState(null);
    const { addToCart } = useCart();

    useEffect(() => {
        const fetchRestaurants = async () => {
            try {
                const data = await restaurantService.getRestaurants();
                setRestaurants(data);
                setLoading(false);
            } catch (error) {
                console.error('Failed to fetch restaurants', error);
                setLoading(false);
            }
        };

        fetchRestaurants();
    }, []);

    const handleRestaurantClick = (restaurant) => {
        setSelectedRestaurant(restaurant);
    };

    const handleAddToCart = (item) => {
        addToCart(item);
        toast.success(`${item.name} added to cart!`, {
            position: "bottom-right",
            autoClose: 2000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
        });
    };

    if (loading) {
        return <div>Loading restaurants...</div>;
    }

    return (
        <div className="restaurant-list">
            <h1>Restaurants</h1>
            {restaurants.length === 0 ? (
                <p>No restaurants available</p>
            ) : (
                <div className="restaurants-grid">
                    {restaurants.map((restaurant) => (
                        <div
                            key={restaurant.id}
                            className="restaurant-card"
                            onClick={() => handleRestaurantClick(restaurant)}
                        >
                            <h2>{restaurant.name}</h2>
                            <p>{restaurant.cuisine_type}</p>
                            <p>Rating: {restaurant.rating}</p>
                        </div>
                    ))}
                </div>
            )}

            {selectedRestaurant && (
                <RestaurantModal
                    restaurant={selectedRestaurant}
                    onClose={() => setSelectedRestaurant(null)}
                    onAddToCart={handleAddToCart}
                />
            )}
        </div>
    );
}

export default RestaurantList;