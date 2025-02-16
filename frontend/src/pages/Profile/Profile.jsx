import React, { useState, useEffect } from 'react';
import { userService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import './Profile.css';

function Profile() {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [editMode, setEditMode] = useState(false);
    const { logout } = useAuth();

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: ''
    });

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await userService.getProfile();
                setProfile(data);
                setFormData({
                    name: data.name || '',
                    email: data.email || '',
                    phone: data.phone || ''
                });
                setLoading(false);
            } catch (error) {
                console.error('Failed to fetch profile', error);
                setLoading(false);
            }
        };

        fetchProfile();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await userService.updateProfile(formData);
            setEditMode(false);
        } catch (error) {
            console.error('Failed to update profile', error);
        }
    };

    if (loading) {
        return <div>Loading profile...</div>;
    }

    return (
        <div className="profile-container">
            <h1>My Profile</h1>
            {editMode ? (
                <form onSubmit={handleSubmit} className="profile-form">
                    <div className="form-group">
                        <label>Name</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleInputChange}
                            disabled
                        />
                    </div>
                    <div className="form-group">
                        <label>Phone</label>
                        <input
                            type="tel"
                            name="phone"
                            value={formData.phone}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="profile-actions">
                        <button type="submit" className="btn btn-primary">Save</button>
                        <button
                            type="button"
                            onClick={() => setEditMode(false)}
                            className="btn btn-secondary"
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            ) : (
                <div className="profile-details">
                    <p><strong>Name:</strong> {profile.name}</p>
                    <p><strong>Email:</strong> {profile.email}</p>
                    <p><strong>Phone:</strong> {profile.phone || 'Not provided'}</p>
                    <div className="profile-actions">
                        <button
                            onClick={() => setEditMode(true)}
                            className="btn btn-primary"
                        >
                            Edit Profile
                        </button>
                        <button
                            onClick={logout}
                            className="btn btn-secondary"
                        >
                            Logout
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default Profile;