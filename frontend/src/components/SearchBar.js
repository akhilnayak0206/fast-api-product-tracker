import React, { useState, useEffect, useRef } from "react";

const SearchBar = ({ 
  filter, 
  setFilter, 
  totalProducts,
  onAiSearch 
}) => {
  const [aiSearchQuery, setAiSearchQuery] = useState("");
  const [aiSearchLoading, setAiSearchLoading] = useState(false);
  const abortControllerRef = useRef(null);
  const debounceTimerRef = useRef(null);
  const MIN_CHARS = 3;

  const handleAiSearchChange = (e) => {
    const query = e.target.value;
    setAiSearchQuery(query);
    
    // Cancel previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    
    // Clear debounce timer
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    
    if (!query.trim() || query.length < MIN_CHARS) {
      onAiSearch("");
      setAiSearchLoading(false);
      return;
    }
    
    // Debounce API call
    setAiSearchLoading(true);
    debounceTimerRef.current = setTimeout(async () => {
      try {
        abortControllerRef.current = new AbortController();
        await onAiSearch(query, abortControllerRef.current.signal);
      } catch (error) {
        if (error.name !== 'AbortError') {
          console.error('AI search failed:', error);
        }
      } finally {
        setAiSearchLoading(false);
        // Only clear if this is still the current controller
        if (abortControllerRef.current?.signal.aborted) {
          abortControllerRef.current = null;
        }
      }
    }, 500); // 500ms debounce
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
        <div className="ai-search-form">
          <input
            type="text"
            placeholder={`AI Search... describe what you're looking for (min ${MIN_CHARS} chars)`}
            value={aiSearchQuery}
            onChange={handleAiSearchChange}
          />
          {aiSearchLoading && (
            <div className="ai-search-indicator">Searching...</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SearchBar;
