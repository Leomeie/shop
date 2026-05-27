import type { ApiResponse, PaginatedResponse } from './types'

export interface OrderItem {
  id: number
  product_name: string
  sku_name: string
  price: number
  price_yuan: number
  download_count: number
  download_token: string
}

export interface OrderListItem {
  id: number
  order_no: string
  pay_amount: number
  pay_amount_yuan: number
  status: string
  status_display: string
  items: OrderItem[]
  created_at: string
}

export interface OrderDetail {
  id: number
  order_no: string
  total_amount: number
  total_amount_yuan: number
  discount_amount: number
  discount_amount_yuan: number
  pay_amount: number
  pay_amount_yuan: number
  status: string
  status_display: string
  remark: string
  pay_time: string | null
  complete_time: string | null
  items: OrderItem[]
  created_at: string
}

export interface OrderCreatePayload {
  remark?: string
}

export interface OrderListParams {
  page?: number
  status?: string
}

export interface DownloadItem {
  id: number
  order_no: string
  product_name: string
  sku_name: string
  download_token: string
  created_at: string
}

export function createOrder(data?: OrderCreatePayload): Promise<ApiResponse<OrderDetail>>
export function getOrders(params?: OrderListParams): Promise<ApiResponse<PaginatedResponse<OrderListItem>>>
export function getOrder(id: number): Promise<ApiResponse<OrderDetail>>
export function cancelOrder(id: number): Promise<ApiResponse<OrderDetail>>
export function getDownloads(params?: { page?: number }): Promise<ApiResponse<PaginatedResponse<DownloadItem>>>
export function getDownloadToken(orderId: number, itemId: number): Promise<ApiResponse<{ download_url: string }>>
