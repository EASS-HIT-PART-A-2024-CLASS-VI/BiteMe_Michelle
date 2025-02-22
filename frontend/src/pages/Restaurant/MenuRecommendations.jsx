import React, { useState, useEffect } from 'react';
import { orderService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const MenuRecommendations = ({ restaurant, onAddToCart }) => {
    const [recommendations, setRecommendations] = useState(null);
    const [loading, setLoading] = useState(true);
    const { user } = useAuth();

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                // Get user's order history
                let orderHistory = [];
                try {
                    const orders = await orderService.getOrders();
                    // Extract all previously ordered items
                    orderHistory = orders.flatMap(order =>
                        order.items.map(item => item.name)
                    );
                    // Remove duplicates
                    orderHistory = [...new Set(orderHistory)];
                } catch (error) {
                    console.log('No previous orders found');
                }

                // Get recommendations from the service
                const response = await fetch('http://localhost:8001/recommend/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        restaurant_menu: restaurant.menu.map(item => ({
                            name: item.name,
                            price: item.price,
                            description: item.description,
                            category: item.category
                        })),
                        user_previous_orders: orderHistory
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to fetch recommendations');
                }

                const data = await response.json();
                setRecommendations(data);
            } catch (error) {
                console.error('Error fetching recommendations:', error);
            } finally {
                setLoading(false);
            }
        };

        if (restaurant?.menu?.length > 0) {
            fetchRecommendations();
        }
    }, [restaurant]);

    if (loading) {
        return <div className="p-4">Loading recommendations...</div>;
    }

    if (!recommendations) {
        return null;
    }

    return (
        <div className="bg-white rounded-lg shadow p-6 mb-6">
            <h3 className="text-xl font-bold mb-4">Recommended for You</h3>
            <div className="space-y-4">
                {recommendations.recommended_items.map((itemName, index) => {
                    const menuItem = restaurant.menu.find(
                        item => item.name.toLowerCase() === itemName.toLowerCase()
                    );

                    if (!menuItem) return null;

                    return (
                        <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded hover:bg-gray-100 transition-colors">
                            <div>
                                <h4 className="font-semibold">{menuItem.name}</h4>
                                <p className="text-sm text-gray-600">${menuItem.price.toFixed(2)}</p>
                                {menuItem.description && (
                                    <p className="text-sm text-gray-500">{menuItem.description}</p>
                                )}
                            </div>
                            <button
                                onClick={() => onAddToCart(menuItem)}
                                className="bg-yellow-400 text-gray-800 px-4 py-2 rounded hover:bg-yellow-500 transition-colors"
                            >
                                Add to Cart
                            </button>
                        </div>
                    );
                })}
                <div className="mt-4 text-sm text-gray-600 bg-gray-50 p-4 rounded">
                    <p>{recommendations.reasoning}</p>
                </div>
            </div>
        </div>
    );
};

export default MenuRecommendations;