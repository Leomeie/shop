import request from '../utils/request'

export const getCart = () => request.get('/cart/')
export const addToCart = (data) => request.post('/cart/items/', data)
export const updateCartItem = (skuId, data) => request.put(`/cart/items/${skuId}/`, data)
export const removeCartItem = (skuId) => request.delete(`/cart/items/${skuId}/`)
export const selectAll = (data) => request.post('/cart/select-all/', data)
export const removeSelected = (data) => request.post('/cart/remove-selected/', data)
export const clearCart = () => request.delete('/cart/')
