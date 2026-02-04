import React, { useEffect, useState, useCallback } from 'react';

function buildBaseUrl() {
  const codespace = process.env.REACT_APP_CODESPACE_NAME;
  if (codespace) return `https://${codespace}-8000.app.github.dev`;
  return `${window.location.protocol}//${window.location.host}`;
}

export default function Teams() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(() => {
    setLoading(true);
    const base = buildBaseUrl();
    const endpoint = `${base}/api/teams/`;
    console.log('Fetching Teams from', endpoint);

    fetch(endpoint)
      .then(res => res.json())
      .then(data => {
        console.log('Teams response:', data);
        const payload = data && data.results ? data.results : data || [];
        setItems(payload);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching teams', err);
        setError(err.toString());
        setLoading(false);
      });
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  return (
    <div className="card card-table">
      <div className="card-body">
        <div className="header-row mb-3">
          <h2 className="h4">Teams</h2>
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
                <th>Name</th>
                <th>Members</th>
                <th>Created By</th>
                <th>Created At</th>
              </tr>
            </thead>
            <tbody>
              {loading && (<tr><td colSpan="5">Loading...</td></tr>)}
              {!loading && items.length === 0 && (<tr><td colSpan="5">No teams found.</td></tr>)}
              {items.map((t, idx) => (
                <tr key={t.id || idx}>
                  <td>{t.id || idx}</td>
                  <td>{t.name}</td>
                  <td>{t.members?.length ?? 'N/A'}</td>
                  <td>{t.created_by?.username || t.created_by || 'N/A'}</td>
                  <td>{t.created_at ? new Date(t.created_at).toLocaleString() : '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
