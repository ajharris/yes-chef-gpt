// src/components/AddReminder.js
import React, { useState } from 'react';
import axios from 'axios';

function AddReminder() {
  const [spotName, setSpotName] = useState('');
  const [interval, setInterval] = useState(30);
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('/auth/reminder', {
        spot_name: spotName,
        reminder_interval_days: interval
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Failed to add reminder');
    }
  };

  return (
    <div>
      <h3>Add a New Reminder</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={spotName}
          onChange={(e) => setSpotName(e.target.value)}
          placeholder="Enter kitchen spot (e.g., sink, stove)"
          required
        />
        <input
          type="number"
          value={interval}
          onChange={(e) => setInterval(e.target.value)}
          placeholder="Reminder interval (days)"
        />
        <button type="submit">Add Reminder</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default AddReminder;
