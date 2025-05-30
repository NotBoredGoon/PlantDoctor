import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import Chatbot from './components/Chatbot';
import './App.css';

const App = () => {
  const [zipCode, setZipCode] = useState('');
  const [language, setLanguage] = useState('English');
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello! Upload a plant image and enter your zip code to get started.' }
  ]);

  const handleSubmit = async () => {
    if (!image || !zipCode) {
      alert('Please upload an image and enter a zip code.');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('zip_code', zipCode);
    formData.append('image', image);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/process_image', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      const newBotMessage = { sender: 'bot', text: data.text.replace(/\n/g, '<br />') };
      setMessages(prevMessages => [...prevMessages, newBotMessage]);

    } catch (error) {
      console.error('Error processing image:', error);
      const errorMessage = { sender: 'bot', text: 'Sorry, something went wrong. Please try again.' };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const languages = ['English', 'Spanish', 'French', 'German', 'Mandarin', 'Hindi', 'Arabic', 'Portuguese'];

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🌿 PlantDoctor</h1>
        <p>Your AI farming assistant</p>
      </header>

      <main className="app-main">
        <div className="controls-container">
          <ImageUpload onImageUpload={setImage} />
          <input
            type="text"
            className="zip-code-input"
            placeholder="Enter your Zip Code"
            value={zipCode}
            onChange={(e) => setZipCode(e.target.value)}
          />
          <select
            className="language-dropdown"
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
          >
            {languages.map(lang => <option key={lang} value={lang}>{lang}</option>)}
          </select>
          <button className="submit-button" onClick={handleSubmit} disabled={loading}>
            {loading ? <div className="loader"></div> : 'Process Image'}
          </button>
        </div>

        <Chatbot messages={messages} />

        <div className="future-feature">
          <h2>Future Vision: Drone Analysis</h2>
          <p>Imagine analyzing entire fields with drone footage. Here’s a concept map of how PlantDoctor would highlight areas needing attention.</p>
          <img src="https://storage.googleapis.com/gweb-cloudblog-publish/images/social_image_2022_07_27_10_01_00_0700_399.max-1000x1000.png" alt="Example map of drone footage analysis" className="map-image" />
        </div>
      </main>
    </div>
  );
};

export default App;