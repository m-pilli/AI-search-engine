import axios, { AxiosResponse } from 'axios';
import { 
  SearchResponse, 
  DocumentResponse, 
  SearchStats, 
  HealthStatus,
  Document,
  ApiError 
} from '../types';

// Temporary hardcoded base URL to unblock production while env propagation is fixed
// Replace with process.env.REACT_APP_API_URL when Vercel env is confirmed
const resolvedBaseURL = 'https://overpuissant-gratulatorily-lorenza.ngrok-free.dev/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: resolvedBaseURL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.baseURL}${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Search API
export const searchApi = {
  search: async (
    query: string,
    limit: number = 10,
    alpha: number = 0.7,
    searchType: 'hybrid' | 'semantic' | 'keyword' = 'hybrid'
  ): Promise<SearchResponse> => {
    const params = new URLSearchParams({
      q: query,
      limit: limit.toString(),
      alpha: alpha.toString(),
      type: searchType,
    });

    const response: AxiosResponse<SearchResponse> = await api.get(`/search?${params}`);
    return response.data;
  },

  getSuggestions: async (query: string, limit: number = 5): Promise<string[]> => {
    const params = new URLSearchParams({
      q: query,
      limit: limit.toString(),
    });

    const response: AxiosResponse<{ suggestions: string[] }> = await api.get(`/search/suggestions?${params}`);
    return response.data.suggestions;
  },

  getStats: async (): Promise<SearchStats> => {
    const response: AxiosResponse<SearchStats> = await api.get('/search/stats');
    return response.data;
  },
};

// Documents API
export const documentsApi = {
  getDocuments: async (page: number = 1, perPage: number = 20): Promise<DocumentResponse> => {
    const params = new URLSearchParams({
      page: page.toString(),
      per_page: perPage.toString(),
    });

    const response: AxiosResponse<DocumentResponse> = await api.get(`/documents?${params}`);
    return response.data;
  },

  getDocument: async (id: string): Promise<Document> => {
    const response: AxiosResponse<Document> = await api.get(`/documents/${id}`);
    return response.data;
  },

  addDocument: async (title: string, content: string, metadata: Record<string, any> = {}): Promise<Document> => {
    const response: AxiosResponse<Document> = await api.post('/documents', {
      title,
      content,
      metadata,
    });
    return response.data;
  },

  updateDocument: async (
    id: string,
    title?: string,
    content?: string,
    metadata?: Record<string, any>
  ): Promise<void> => {
    await api.put(`/documents/${id}`, {
      title,
      content,
      metadata,
    });
  },

  deleteDocument: async (id: string): Promise<void> => {
    await api.delete(`/documents/${id}`);
  },

  addDocumentsBatch: async (documents: Array<{
    title: string;
    content: string;
    metadata?: Record<string, any>;
  }>): Promise<{
    added_documents: Document[];
    total_added: number;
    errors: string[];
  }> => {
    const response = await api.post('/documents/batch', { documents });
    return response.data;
  },

  rebuildIndex: async (): Promise<{
    message: string;
    total_documents: number;
  }> => {
    const response = await api.post('/documents/rebuild-index');
    return response.data;
  },
};

// Health API
export const healthApi = {
  getHealth: async (): Promise<HealthStatus> => {
    const response: AxiosResponse<HealthStatus> = await api.get('/health');
    return response.data;
  },

  getDetailedHealth: async (): Promise<HealthStatus> => {
    const response: AxiosResponse<HealthStatus> = await api.get('/health/detailed');
    return response.data;
  },

  getReadiness: async (): Promise<{ status: string; timestamp: number }> => {
    const response = await api.get('/health/ready');
    return response.data;
  },

  getLiveness: async (): Promise<{ status: string; timestamp: number }> => {
    const response = await api.get('/health/live');
    return response.data;
  },
};

// Error handling utility
export const handleApiError = (error: any): ApiError => {
  if (error.response) {
    // Server responded with error status
    return {
      error: error.response.data?.error || 'Server error',
      message: error.response.data?.message,
      status: error.response.status,
    };
  } else if (error.request) {
    // Request was made but no response received
    return {
      error: 'Network error',
      message: 'Unable to connect to the server',
    };
  } else {
    // Something else happened
    return {
      error: 'Request error',
      message: error.message,
    };
  }
};

export default api;

