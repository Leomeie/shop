import request from '../utils/request'

export const register = (data) => request.post('/auth/register/', data)
export const login = (data) => request.post('/auth/login/', data)
export const refreshToken = (data) => request.post('/auth/token/refresh/', data)
export const getUserInfo = () => request.get('/auth/me/')
export const updateUserInfo = (data) => request.patch('/auth/me/', data)
