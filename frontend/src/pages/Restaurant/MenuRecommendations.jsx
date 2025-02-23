import React, { useState, useEffect, useRef, useCallback } from 'react';
import { orderService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { Sparkles, Wand2 } from 'lucide-react';

const MenuRecommendations = ({ restaurant, onAddToCart }) => {
    // State management
    const [recommendations, setRecommendations] = useState(null);
    const [loading, setLoading] = useState(false);
    const [userPreference, setUserPreference] = useState('');

    // Authentication context
    const { user } = useAuth();

    // Fetch recommendations function
    const fetchRecommendations = useCallback(async (preferenceTriggered = false) => {
        // Only fetch if preference is provided
        if (!preferenceTriggered || !userPreference.trim()) return;

        try {
            setLoading(true);

            // Get user's order history
            let orderHistory = [];
            try {
                const orders = await orderService.getOrders();
                orderHistory = orders.flatMap(order =>
                    order.items.map(item => item.name)
                );
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
                    user_previous_orders: orderHistory,
                    user_preference: userPreference
                })
            });

            if (!response.ok) {
                throw new Error('Failed to fetch recommendations');
            }

            const data = await response.json();

            // Clean up the reasoning text
            const cleanedReasoning = data.reasoning
                .replace(/\*\*.*?\*\*/g, '')  // Remove bold markers
                .trim();

            // Update recommendations
            setRecommendations({
                ...data,
                reasoning: cleanedReasoning
            });
        } catch (error) {
            console.error('Error fetching recommendations:', error);
            setRecommendations(null);
        } finally {
            setLoading(false);
        }
    }, [restaurant, userPreference]);

    // Handler for manual recommendation request
    const handleRecommendationRequest = () => {
        fetchRecommendations(true);
    };

    // Handler for adding recommended item to cart
    const handleAddToCart = (menuItem) => {
        const cartItem = {
            id: `${restaurant.id}-${menuItem.id || menuItem.name}`,
            name: menuItem.name,
            price: menuItem.price,
            restaurantId: restaurant.id,
            quantity: 1
        };
        onAddToCart(cartItem);
    };

    return (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6 border border-gray-100">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-2xl font-bold text-gray-800 flex items-center">
                    <Sparkles className="mr-2 text-yellow-500" />
                    Recommended for You
                </h3>
            </div>

            {/* User Preference Input */}
            <div className="mb-6 flex shadow-sm">
                <div className="relative flex-grow">
                    <input
                        type="text"
                        placeholder="What are you craving? Spicy, light, dessert..."
                        value={userPreference}
                        onChange={(e) => setUserPreference(e.target.value)}
                        className="w-full p-3 pl-10 border border-gray-200 rounded-l-lg focus:ring-2 focus:ring-yellow-300 transition-all duration-300 ease-in-out"
                    />
                    <Wand2 className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                </div>
                <button
                    onClick={handleRecommendationRequest}
                    disabled={loading || !userPreference.trim()}
                    className={`
                        px-6 py-3 bg-yellow-400 text-gray-800 
                        rounded-r-lg hover:bg-yellow-500 
                        transition-all duration-300 
                        flex items-center justify-center
                        ${(loading || !userPreference.trim()) ? 'opacity-50 cursor-not-allowed' : ''}
                    `}
                >
                    {loading ? (
                        <div className="animate-pulse">Finding...</div>
                    ) : (
                        'Get Recommendation'
                    )}
                </button>
            </div>

            {/* Recommendations Area */}
            {recommendations && (
                <div
                    className="space-y-4 animate-fade-in"
                    key={userPreference} // This ensures re-render on preference change
                >
                    {recommendations.recommended_items.map((itemName, index) => {
                        const menuItem = restaurant.menu.find(
                            item => item.name.toLowerCase() === itemName.toLowerCase()
                        );

                        if (!menuItem) return null;

                        return (
                            <div
                                key={index}
                                className="
                                    flex justify-between items-center
                                    p-4 bg-gray-50 rounded-lg
                                    hover:shadow-md
                                    transition-all duration-300
                                    border border-transparent
                                    hover:border-yellow-300
                                "
                            >
                                <div>
                                    <h4 className="font-semibold text-lg text-gray-800">{menuItem.name}</h4>
                                    <p className="text-sm text-gray-600 mb-1">${menuItem.price.toFixed(2)}</p>
                                    {menuItem.description && (
                                        <p className="text-sm text-gray-500 italic">{menuItem.description}</p>
                                    )}
                                </div>
                                <button
                                    onClick={() => handleAddToCart(menuItem)}
                                    className="
                                        bg-yellow-400 text-gray-800
                                        px-4 py-2 rounded-md
                                        hover:bg-yellow-500
                                        transition-colors
                                        flex items-center
                                    "
                                >
                                    Add to Cart
                                </button>
                            </div>
                        );
                    })}

                    {/* Reasoning Section */}
                    <div
                        className="
                            mt-4 text-sm text-gray-600
                            bg-white border border-gray-200
                            p-4 rounded-lg
                            shadow-sm
                        "
                    >
                        <p className="italic">{recommendations.reasoning}</p>
                    </div>
                </div>
            )}

            {/* Empty State */}
            {!recommendations && !loading && (
                <div className="text-center py-8 text-gray-400">
                    <Sparkles className="mx-auto mb-4 text-yellow-500" size={48} />
                    <p>Your personalized recommendation awaits!</p>
                    <p className="text-sm">Tell us what you're in the mood for.</p>
                </div>
            )}
        </div>
    );
};

export default MenuRecommendations;