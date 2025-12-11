import React, { useState, useEffect } from 'react';
import { userPreferencesApi } from '../../services/api_client';

interface SettingsProps {}

interface UserPreferences {
  language: string;
  personalization_enabled: boolean;
  preferred_chapters: string | null;
}

const Settings: React.FC<SettingsProps> = () => {
  const [preferences, setPreferences] = useState<UserPreferences>({
    language: 'en',
    personalization_enabled: true,
    preferred_chapters: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [saveSuccess, setSaveSuccess] = useState(false);

  useEffect(() => {
    const fetchPreferences = async () => {
      try {
        setLoading(true);
        const response = await userPreferencesApi.getPreferences();
        
        if (response.success && response.data) {
          setPreferences({
            language: response.data.language || 'en',
            personalization_enabled: response.data.personalization_enabled !== false,
            preferred_chapters: response.data.preferred_chapters || null,
          });
        } else {
          // Set default preferences if none exist
          setPreferences({
            language: 'en',
            personalization_enabled: true,
            preferred_chapters: null,
          });
        }
      } catch (err) {
        setError('Failed to load preferences');
      } finally {
        setLoading(false);
      }
    };

    fetchPreferences();
  }, []);

  const handleSave = async () => {
    try {
      const response = await userPreferencesApi.updatePreferences(preferences);
      
      if (response.success) {
        setSaveSuccess(true);
        setTimeout(() => setSaveSuccess(false), 3000); // Hide success message after 3 seconds
      } else {
        setError(response.error || 'Failed to save preferences');
      }
    } catch (err) {
      setError('An error occurred while saving preferences');
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement | HTMLInputElement>) => {
    const { name, value, type } = e.target;
    const checked = type === 'checkbox' ? (e.target as HTMLInputElement).checked : undefined;
    
    setPreferences(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  if (loading) {
    return <div>Loading settings...</div>;
  }

  return (
    <div className="settings">
      <h3>Personalization Settings</h3>
      
      {error && <div style={{ color: 'red' }}>Error: {error}</div>}
      {saveSuccess && <div style={{ color: 'green' }}>Preferences saved successfully!</div>}
      
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="language">Language: </label>
        <select
          id="language"
          name="language"
          value={preferences.language}
          onChange={handleChange}
        >
          <option value="en">English</option>
          <option value="ur">Urdu</option>
        </select>
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label>
          <input
            type="checkbox"
            name="personalization_enabled"
            checked={preferences.personalization_enabled}
            onChange={handleChange}
          />
          Enable Personalization
        </label>
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label htmlFor="preferred_chapters">Preferred Chapters Order: </label>
        <input
          type="text"
          id="preferred_chapters"
          name="preferred_chapters"
          value={preferences.preferred_chapters || ''}
          onChange={handleChange}
          placeholder="Enter chapter numbers separated by commas (e.g., 1,3,2)"
        />
        <div style={{ fontSize: '0.8em', color: '#666' }}>
          Enter chapter numbers in your preferred order (e.g., "1,3,2" to read chapter 1, then 3, then 2)
        </div>
      </div>
      
      <button 
        onClick={handleSave}
        style={{
          padding: '8px 16px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        Save Settings
      </button>
    </div>
  );
};

export default Settings;