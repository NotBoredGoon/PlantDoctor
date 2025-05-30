import React from 'react';
import MarkdownViewer from '../MarkdownViewer';

const Chatbot = ({ messages }) => {
  return (
    <div className="chatbot-container">
      {messages.map((msg, index) => (
        <div key={index} className={`chat-message ${msg.sender}`}>
          <MarkdownViewer content={msg.text} />
        </div>
      ))}
    </div>
  );
};

export default Chatbot;