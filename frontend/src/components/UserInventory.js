// UserInventory.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserInventory = () => {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    // Fetch user inventory when the component loads
    axios.get('/api/inventory')
      .then(response => setInventory(response.data))
      .catch(error => console.log(error));
  }, []);

  return (
    <div>
      <h2>Your Kitchen Inventory</h2>
      {inventory.map(item => (
        <div key={item.id}>
          {item.name}: {item.quantity}
        </div>
      ))}
    </div>
  );
};

export default UserInventory;
