import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // Django API URL
});

export const getProducts = (params = {}) => api.get('products/', { params });