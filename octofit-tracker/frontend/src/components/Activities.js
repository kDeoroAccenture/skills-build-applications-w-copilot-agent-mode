import React, { useEffect, useState, useCallback } from 'react';

function buildBaseUrl() {
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  if (codespace) return `https://${codespace}-8000.app.github.dev`;
  return `${window.location.protocol}//${window.location.host}`;
}

export default function Activities() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(() => {
    setLoading(true);
    const base = buildBaseUrl();
    const endpoint = `${base}/api/activities/`;
    console.log('Fetching Activities from', endpoint);

    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        console.log('Activities response:', data);
        const payload = data && data.results ? data.results : data || [];
        setItems(payload);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching activities', err);
        setError(err.toString());
        setLoading(false);
      });
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="card card-table">
      <div className="card-body">
        <div className="header-row mb-3">
          <h2 className="h4">Activities</h2>
          <div>
            <button className="btn btn-primary" onClick={fetchData}>
              Refresh
            </button>
          </div>
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Type</th>
                <th>User</th>
                <th>Duration (min)</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {loading && (
                <tr>
                  <td colSpan="7">Loading...</td>
                </tr>
              )}
              {!loading && items.length === 0 && (
                <tr>
                  <td colSpan="7">No activities found.</td>
                </tr>
              )}
              {items.map((a, idx) => (
                <tr key={a.id || idx}>
                  <td>{a.id || idx}</td>
                  <td>{a.title || a.activity_type}</td>
                  <td>{a.activity_type}</td>
                  <td>{a.user?.username || (typeof a.user === 'string' ? a.user : 'N/A')}</td>
                  <td>{a.duration_minutes || '-'}</td>
                  <td>{a.activity_date ? new Date(a.activity_date).toLocaleString() : '-'}</td>
                  <td>
                    <button className="btn btn-sm btn-outline-primary">View</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
