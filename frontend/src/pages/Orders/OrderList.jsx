import React, { useState, useEffect } from 'react';
import { orderService } from '../../services/api';
import './OrderList.css';

function OrderList() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchOrders = async () => {
            try {
                setLoading(true);
                const data = await orderService.getOrders();

                // Sort orders by creation date, most recent first
                const sortedOrders = data.sort((a, b) =>
                    new Date(b.created_at) - new Date(a.created_at)
                );

                setOrders(sortedOrders);
                setLoading(false);
            } catch (error) {
                console.error('Failed to fetch orders', error);
                setError('Unable to load orders. Please try again.');
                setLoading(false);
            }
        };

        fetchOrders();
    }, []);

    if (loading) {
        return <div className="orders-loading">Loading orders...</div>;
    }

    if (error) {
        return <div className="orders-error">{error}</div>;
    }

    return (
        <div className="order-list">
            <h1>My Orders</h1>
            {orders.length === 0 ? (
                <p>No orders found</p>
            ) : (
                <div className="orders-container">
                    {orders.map((order) => (
                        <div key={order.id} className="order-card">
                            <div className="order-header">
                                <h2>Order #{order.id}</h2>
                                <span className="order-status">{order.status}</span>
                            </div>
                            <p className="order-date">
                                {new Date(order.created_at).toLocaleString()}
                            </p>
                            <div className="order-total">
                                <strong>Total:</strong> ${order.total_price.toFixed(2)}
                            </div>
                            <div className="order-items">
                                <h3>Items:</h3>
                                {order.items.map((item, index) => (
                                    <div key={index} className="order-item">
                                        <span>{item.name}</span>
                                        <span>
                                            {item.quantity} x ${item.price.toFixed(2)}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default OrderList;