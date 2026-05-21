import request from '../utils/request'

export const getProducts = (params) => request.get('/products/', { params })
export const getProduct = (id) => request.get(`/products/${id}/`)
export const getCategories = () => request.get('/products/categories/')
export const getCategoriesFlat = () => request.get('/products/categories/flat/')
