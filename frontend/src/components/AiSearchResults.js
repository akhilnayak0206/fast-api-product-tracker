import React from "react";

const AiSearchResults = ({ 
  showAiResults, 
  aiSearchResults, 
  onClear, 
  onEdit, 
  onDelete 
}) => {
  const currency = (n) =>
    typeof n === "number" ? n.toFixed(2) : Number(n || 0).toFixed(2);

  if (!showAiResults) return null;

  return (
    <div className="card ai-results-card">
      <div className="ai-results-header">
        <h2>AI Search Results</h2>
        <button 
          className="btn btn-secondary"
          onClick={onClear}
        >
          Clear
        </button>
      </div>
      <div className="scroll-x">
        <table className="product-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Price</th>
              <th>Quantity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {aiSearchResults.map((p) => (
              <tr key={p.id}>
                <td>{p.id}</td>
                <td className="name-cell">{p.name}</td>
                <td className="desc-cell" title={p.description}>{p.description}</td>
                <td className="price-cell">${currency(p.price)}</td>
                <td>
                  <span className="qty-badge">{p.quantity}</span>
                </td>
                <td>
                  <div className="row-actions">
                    <button className="btn btn-edit" onClick={() => onEdit(p)}>
                      Edit
                    </button>
                    <button className="btn btn-delete" onClick={() => onDelete(p.id)}>
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {aiSearchResults.length === 0 && (
              <tr>
                <td colSpan={6} className="empty">
                  No products found matching your AI search.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AiSearchResults;
