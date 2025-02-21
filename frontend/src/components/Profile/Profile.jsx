import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { userService } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import { User, Mail, Phone, Lock, LogOut, Edit } from 'lucide-react';
import './Profile.css';

function Profile() {
    const navigate = useNavigate();
    const { logout } = useAuth();
    const [loading, setLoading] = useState(true);
    const [editMode, setEditMode] = useState(false);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const [profile, setProfile] = useState({
        name: '',
        email: '',
        phone: ''
    });

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        newPassword: '',
        confirmNewPassword: ''
    });

    const fetchProfile = async () => {
        try {
            const userData = await userService.getProfile();

            const newProfile = {
                name: userData.full_name || '',
                email: userData.email || '',
                phone: userData.phone_number
            };

            setProfile(newProfile);

            const newFormData = {
                name: userData.full_name || '',
                email: userData.email || '',
                phone: userData.phone_number || '',
                newPassword: '',
                confirmNewPassword: ''
            };

            setFormData(newFormData);
            setLoading(false);
        } catch (error) {
            console.error('Failed to load profile:', error);
            toast.error('Failed to load profile');
            setLoading(false);
        }
    };

    useEffect(() => {
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

        if (formData.newPassword) {
            if (formData.newPassword !== formData.confirmNewPassword) {
                toast.error('Passwords do not match');
                return;
            }
        }

        try {
            setIsSubmitting(true);

            const updateData = {
                name: formData.name,
                phone: formData.phone,
                ...(formData.newPassword && { password: formData.newPassword })
            };

            const updatedProfile = await userService.updateProfile(updateData);

            setProfile({
                name: updatedProfile.full_name,
                email: updatedProfile.email,
                phone: updatedProfile.phone_number
            });

            setEditMode(false);
            toast.success('Profile updated successfully');
            await fetchProfile();
        } catch (error) {
            console.error('Failed to update profile:', error);
            toast.error(error.response?.data?.detail || 'Failed to update profile');
        } finally {
            setIsSubmitting(false);
        }
    };

    if (loading) {
        return (
            <div className="modern-profile-container">
                <div className="modern-profile-loading">Loading your profile...</div>
            </div>
        );
    }

    if (editMode) {
        return (
            <div className="modern-profile-container">
                <h1>Edit Profile</h1>
                <form onSubmit={handleSubmit} className="modern-profile-form">
                    <div className="modern-form-group">
                        <label>
                            <User size={16} className="icon" />
                            Full Name
                        </label>
                        <input
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={handleInputChange}
                            placeholder="Enter your full name"
                            required
                        />
                    </div>

                    <div className="modern-form-group">
                        <label>
                            <Mail size={16} className="icon" />
                            Email
                        </label>
                        <input
                            type="email"
                            value={formData.email}
                            disabled
                            className="modern-input-disabled"
                        />
                    </div>

                    <div className="modern-form-group">
                        <label>
                            <Phone size={16} className="icon" />
                            Phone Number
                        </label>
                        <input
                            type="tel"
                            name="phone"
                            value={formData.phone}
                            onChange={handleInputChange}
                            placeholder="Enter your phone number"
                        />
                    </div>

                    <div className="modern-form-group">
                        <label>
                            <Lock size={16} className="icon" />
                            New Password (optional)
                        </label>
                        <input
                            type="password"
                            name="newPassword"
                            value={formData.newPassword}
                            onChange={handleInputChange}
                            placeholder="Leave blank to keep current password"
                        />
                    </div>

                    {formData.newPassword && (
                        <div className="modern-form-group">
                            <label>
                                <Lock size={16} className="icon" />
                                Confirm New Password
                            </label>
                            <input
                                type="password"
                                name="confirmNewPassword"
                                value={formData.confirmNewPassword}
                                onChange={handleInputChange}
                                placeholder="Confirm your new password"
                                required
                            />
                        </div>
                    )}

                    <div className="modern-profile-actions">
                        <button
                            type="submit"
                            className="modern-btn modern-btn-primary"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Saving Changes...' : 'Save Changes'}
                        </button>
                        <button
                            type="button"
                            className="modern-btn modern-btn-secondary"
                            onClick={() => setEditMode(false)}
                            disabled={isSubmitting}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        );
    }

    return (
        <div className="modern-profile-container">
            <h1>My Profile</h1>
            <div className="modern-profile-details">
                <div className="modern-profile-item">
                    <strong>
                        <User className="icon" size={18} />
                        Name
                    </strong>
                    <span>{profile.name}</span>
                </div>
                <div className="modern-profile-item">
                    <strong>
                        <Mail className="icon" size={18} />
                        Email
                    </strong>
                    <span>{profile.email}</span>
                </div>
                <div className="modern-profile-item">
                    <strong>
                        <Phone className="icon" size={18} />
                        Phone
                    </strong>
                    <span>{profile.phone || 'Not provided'}</span>
                </div>
            </div>

            <div className="modern-profile-actions">
                <button
                    onClick={() => setEditMode(true)}
                    className="modern-btn modern-btn-primary"
                >
                    <Edit size={18} /> Edit Profile
                </button>
                <button
                    onClick={logout}
                    className="modern-btn modern-btn-secondary"
                >
                    <LogOut size={18} /> Logout
                </button>
            </div>
        </div>
    );
}

export default Profile;