import React, { useState, useEffect, useCallback } from 'react';

const WebSocketComponent: React.FC = () => {
  const [socket, setSocket] = useState<WebSocket | null>(null);
  const [messages, setMessages] = useState<string[]>([]);
  const [inputMessage, setInputMessage] = useState('');

  useEffect(() => {
    const clientId = Date.now()
    const ws = new WebSocket(`ws://localhost:80/ws?clientId=${clientId}`);
    
    ws.onopen = () => {
      console.log('Connected to WebSocket');
    };

    ws.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    ws.onclose = () => {
      console.log('Disconnected from WebSocket');
    };

    ws.onerror = (error) => {
      console.error(error);
    }

    // window.addEventListener('beforeunload', () => {
    //   ws.close(1000, 'Page is being unloaded');
    // });

    setSocket(ws);

    return () => {
      console.log('Websocket cleanup')
      ws.close();
    };
  }, []);

  const sendMessage = useCallback(() => {
    if (socket && inputMessage) {
      socket.send(inputMessage);
      setInputMessage('');
    }
  }, [socket, inputMessage]);

  return (
    <div>
      <ul>
        {messages.map((message, index) => (
          <li key={index}>{message}</li>
        ))}
      </ul>
      <input
        type="text"
        value={inputMessage}
        onChange={(e) => setInputMessage(e.target.value)}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default WebSocketComponent;