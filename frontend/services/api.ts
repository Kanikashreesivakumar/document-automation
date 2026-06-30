import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
});

// Add a request interceptor
api.interceptors.request.use((config) => {
  console.log(`[Frontend Request] ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
  return config;
}, (error) => {
  return Promise.reject(error);
});

// Add a response interceptor
api.interceptors.response.use((response) => {
  console.log(`[Frontend Response] Status: ${response.status} for URL: ${response.config.url}`);
  console.log(`[Frontend Response Data]`, response.data);
  return response;
}, (error) => {
  console.log(`[Frontend Error]`, error);
  return Promise.reject(error);
});

export default api;
