import React, { useEffect, useState, useCallback } from 'react';

function buildBaseUrl() {
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  if (codespace) return `https://${codespace}-8000.app.github.dev`;
  return `${window.location.protocol}//${window.location.host}`;
}

export default function Leaderboard() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(() => {
    setLoading(true);
    const base = buildBaseUrl();
    const endpoint = `${base}/api/leaderboard/`;
    console.log('Fetching Leaderboard from', endpoint);

    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        console.log('Leaderboard response:', data);
        const payload = data && data.results ? data.results : data || [];
        setItems(payload);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching leaderboard', err);
        setError(err.toString());
        setLoading(false);
      });
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="card card-table">
      <div className="card-body">
        <div className="header-row mb-3">
          <h2 className="h4">Leaderboard</h2>
          <div>
            <button className="btn btn-primary" onClick={fetchData}>Refresh</button>
          </div>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead>
              <tr>
                <th>Rank</th>
                <th>User</th>
                <th>Team</th>
                <th>Calories</th>
                <th>Distance (km)</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr><td colSpan="6">Loading...</td></tr>
              )}
              {!loading && items.length === 0 && (
                <tr><td colSpan="6">No leaderboard entries found.</td></tr>
              )}
              {items.map((entry, idx) => (
                <tr key={entry.id || idx}>
                  <td>{entry.rank || idx + 1}</td>
                  <td>{entry.user?.username || entry.user || 'N/A'}</td>
                  <td>{entry.team?.name || entry.team || 'N/A'}</td>
                  <td>{entry.total_calories_burned || 0}</td>
                  <td>{entry.total_distance_km || 0}</td>
                  <td><button className="btn btn-sm btn-outline-primary">View</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
