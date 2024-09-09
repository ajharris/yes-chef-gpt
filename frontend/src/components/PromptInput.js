import React, { useState } from 'react';

function PromptInput({ onSubmit }) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('onSubmit in PromptInput:', typeof onSubmit);  // Log the type of onSubmit

    if (typeof onSubmit === 'function') {
      onSubmit(prompt);  // Call the function if it's a function
    } else {
      console.error('onSubmit is not a function');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Type your recipe prompt here..."
      />
      <button type="submit">Submit</button>
    </form>
  );
}

export default PromptInput;
