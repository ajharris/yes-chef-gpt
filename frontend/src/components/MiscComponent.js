import React from 'react';
import axios from 'axios';

function YourComponent() {
  const handleButtonClick = async () => {
    try {
      const response = await axios.post('/api/button-click');
      console.log(response.data);  // Handle the response as needed
      alert(response.data.message);  // Example of handling the response
    } catch (error) {
      console.error('Error during API call:', error);
      alert('Failed to click button!');
    }
  };

  return (
    <div>
      <button onClick={handleButtonClick}>Click Me!</button>
    </div>
  );
}

export default MiscComponent;