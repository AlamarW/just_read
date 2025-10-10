import { useState, useEffect } from 'react';

function TextualItemsList({ projectId }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const url = projectId
          ? `http://localhost:8000/api/textual-items/?project=${projectId}`
          : 'http://localhost:8000/api/textual-items/';

        const response = await fetch(url);

        if (!response.ok) {
          throw new Error('Failed to fetch items');
        }

        const data = await response.json();
        setItems(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchItems();
  }, [projectId]);

  if (loading) return <div className="loading">Loading books...</div>;
  if (error) return <div className="error">Error: {error}</div>;
  if (items.length === 0) return <div className="empty">No books in this project yet.</div>;

  return (
    <div className="textual-items-list">
      <h2>Reading List</h2>
      <div className="items-grid">
        {items.map((item) => (
          <div key={item.title} className="item-card">
            <h3>{item.title}</h3>
            <p className="author">by {item.author}</p>
            <div className="item-details">
              <span className="isbn">ISBN: {item.isbn}</span>
              <span className="pages">{item.total_pages} pages</span>
            </div>
            <div className="progress">
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${item.progress_percent}%` }}
                />
              </div>
              <span>{item.progress_percent}% complete</span>
            </div>
            <span className={`status status-${item.status.toLowerCase().replace(' ', '-')}`}>
              {item.status}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default TextualItemsList;
