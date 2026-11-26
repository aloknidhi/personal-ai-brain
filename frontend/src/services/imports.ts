// Import service
import api from './api'

export const importChatGPT = (formData: FormData) =>
  api.post('/imports/import/chatgpt', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

export const syncSource = (sourceId: string) =>
  api.post(`/imports/sources/${sourceId}/sync`)

export const getSourceConversations = (sourceId: string) =>
  api.get(`/imports/sources/${sourceId}/conversations`)

export const analyzeSelected = (conversationIds: string[]) =>
  api.post('/analysis/analyze-selected', conversationIds)

export const listAnalyses = () => api.get('/analysis/')
