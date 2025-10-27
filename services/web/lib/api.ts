//services/web/lib/api.ts

import axios from 'axios';

// API Base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// Create axios instance
export const apiClient = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Organization API
export const organizationsApi = {
  getAll: () => apiClient.get('/organizations/'),
  getById: (id: number) => apiClient.get(`/organizations/${id}/`),
  create: (data: any) => apiClient.post('/organizations/', data),
  update: (id: number, data: any) => apiClient.put(`/organizations/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/organizations/${id}/`),
};

// Employee API
export const employeesApi = {
  getAll: (params?: any) => apiClient.get('/employees/', { params }),
  getById: (id: number) => apiClient.get(`/employees/${id}/`),
  create: (data: any) => apiClient.post('/employees/', data),
  update: (id: number, data: any) => apiClient.put(`/employees/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/employees/${id}/`),
  search: (query: string) => apiClient.get(`/employees/search/?q=${query}`),
};

// Department API - ✅ UPDATED ENDPOINTS
export const departmentsApi = {
  getAll: (params?: any) => apiClient.get('/departments/', { params }),
  getById: (id: number) => apiClient.get(`/departments/${id}/`),
  create: (data: any) => apiClient.post('/departments/', data),
  update: (id: number, data: any) => apiClient.put(`/departments/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/departments/${id}/`),
};

// Health Check API
export const healthApi = {
  check: () => apiClient.get('/health/', { baseURL: API_BASE_URL }),
};
