import request from '../utils/request'

export const createOrder = (data) => request.post('/orders/create/', data)
export const getOrders = (params) => request.get('/orders/', { params })
export const getOrder = (id) => request.get(`/orders/${id}/`)
export const cancelOrder = (id) => request.post(`/orders/${id}/cancel/`)
export const getDownloads = (params) => request.get('/orders/downloads/', { params })
export const getDownloadToken = (orderId, itemId) => request.get(`/orders/${orderId}/items/${itemId}/download/`)
