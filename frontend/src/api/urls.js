// API Base URL and Endpoints
const API_BASE_URL = "http://localhost:8000";

export const API_URLS = {
  // Base URL
  BASE_URL: API_BASE_URL,
  
  // Product endpoints
  PRODUCTS: `${API_BASE_URL}/api/v1/products`,
  PRODUCT_BY_ID: (id) => `${API_BASE_URL}/api/v1/products/${id}`,
  
  // AI Search endpoint (if exists)
  AI_SEARCH: `${API_BASE_URL}/api/v1/product/ai-search`,
};
