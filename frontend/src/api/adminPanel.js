import request from '../utils/request'

export const getAdminOrders = (params) => request.get('/admin/orders/', { params })
export const getAdminOrder = (id) => request.get(`/admin/orders/${id}/`)

export const getAdminUsers = (params) => request.get('/admin/users/', { params })
export const getAdminUser = (id) => request.get(`/admin/users/${id}/`)
