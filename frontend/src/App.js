import React, { useEffect, useState, useMemo } from "react";
import "./App.css";
import TaglineSection from "./TaglineSection";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import ProductForm from "./components/ProductForm";
import ProductTable from "./components/ProductTable";
import Footer from "./components/Footer";
import { productAPI, aiAPI } from "./api/api";

function App() {
  const [products, setProducts] = useState([]);
  const [editId, setEditId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState("");
  const [aiSearchResults, setAiSearchResults] = useState([]);
  const [aiSearchLoading, setAiSearchLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("products"); // "products" or "ai-search"
  const [sortField, setSortField] = useState("id");
  const [sortDirection, setSortDirection] = useState("asc");


  // Fetch all products
  const fetchProducts = async () => {
    setLoading(true);
    try {
      const res = await productAPI.getAll();
      setProducts(res.data.products || res.data);
    } catch (err) {
      console.error("Failed to fetch products:", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  // Handle sorting
  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  // Derived list with filter and sorting
  const filteredProducts = useMemo(() => {
    let filtered = products;
    
    // Apply filter
    const q = filter.trim().toLowerCase();
    if (q) {
      filtered = products.filter((p) =>
        String(p.id).includes(q) ||
        p.name?.toLowerCase().includes(q) ||
        p.description?.toLowerCase().includes(q)
      );
    }
    
    // Apply sorting
    return filtered.sort((a, b) => {
      let aVal = a[sortField];
      let bVal = b[sortField];
      
      // Handle numeric fields
      if (sortField === "id" || sortField === "price" || sortField === "quantity") {
        aVal = Number(aVal);
        bVal = Number(bVal);
      } else {
        // Handle string fields
        aVal = String(aVal).toLowerCase();
        bVal = String(bVal).toLowerCase();
      }
      
      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [products, filter, sortField, sortDirection]);

  // AI search results with sorting
  const sortedAiResults = useMemo(() => {
    return aiSearchResults.sort((a, b) => {
      let aVal = a[sortField];
      let bVal = b[sortField];
      
      if (sortField === "id" || sortField === "price" || sortField === "quantity") {
        aVal = Number(aVal);
        bVal = Number(bVal);
      } else {
        aVal = String(aVal).toLowerCase();
        bVal = String(bVal).toLowerCase();
      }
      
      if (aVal < bVal) return sortDirection === "asc" ? -1 : 1;
      if (aVal > bVal) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [aiSearchResults, sortField, sortDirection]);

  // Handle form input
  const handleEdit = (product) => {
    setEditId(product.id);
  };

  // Reset form
  const resetForm = () => {
    setEditId(null);
  };

  // Create or update product
  const handleProductSubmit = async (formData) => {
    setLoading(true);
    try {
      if (editId) {
        await productAPI.update(editId, formData);
      } else {
        await productAPI.create(formData);
      }
      resetForm();
      fetchProducts();
    } finally {
      setLoading(false);
    }
  };

  // Handle AI search
  const handleAiSearch = async (query, signal = null) => {
    if (!query.trim()) {
      setAiSearchResults([]);
      return;
    }
    
    try {
      const res = await aiAPI.search(query, signal);
      if (!signal?.aborted) {
        setAiSearchResults(res.data.products || []);
        setActiveTab("ai-search"); // Switch to AI search tab when results are available
      }
    } catch (err) {
      if (!signal?.aborted && err.name !== 'AbortError') {
        console.error("AI search failed:", err);
        setAiSearchResults([]);
      }
    }
  };

  // Delete product
  const handleDelete = async (id) => {
    const ok = window.confirm("Delete this product?");
    if (!ok) return;
    
    setLoading(true);
    try {
      await productAPI.delete(id);
      fetchProducts();
    } catch (err) {
      console.error("Delete failed:", err);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="app-bg">
      <Header onRefresh={fetchProducts} loading={loading} />

      <div className="container">
        <SearchBar 
          filter={filter}
          setFilter={setFilter}
          totalProducts={products.length}
          onAiSearch={handleAiSearch}
        />

        <div className="content-grid">
          <ProductForm 
            editId={editId}
            loading={loading}
            onSubmit={handleProductSubmit}
            onCancel={resetForm}
          />
          
          <TaglineSection />

          {/* Tab Navigation */}
          <div className="tabs-container">
            <div className="tabs">
              <button 
                className={`tab-button ${activeTab === "products" ? "active" : ""}`}
                onClick={() => setActiveTab("products")}
              >
                All Products ({products.length})
              </button>
              <button 
                className={`tab-button ${activeTab === "ai-search" ? "active" : ""}`}
                onClick={() => setActiveTab("ai-search")}
              >
                AI Search Results ({aiSearchResults.length})
              </button>
            </div>
          </div>

          {/* Tab Content */}
          {activeTab === "products" && (
            <ProductTable 
              products={filteredProducts}
              loading={loading}
              sortField={sortField}
              sortDirection={sortDirection}
              onSort={handleSort}
              onEdit={handleEdit}
              onDelete={handleDelete}
              isAiSearch={false}
            />
          )}
          
          {activeTab === "ai-search" && (
            <ProductTable 
              products={sortedAiResults}
              loading={aiSearchLoading}
              sortField={sortField}
              sortDirection={sortDirection}
              onSort={handleSort}
              onEdit={handleEdit}
              onDelete={handleDelete}
              isAiSearch={true}
            />
          )}
        </div>
      </div>
      
      <Footer />
    </div>
  );
}

export default App;
