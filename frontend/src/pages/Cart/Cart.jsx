import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { useCart } from '../../context/CartContext';
import { orderService } from '../../services/api';
import './Cart.css';

function CheckoutModal({ total, onClose, onConfirm }) {
    const [paymentMethod, setPaymentMethod] = useState('credit');
    const [name, setName] = useState('');
    const [cardNumber, setCardNumber] = useState('');
    const [expiry, setExpiry] = useState('');
    const [cvv, setCvv] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();

        // Basic validation
        if (!name || !cardNumber || !expiry || !cvv) {
            toast.error('Please fill in all payment details');
            return;
        }

        // Validate card number (simple check)
        const cardNumberRegex = /^\d{16}$/;
        if (!cardNumberRegex.test(cardNumber.replace(/\s/g, ''))) {
            toast.error('Invalid card number');
            return;
        }

        // Validate expiry date
        const expiryRegex = /^(0[1-9]|1[0-2])\/\d{2}$/;
        if (!expiryRegex.test(expiry)) {
            toast.error('Invalid expiry date. Use MM/YY format');
            return;
        }

        // Validate CVV
        const cvvRegex = /^\d{3}$/;
        if (!cvvRegex.test(cvv)) {
            toast.error('Invalid CVV');
            return;
        }

        // Simulate payment processing
        onConfirm();
    };

    return (
        <div className="checkout-modal-overlay">
            <div className="checkout-modal">
                <h2>Checkout</h2>
                <p>Total: ${total.toFixed(2)}</p>

                <form onSubmit={handleSubmit}>
                    <div className="payment-methods">
                        <label>
                            <input
                                type="radio"
                                name="paymentMethod"
                                value="credit"
                                checked={paymentMethod === 'credit'}
                                onChange={() => setPaymentMethod('credit')}
                            />
                            Credit Card
                        </label>
                        <label>
                            <input
                                type="radio"
                                name="paymentMethod"
                                value="paypal"
                                checked={paymentMethod === 'paypal'}
                                onChange={() => setPaymentMethod('paypal')}
                            />
                            PayPal
                        </label>
                    </div>

                    <div className="form-group">
                        <label>Cardholder Name</label>
                        <input
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            placeholder="John Doe"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Card Number</label>
                        <input
                            type="text"
                            value={cardNumber}
                            onChange={(e) => setCardNumber(e.target.value)}
                            placeholder="1234 5678 9012 3456"
                            required
                        />
                    </div>

                    <div className="card-details">
                        <div className="form-group">
                            <label>Expiry Date</label>
                            <input
                                type="text"
                                value={expiry}
                                onChange={(e) => setExpiry(e.target.value)}
                                placeholder="MM/YY"
                                required
                            />
                        </div>
                        <div className="form-group">
                            <label>CVV</label>
                            <input
                                type="text"
                                value={cvv}
                                onChange={(e) => setCvv(e.target.value)}
                                placeholder="123"
                                required
                            />
                        </div>
                    </div>

                    <div className="checkout-actions">
                        <button
                            type="button"
                            onClick={onClose}
                            className="btn btn-secondary"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="btn btn-primary"
                        >
                            Pay Now
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}

function Cart() {
    const navigate = useNavigate();
    const {
        cartItems,
        removeFromCart,
        updateQuantity,
        calculateTotal,
        clearCart
    } = useCart();

    const [isCheckoutModalOpen, setIsCheckoutModalOpen] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);

    const handleCheckout = () => {
        if (cartItems.length === 0) {
            toast.error('Your cart is empty');
            return;
        }

        // Open checkout modal
        setIsCheckoutModalOpen(true);
    };

    const processPayment = async () => {
        setIsProcessing(true);

        try {
            // Group items by restaurant
            const restaurantGroups = cartItems.reduce((groups, item) => {
                const restaurantId = item.restaurantId || 'unknown';
                if (!groups[restaurantId]) {
                    groups[restaurantId] = [];
                }
                groups[restaurantId].push(item);
                return groups;
            }, {});

            // Create separate orders for each restaurant group
            const orderPromises = Object.entries(restaurantGroups).map(([restaurantId, items]) => {
                const orderItems = items.map(item => ({
                    menu_item_id: item.id,
                    name: item.name,
                    quantity: item.quantity,
                    price: item.price,
                    restaurant_id: restaurantId
                }));

                const orderData = {
                    items: orderItems,
                    total_price: items.reduce(
                        (total, item) => total + (item.price * item.quantity),
                        0
                    ),
                    status: 'PENDING',
                    created_at: new Date().toISOString(),
                    payment_method: 'credit_card'
                };

                return orderService.createOrder(orderData);
            });

            // Wait for all orders to be created
            await Promise.all(orderPromises);

            // Clear cart after successful order
            clearCart();

            // Close checkout modal
            setIsCheckoutModalOpen(false);

            // Show success toast
            toast.success('Order placed successfully!');

            // Navigate to orders page
            navigate('/orders');
        } catch (error) {
            console.error('Checkout failed', error);

            // Specific error message
            toast.error(
                error.response?.data?.detail ||
                'Failed to place order. Please check your connection and try again.'
            );
        } finally {
            setIsProcessing(false);
        }
    };

    // Calculate total quantity of items in cart
    const totalQuantity = cartItems.reduce(
        (total, item) => total + item.quantity,
        0
    );

    return (
        <div className="cart-container">
            <h1>Your Cart</h1>
            {cartItems.length === 0 ? (
                <p>Your cart is empty</p>
            ) : (
                <>
                    <div className="cart-summary-header">
                        <p>Total Items: {totalQuantity}</p>
                    </div>

                    <div className="cart-items">
                        {cartItems.map((item) => (
                            <div key={item.id} className="cart-item">
                                <div className="cart-item-details">
                                    <span className="item-name">{item.name}</span>
                                    <span className="item-price">${item.price.toFixed(2)} each</span>
                                </div>
                                <div className="item-controls">
                                    <button
                                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                        disabled={item.quantity <= 1}
                                    >
                                        -
                                    </button>
                                    <span>{item.quantity}</span>
                                    <button
                                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                    >
                                        +
                                    </button>
                                </div>
                                <span className="item-total">
                                    ${(item.price * item.quantity).toFixed(2)}
                                </span>
                                <button
                                    onClick={() => removeFromCart(item.id)}
                                    className="remove-item"
                                >
                                    Remove
                                </button>
                            </div>
                        ))}
                    </div>

                    <div className="cart-summary">
                        <div className="cart-total">
                            <strong>Total:</strong> ${calculateTotal().toFixed(2)}
                        </div>
                        <button
                            onClick={handleCheckout}
                            disabled={isProcessing}
                            className="btn btn-primary checkout-btn"
                        >
                            {isProcessing ? 'Processing...' : 'Checkout'}
                        </button>
                    </div>

                    {isCheckoutModalOpen && (
                        <CheckoutModal
                            total={calculateTotal()}
                            onClose={() => setIsCheckoutModalOpen(false)}
                            onConfirm={processPayment}
                        />
                    )}
                </>
            )}
        </div>
    );
}

export default Cart;