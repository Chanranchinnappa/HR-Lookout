import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Create axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
const TOKEN_KEY = 'hr_lookout_token';

export const tokenManager = {
  get: () => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem(TOKEN_KEY);
    }
    return null;
  },
  set: (token: string) => {
    if (typeof window !== 'undefined') {
      localStorage.setItem(TOKEN_KEY, token);
    }
  },
  remove: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem(TOKEN_KEY);
    }
  },
};

// Request interceptor to add token to headers
apiClient.interceptors.request.use(
  (config) => {
    const token = tokenManager.get();
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      tokenManager.remove();
      // Redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// Authentication API
export const authApi = {
  login: async (username: string, password: string) => {
    const response = await apiClient.post('/auth/login/', { username, password });
    if (response.data.token) {
      tokenManager.set(response.data.token);
    }
    return response;
  },
  logout: async () => {
    try {
      await apiClient.post('/auth/logout/');
    } finally {
      tokenManager.remove();
    }
  },
  getCurrentUser: () => apiClient.get('/auth/me/'),
  getUserProfile: () => apiClient.get('/auth/profile/'),
};

// Organizations API
export const organizationsApi = {
  getAll: (params?: any) => apiClient.get('/organizations/', { params }),
  getById: (id: number) => apiClient.get(`/organizations/${id}/`),
  create: (data: any) => apiClient.post('/organizations/', data),
  update: (id: number, data: any) => apiClient.put(`/organizations/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/organizations/${id}/`),
};

// Departments API
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

// Employees API
export const employeesApi = {
  getAll: (params?: any) => apiClient.get('/employees/', { params }),
  getById: (id: number) => apiClient.get(`/employees/${id}/`),
  create: (data: any) => apiClient.post('/employees/', data),
  update: (id: number, data: any) => apiClient.put(`/employees/${id}/`, data),
  delete: (id: number) => apiClient.delete(`/employees/${id}/`),
};

export default apiClient;
