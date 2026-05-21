import request from '../utils/request'

export const getAdminProducts = (params) => request.get('/products/admin/', { params })
export const getAdminProduct = (id) => request.get(`/products/admin/${id}/`)
export const createAdminProduct = (data) => request.post('/products/admin/', data)
export const updateAdminProduct = (id, data) => request.patch(`/products/admin/${id}/`, data)
export const deleteAdminProduct = (id) => request.delete(`/products/admin/${id}/`)
export const batchAdminProducts = (data) => request.post('/products/admin/batch/', data)

export const getAdminCategories = () => request.get('/products/admin/categories/')
export const createAdminCategory = (data) => request.post('/products/admin/categories/', data)

export const createAdminProductImage = (productId, data) => request.post(`/products/admin/${productId}/images/`, data)
export const deleteAdminProductImage = (productId, imageId) => request.delete(`/products/admin/${productId}/images/${imageId}/`)

export const createAdminSku = (productId, data) => request.post(`/products/admin/${productId}/skus/`, data)
export const updateAdminSku = (productId, skuId, data) => request.patch(`/products/admin/${productId}/skus/${skuId}/`, data)
export const deleteAdminSku = (productId, skuId) => request.delete(`/products/admin/${productId}/skus/${skuId}/`)
