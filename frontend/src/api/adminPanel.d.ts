import type { ApiResponse, PaginatedResponse } from './types'
import type { OrderListItem } from './order'
import type { UserData } from './user'

export interface AdminOrderListParams {
  page?: number
  status?: string
}

export interface AdminUserListParams {
  page?: number
  search?: string
}

export function getAdminOrders(params?: AdminOrderListParams): Promise<ApiResponse<PaginatedResponse<OrderListItem>>>
export function getAdminOrder(id: number): Promise<ApiResponse<OrderListItem>>

export function getAdminUsers(params?: AdminUserListParams): Promise<ApiResponse<PaginatedResponse<UserData>>>
export function getAdminUser(id: number): Promise<ApiResponse<UserData>>
