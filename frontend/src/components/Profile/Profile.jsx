import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { userService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import './Profile.css';

function Profile() {
    const navigate = useNavigate();
    const { logout } = useAuth();

    // State for loading and edit mode
    const [loading, setLoading] = useState(true);
    const [editMode, setEditMode] = useState(false);

    // State for user profile
    const [profile, setProfile] = useState({
        name: '',
        email: '',
        phone: ''
    });

    // State for form data (includes password fields)
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        currentPassword: '',
        newPassword: '',
        confirmNewPassword: ''
    });

    // Fetch user profile on component mount
    useEffect(() => {
        const fetchUserProfile = async () => {
            try {
                const userData = await userService.getProfile();
                setProfile({
                    name: userData.full_name || '',
                    email: userData.email || '',
                    phone: userData.phone_number || ''
                });

                // Populate form with existing data
                setFormData({
                    name: userData.full_name || '',
                    email: userData.email || '',
                    phone: userData.phone_number || '',
                    currentPassword: '',
                    newPassword: '',
                    confirmNewPassword: ''
                });

                setLoading(false);
            } catch (error) {
                toast.error('Failed to load profile');
                setLoading(false);
            }
        };

        fetchUserProfile();
    }, []);

    // Handle input changes
    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevData => ({
            ...prevData,
            [name]: value
        }));
    };

    // Handle profile update submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate new password if entered
        if (formData.newPassword) {
            if (formData.newPassword !== formData.confirmNewPassword) {
                toast.error('New passwords do not match');
                return;
            }
        }

        try {
            // Prepare update data
            const updateData = {
                name: formData.name,
                phone: formData.phone
            };

            // Add password if new password is provided
            if (formData.newPassword) {
                updateData.password = formData.newPassword;
            }

            // Update profile
            const updatedProfile = await userService.updateProfile(updateData);

            // Update local state
            setProfile({
                name: updatedProfile.full_name,
                email: updatedProfile.email,
                phone: updatedProfile.phone_number
            });

            // Exit edit mode
            setEditMode(false);

            // Show success message
            toast.success('Profile updated successfully');
        } catch (error) {
            // Handle update errors
            const errorMessage = error.response?.data?.detail || 'Update failed';
            toast.error(errorMessage);
            console.error('Profile update error:', error);
        }
    };

    // Handle logout
    const handleLogout = () => {
        logout();
        navigate('/');
    };

    // Render loading state
    if (loading) {
        return <div className="profile-loading">Loading profile...</div>;
    }

    // Render edit mode
    if (editMode) {
        return (
            <div className="profile-container">
                <h1>Edit Profile</h1>
                <form onSubmit={handleSubmit} className="profile-edit-form">
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
                            name="newPassword"
                            value={formData.newPassword}
                            onChange={handleInputChange}
                            placeholder="Leave blank to keep current password"
                        />
                    </div>

                    {formData.newPassword && (
                        <div className="form-group">
                            <label>Confirm New Password</label>
                            <input
                                type="password"
                                name="confirmNewPassword"
                                value={formData.confirmNewPassword}
                                onChange={handleInputChange}
                                required
                            />
                        </div>
                    )}

                    <div className="profile-actions">
                        <button
                            type="submit"
                            className="btn btn-primary"
                        >
                            Save Changes
                        </button>
                        <button
                            type="button"
                            className="btn btn-secondary"
                            onClick={() => setEditMode(false)}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        );
    }

    // Render view mode
    return (
        <div className="profile-container">
            <h1>My Profile</h1>
            <div className="profile-details">
                <div className="profile-item">
                    <strong>Name:</strong>
                    <span>{profile.name}</span>
                </div>
                <div className="profile-item">
                    <strong>Email:</strong>
                    <span>{profile.email}</span>
                </div>
                <div className="profile-item">
                    <strong>Phone:</strong>
                    <span>{profile.phone || 'Not provided'}</span>
                </div>
            </div>

            <div className="profile-actions">
                <button
                    onClick={() => setEditMode(true)}
                    className="btn btn-primary"
                >
                    Edit Profile
                </button>
                <button
                    onClick={handleLogout}
                    className="btn btn-secondary"
                >
                    Logout
                </button>
            </div>
        </div>
    );
}

export default Profile;