import React, { useState } from 'react';
import { ragApi } from '../../services/api_client';

interface RAGChatProps {
  chapterId?: string;
}

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

const RAGChat: React.FC<RAGChatProps> = ({ chapterId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (!inputValue.trim()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the RAG API
      const response = await ragApi.queryRag(inputValue, chapterId);

      if (response.success && response.data) {
        const aiMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: response.data.response,
          sender: 'ai',
          timestamp: new Date(response.data.timestamp),
        };

        setMessages(prev => [...prev, aiMessage]);
      } else {
        const errorMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: `Error: ${response.error || 'Failed to get response'}`,
          sender: 'ai',
          timestamp: new Date(),
        };

        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: `Error: ${error.message || 'An unknown error occurred'}`,
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="rag-chat">
      <div className="chat-messages">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.sender}-message`}
            style={{ 
              textAlign: message.sender === 'user' ? 'right' : 'left',
              margin: '10px 0'
            }}
          >
            <div 
              style={{ 
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '18px',
                backgroundColor: message.sender === 'user' ? '#007bff' : '#f8f9fa',
                color: message.sender === 'user' ? 'white' : 'black',
              }}
            >
              {message.text}
            </div>
          </div>
        ))}

        {isLoading && (
          <div style={{ textAlign: 'left', margin: '10px 0' }}>
            <div 
              style={{ 
                display: 'inline-block',
                padding: '8px 12px',
                borderRadius: '18px',
                backgroundColor: '#f8f9fa',
                color: 'black',
              }}
            >
              Thinking...
            </div>
          </div>
        )}
      </div>

      <div className="chat-input">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question about this chapter..."
          rows={3}
          style={{
            width: '100%',
            padding: '8px',
            borderRadius: '4px',
            border: '1px solid #ccc',
            resize: 'vertical',
            minHeight: '60px'
          }}
        />
        <button 
          onClick={handleSend}
          disabled={!inputValue.trim() || isLoading}
          style={{
            marginTop: '8px',
            padding: '8px 16px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: !inputValue.trim() || isLoading ? 'not-allowed' : 'pointer',
            opacity: !inputValue.trim() || isLoading ? 0.6 : 1
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default RAGChat;