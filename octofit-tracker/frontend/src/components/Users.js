import React, { useEffect, useState, useCallback } from 'react';

function buildBaseUrl() {
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  if (codespace) return `https://${codespace}-8000.app.github.dev`;
  return `${window.location.protocol}//${window.location.host}`;
}

export default function Users() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(() => {
    setLoading(true);
    const base = buildBaseUrl();
    const endpoint = `${base}/api/users/`;
    console.log('Fetching Users from', endpoint);

    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        console.log('Users response:', data);
        const payload = data && data.results ? data.results : data || [];
        setItems(payload);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching users', err);
        setError(err.toString());
        setLoading(false);
      });
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="card card-table">
      <div className="card-body">
        <div className="header-row mb-3">
          <h2 className="h4">Users</h2>
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
                <th>Username</th>
                <th>Email</th>
                <th>Joined</th>
              </tr>
            </thead>
            <tbody>
              {loading && (<tr><td colSpan="4">Loading...</td></tr>)}
              {!loading && items.length === 0 && (<tr><td colSpan="4">No users found.</td></tr>)}
              {items.map((u, idx) => (
                <tr key={u.id || idx}>
                  <td>{u.id || idx}</td>
                  <td>{u.username}</td>
                  <td>{u.email}</td>
                  <td>{u.date_joined ? new Date(u.date_joined).toLocaleString() : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
