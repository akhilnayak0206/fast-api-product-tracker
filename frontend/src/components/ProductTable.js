import React from "react";

const ProductTable = ({ 
  products, 
  loading, 
  sortField, 
  sortDirection, 
  onSort, 
  onEdit, 
  onDelete 
}) => {
  const currency = (n) =>
    typeof n === "number" ? n.toFixed(2) : Number(n || 0).toFixed(2);

  return (
    <div className="card list-card">
      <h2>Products</h2>
      {loading ? (
        <div className="loader">Loading...</div>
      ) : (
        <div className="scroll-x">
          <table className="product-table">
            <thead>
              <tr>
                <th 
                  className={`sortable ${sortField === 'id' ? `sort-${sortDirection}` : ''}`}
                  onClick={() => onSort('id')}
                >
                  ID
                </th>
                <th 
                  className={`sortable ${sortField === 'name' ? `sort-${sortDirection}` : ''}`}
                  onClick={() => onSort('name')}
                >
                  Name
                </th>
                <th>Description</th>
                <th 
                  className={`sortable ${sortField === 'price' ? `sort-${sortDirection}` : ''}`}
                  onClick={() => onSort('price')}
                >
                  Price
                </th>
                <th 
                  className={`sortable ${sortField === 'quantity' ? `sort-${sortDirection}` : ''}`}
                  onClick={() => onSort('quantity')}
                >
                  Quantity
                </th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map((p) => (
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
              {products.length === 0 && (
                <tr>
                  <td colSpan={6} className="empty">
                    No products found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ProductTable;
