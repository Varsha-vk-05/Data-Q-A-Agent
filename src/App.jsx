import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import QACard from './components/QACard';
import { computeAnswers } from './utils/computeQA';

export default function App() {
  const [data, setData] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch default CSV with relative path for deployment compatibility
    fetch('sales_data.csv')
      .then(response => {
        if (!response.ok) throw new Error("Could not load default CSV");
        return response.text();
      })
      .then(csvText => {
        Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            setData(results.data);
            const computed = computeAnswers(results.data);
            setAnswers(computed);
            setLoading(false);
          },
          error: (err) => {
            setError(err.message);
            setLoading(false);
          }
        });
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return (
    <div className="app-container">
      <header>
        <h1>Data Q&A Agent</h1>
        <p className="subtitle">Computing intelligent answers directly from your dataset.</p>
      </header>

      <main>
        {loading && <div className="loading">Agent is analyzing the data...</div>}
        {error && <div className="error" style={{color: '#ef4444', textAlign: 'center'}}>Error: {error}</div>}
        
        {!loading && !error && answers.length > 0 && (
          <div className="qa-grid">
            {answers.map((item, index) => (
              <QACard key={index} item={item} index={index} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
