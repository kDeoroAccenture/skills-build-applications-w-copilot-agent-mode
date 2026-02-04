import React, { useEffect, useState, useCallback } from 'react';

function buildBaseUrl() {
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  if (codespace) return `https://${codespace}-8000.app.github.dev`;
  return `${window.location.protocol}//${window.location.host}`;
}

export default function Workouts() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(() => {
    setLoading(true);
    const base = buildBaseUrl();
    const endpoint = `${base}/api/workouts/`;
    console.log('Fetching Workouts from', endpoint);

    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        console.log('Workouts response:', data);
        const payload = data && data.results ? data.results : data || [];
        setItems(payload);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching workouts', err);
        setError(err.toString());
        setLoading(false);
      });
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="card card-table">
      <div className="card-body">
        <div className="header-row mb-3">
          <h2 className="h4">Workouts</h2>
          <div>
            <button className="btn btn-primary" onClick={fetchData}>Refresh</button>
          </div>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Difficulty</th>
                <th>Duration (min)</th>
                <th>Estimated Calories</th>
              </tr>
            </thead>
            <tbody>
              {loading && (<tr><td colSpan="5">Loading...</td></tr>)}
              {!loading && items.length === 0 && (<tr><td colSpan="5">No workouts found.</td></tr>)}
              {items.map((w, idx) => (
                <tr key={w.id || idx}>
                  <td>{w.id || idx}</td>
                  <td>{w.title}</td>
                  <td>{w.difficulty}</td>
                  <td>{w.duration_minutes || '-'}</td>
                  <td>{w.estimated_calories || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
