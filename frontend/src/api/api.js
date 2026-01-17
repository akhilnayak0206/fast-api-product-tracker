import axios from "axios";
import { API_URLS } from "./urls";

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URLS.BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// API functions for products
export const productAPI = {
  // Get all products
  getAll: () => api.get(API_URLS.PRODUCTS),
  
  // Get product by ID
  getById: (id) => api.get(API_URLS.PRODUCT_BY_ID(id)),
  
  // Create new product
  create: (data) => api.post(API_URLS.PRODUCTS, data),
  
  // Update product
  update: (id, data) => api.put(API_URLS.PRODUCT_BY_ID(id), data),
  
  // Delete product
  delete: (id) => api.delete(API_URLS.PRODUCT_BY_ID(id)),
};

// AI Search API (if available)
export const aiAPI = {
  search: (query, signal = null) => {
    return api.post(API_URLS.AI_SEARCH, { user_query: query }, { 
      signal,
      headers: {
        'Content-Type': 'application/json',
      }
    });
  },
};

export default api;
