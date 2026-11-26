// Auth service
import api from './api'

export const register = (email: string, password: string, fullName?: string) =>
  api.post('/auth/register', { email, password, full_name: fullName })

export const login = (email: string, password: string) =>
  api.post('/auth/login', { email, password })

export const getMe = () => api.get('/auth/me')
