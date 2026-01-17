import React, { useState } from "react";

const SearchBar = ({ 
  filter, 
  setFilter, 
  totalProducts,
  onAiSearch 
}) => {
  const [aiSearchQuery, setAiSearchQuery] = useState("");
  const [aiSearchLoading, setAiSearchLoading] = useState(false);

  const handleAiSearchChange = (e) => {
    setAiSearchQuery(e.target.value);
    if (!e.target.value.trim()) {
      onAiSearch("", []);
    }
  };

  const handleAiSearchSubmit = async (e) => {
    e.preventDefault();
    if (!aiSearchQuery.trim()) return;
    
    setAiSearchLoading(true);
    try {
      await onAiSearch(aiSearchQuery);
    } finally {
      setAiSearchLoading(false);
    }
  };

  return (
    <div className="stats">
      <div className="chip">Total: {totalProducts}</div>
      <div className="search">
        <input
          type="text"
          placeholder="Search by id, name or description..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
      </div>
      <div className="ai-search">
        <form onSubmit={handleAiSearchSubmit} className="ai-search-form">
          <input
            type="text"
            placeholder="AI Search... describe what you're looking for"
            value={aiSearchQuery}
            onChange={handleAiSearchChange}
            disabled={aiSearchLoading}
          />
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={aiSearchLoading || !aiSearchQuery.trim()}
          >
            {aiSearchLoading ? "Searching..." : "AI Search"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default SearchBar;
