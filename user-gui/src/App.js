import React, { useState } from 'react';
import './App.css';

function App() {
  const [name, setName] = useState('');
  const [result, setResult] = useState('');

  const handleSubmit = async () => {
    if (!name.trim()) {
      setResult('❌ Please enter a name');
      return;
    }

    try {
      const res = await fetch('http://localhost:5000/comedor', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
      });

      const data = await res.json();
      if (res.ok) {
        setResult(`✅ User created! ID: ${data.id}`);
        setName('');
      } else {
        setResult(`❌ Error: ${data.error}`);
      }
    } catch (err) {
      setResult('❌ Server is unreachable');
      console.error(err);
    }
  };

  return (
    <div className="App">
      <h1>Create User</h1>
      <input
        type="text"
        placeholder="Enter name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <button onClick={handleSubmit}>Send</button>
      <div style={{ marginTop: '20px' }}>{result}</div>
    </div>
  );
}

export default App;
