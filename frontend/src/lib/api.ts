import axios from 'axios';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Chat
  sendChatMessage: async (data: {
    message: string;
    conversation_id?: string | null;
    jurisdiction: string;
    selected_country?: string | null;
    language: string;
  }) => {
    const res = await apiClient.post('/chat', data);
    return res.data;
  },

  // Classification
  classifyProduct: async (data: any) => {
    const res = await apiClient.post('/classify', data);
    return res.data;
  },

  // ABS
  assessABS: async (data: any) => {
    const res = await apiClient.post('/abs/assessment', data);
    return res.data;
  },

  // IP Strategy
  assessIPStrategy: async (data: any) => {
    const res = await apiClient.post('/ip/assessment', data);
    return res.data;
  },

  // Products
  getProducts: async () => {
    const res = await apiClient.get('/products');
    return res.data;
  },

  createProduct: async (data: any) => {
    const res = await apiClient.post('/products', data);
    return res.data;
  },

  deleteProduct: async (id: string) => {
    const res = await apiClient.delete(`/products/${id}`);
    return res.data;
  },

  // Documents
  getDocuments: async () => {
    const res = await apiClient.get('/documents');
    return res.data;
  },

  uploadDocument: async (formData: FormData) => {
    const res = await apiClient.post('/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  // Sources & Authoritative Registry
  getSources: async (params?: { jurisdiction?: string; domain?: string }) => {
    const res = await apiClient.get('/sources', { params });
    return res.data;
  },

  discoverSources: async () => {
    const res = await apiClient.get('/sources/discover');
    return res.data;
  },

  downloadSource: async (sourceId: string) => {
    const res = await apiClient.post(`/sources/${sourceId}/download`);
    return res.data;
  },

  validateSource: async (sourceId: string) => {
    const res = await apiClient.post(`/sources/${sourceId}/validate`);
    return res.data;
  },

  ingestSource: async (sourceId: string) => {
    const res = await apiClient.post(`/sources/${sourceId}/ingest`);
    return res.data;
  },

  syncCheckSources: async () => {
    const res = await apiClient.post('/sources/sync-check');
    return res.data;
  },

  getSourceChunks: async (sourceId: string) => {
    const res = await apiClient.get(`/sources/${sourceId}/chunks`);
    return res.data;
  },

  getSourceVersions: async (sourceId: string) => {
    const res = await apiClient.get(`/sources/${sourceId}/versions`);
    return res.data;
  },

  // Escalation
  createEscalation: async (data: any) => {
    const res = await apiClient.post('/escalations', data);
    return res.data;
  },

  getEscalations: async () => {
    const res = await apiClient.get('/escalations');
    return res.data;
  },

  updateEscalation: async (id: string, data: any) => {
    const res = await apiClient.patch(`/escalations/${id}`, data);
    return res.data;
  },

  // Admin & Health
  getAdminStats: async () => {
    const res = await apiClient.get('/admin/stats');
    return res.data;
  },

  getSystemHealth: async () => {
    const res = await apiClient.get('/admin/health');
    return res.data;
  },

  runBenchmark: async () => {
    const res = await apiClient.post('/evaluation/run-benchmark');
    return res.data;
  },
};
