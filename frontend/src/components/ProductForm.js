import React, { useState, useEffect } from "react";
import { productAPI } from "../api/api";

const ProductForm = ({ 
  editId, 
  loading, 
  onSubmit, 
  onCancel 
}) => {
  const [form, setForm] = useState({
    name: "",
    description: "",
    price: "",
    quantity: "",
  });
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (editId) {
      const fetchProduct = async () => {
        try {
          const res = await productAPI.getById(editId);
          const product = res.data;
          setForm({
            name: product.name,
            description: product.description,
            price: product.price,
            quantity: product.quantity,
          });
        } catch (err) {
          setError("Failed to fetch product details");
        }
      };
      fetchProduct();
    } else {
      setForm({ name: "", description: "", price: "", quantity: "" });
    }
  }, [editId]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage("");
    setError("");
    
    try {
      await onSubmit({
        ...form,
        price: Number(form.price),
        quantity: Number(form.quantity),
      });
      setForm({ name: "", description: "", price: "", quantity: "" });
      setMessage(editId ? "Product updated successfully" : "Product created successfully");
    } catch (err) {
      setError(err.response?.data?.detail || "Operation failed");
    }
  };

  return (
    <div className="card form-card">
      <h2>{editId ? "Edit Product" : "Add Product"}</h2>
      <form onSubmit={handleSubmit} className="product-form">
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="description"
          placeholder="Description"
          value={form.description}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="price"
          placeholder="Price"
          value={form.price}
          onChange={handleChange}
          required
          step="0.01"
        />
        <input
          type="number"
          name="quantity"
          placeholder="Quantity"
          value={form.quantity}
          onChange={handleChange}
          required
        />
        <div className="form-actions">
          <button className="btn" type="submit" disabled={loading}>
            {editId ? "Update" : "Add"}
          </button>
          {editId && (
            <button
              className="btn btn-secondary"
              type="button"
              onClick={onCancel}
            >
              Cancel
            </button>
          )}
        </div>
      </form>
      {message && <div className="success-msg">{message}</div>}
      {error && <div className="error-msg">{error}</div>}
    </div>
  );
};

export default ProductForm;
