import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const organizationsApi = {
  getAll: (params?: any) => apiClient.get('/organizations/', { params }),
  getById: (id: number) => apiClient.get(`/organizations/${id}/`),
  create: (data: any) => apiClient.post('/organizations/', data),
  update: (id: number, data: any) => apiClient.put(`/organizations/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/organizations/${id}/`),
};

export const departmentsApi = {
  getAll: (params?: any) => apiClient.get('/departments/', { params }),
  getById: (id: number) => apiClient.get(`/departments/${id}/`),
  create: (data: any) => apiClient.post('/departments/', data),
  update: (id: number, data: any) => apiClient.put(`/departments/${id}/`, data),
  delete: (id: number, params?: { force?: boolean }) => {
    const queryParams = params?.force ? '?force=true' : '';
    return apiClient.delete(`/departments/${id}/${queryParams}`);
  },
};

export const employeesApi = {
  getAll: (params?: any) => apiClient.get('/employees/', { params }),
  getById: (id: number) => apiClient.get(`/employees/${id}/`),
  create: (data: any) => apiClient.post('/employees/', data),
  update: (id: number, data: any) => apiClient.put(`/employees/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/employees/${id}/`),
};
