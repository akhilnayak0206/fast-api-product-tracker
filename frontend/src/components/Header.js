import React from "react";

const Header = ({ onRefresh, loading }) => {
  return (
    <header className="topbar">
      <div className="brand">
        <span className="brand-badge">📦</span>
        <h1>Product Tracker</h1>
      </div>
      <div className="top-actions">
        <button className="btn btn-light" onClick={onRefresh} disabled={loading}>
          Refresh
        </button>
      </div>
    </header>
  );
};

export default Header;
