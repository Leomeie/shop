import request from '../utils/request'

export const createPayment = (data) => request.post('/payment/create/', data)
export const queryPayment = (paymentNo) => request.get(`/payment/${paymentNo}/`)
export const paymentCallback = (data) => request.post('/payment/callback/', data)
