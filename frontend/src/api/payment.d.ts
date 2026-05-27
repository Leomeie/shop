import type { ApiResponse } from './types'

export interface PaymentData {
  payment_no: string
  pay_url: string
  method: string
  status: string
}

export interface PaymentCreatePayload {
  order_id: number
  method: string
}

export interface PaymentQueryResult {
  payment_no: string
  status: string
  order_no: string
}

export interface PaymentCallbackPayload {
  payment_no: string
  status: string
}

export function createPayment(data: PaymentCreatePayload): Promise<ApiResponse<PaymentData>>
export function queryPayment(paymentNo: string): Promise<ApiResponse<PaymentQueryResult>>
export function paymentCallback(data: PaymentCallbackPayload): Promise<ApiResponse<null>>
