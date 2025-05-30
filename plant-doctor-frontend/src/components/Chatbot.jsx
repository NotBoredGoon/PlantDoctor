import React from 'react';

const Chatbot = ({ messages }) => {
  return (
    <div className="chatbot-container">
      {messages.map((msg, index) => (
        <div key={index} className={`chat-message ${msg.sender}`}>
          <p dangerouslySetInnerHTML={{ __html: msg.text }} />
        </div>
      ))}
    </div>
  );
};

export default Chatbot;