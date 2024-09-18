import React, { useState } from 'react';

const QueryGPT = () => {
  const [prompt, setPrompt] = useState(''); // Stores the user prompt
  const [response, setResponse] = useState(null); // Stores the response from ChatGPT
  const [queryTime, setQueryTime] = useState(null); // Stores the query duration
  const [loading, setLoading] = useState(false); // Tracks the loading state
  const [error, setError] = useState(null); // Stores any error messages

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);
    setQueryTime(null);

    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }), // Send the prompt to the backend
      });

      const data = await res.json();

      if (res.ok) {
        setResponse(data.response); // Set the response from the backend
        setQueryTime(data.duration); // Set the query duration
      } else {
        throw new Error(data.error || 'An unknown error occurred');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false); // Stop the loading state
    }
  };

  return (
    <div>
      <h2>Query ChatGPT</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Type your prompt here..."
          rows="5"
          style={{ width: '100%' }}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>

      {/* Display loading indicator */}
      {loading && <p>Loading...</p>}

      {/* Display error message if any */}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}

      {/* Display ChatGPT response */}
      {response && (
        <div>
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}

      {/* Display query time */}
      {queryTime && <p>Query Time: {queryTime.toFixed(2)} seconds</p>}
    </div>
  );
};

export default QueryGPT;
