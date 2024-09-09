import React, { useState } from 'react';
import PromptInput from './PromptInput';  // Make sure this path is correct

function RecipePromptPage() {
  const [response, setResponse] = useState('');

  const handlePromptSubmit = async (prompt) => {
    try {
      const result = await fetch('http://localhost:5000/api/chatgpt', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });
      const data = await result.json();
      setResponse(data.response);
    } catch (error) {
      console.error('Error submitting prompt:', error);
    }
  };

  console.log('handlePromptSubmit:', handlePromptSubmit);  // Check if this logs in the console

  return (
    <div>
      <PromptInput onSubmit={handlePromptSubmit} />
      <div>
        <h3>ChatGPT Response:</h3>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default RecipePromptPage;
