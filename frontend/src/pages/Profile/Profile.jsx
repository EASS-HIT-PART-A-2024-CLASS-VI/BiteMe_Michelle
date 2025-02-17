import React, { useState, useEffect } from 'react';
import { userService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { toast } from 'react-toastify';
import './Profile.css';

function Profile() {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [editMode, setEditMode] = useState(false);
    const { logout } = useAuth();

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        password: '',
        confirmPassword: ''
    });

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const data = await userService.getProfile();
                setProfile(data);
                setFormData({
                    name: data.full_name || '',
                    email: data.email || '',
                    phone: data.phone_number || '',
                    password: '',
                    confirmPassword: ''
                });
                setLoading(false);
            } catch (error) {
                console.error('Failed to fetch profile', error);
                toast.error('Failed to load profile');
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

        // Validate password match if password is being changed
        if (formData.password && formData.password !== formData.confirmPassword) {
            toast.error('Passwords do not match');
            return;
        }

        try {
            // Prepare update data
            const updateData = {
                name: formData.name,
                phone: formData.phone
            };

            // Add password if provided
            if (formData.password) {
                updateData.password = formData.password;
            }

            // Send update request
            const updatedProfile = await userService.updateProfile(updateData);

            // Update local state
            setProfile(updatedProfile);
            setEditMode(false);

            toast.success('Profile updated successfully');
        } catch (error) {
            console.error('Failed to update profile', error);
            toast.error(error.response?.data?.detail || 'Failed to update profile');
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
                        <label>Full Name</label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Email (cannot be changed)</label>
                        <input
                            type="email"
                            value={formData.email}
                            disabled
                        />
                    </div>
                    <div className="form-group">
                        <label>Phone Number</label>
                        <input
                            type="tel"
                            name="phone"
                            value={formData.phone}
                            onChange={handleInputChange}
                        />
                    </div>
                    <div className="form-group">
                        <label>New Password (optional)</label>
                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleInputChange}
                            placeholder="Leave blank to keep current password"
                        />
                    </div>
                    {formData.password && (
                        <div className="form-group">
                            <label>Confirm New Password</label>
                            <input
                                type="password"
                                name="confirmPassword"
                                value={formData.confirmPassword}
                                onChange={handleInputChange}
                                required={!!formData.password}
                            />
                        </div>
                    )}
                    <div className="profile-actions">
                        <button type="submit" className="btn btn-primary">Save Changes</button>
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
                    <p><strong>Name:</strong> {profile.full_name}</p>
                    <p><strong>Email:</strong> {profile.email}</p>
                    <p><strong>Phone:</strong> {profile.phone_number || 'Not provided'}</p>
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