// src/components/TestConnection.js

import React, { useState } from 'react';

const TestConnection = ({ testConnection }) => {
    const [serverInfo, setServerInfo] = useState(null);
    const [error, setError] = useState(null);

    const handleTestConnection = async () => {
        try {
            const info = await testConnection();
            setServerInfo(info);
            setError(null);  // Clear any previous error
        } catch (err) {
            setServerInfo(null);  // Clear any previous server info
            setError("Failed to fetch server information");
        }
    };

    return (
        <div>
            <button onClick={handleTestConnection}>Test Connection</button>
            {serverInfo && (
                <div style={{ marginTop: '10px' }}>
                    <h3>Server Information:</h3>
                    <pre>{JSON.stringify(serverInfo, null, 2)}</pre>
                </div>
            )}
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
        </div>
    );
};

export default TestConnection;
