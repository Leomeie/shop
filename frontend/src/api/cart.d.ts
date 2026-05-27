import type { ApiResponse } from './types'

export interface CartItem {
  id: number
  sku_id: number
  product_id: number
  product_name: string
  sku_name: string
  main_image: string
  price_yuan: number
  original_price_yuan: number | null
  quantity: number
  subtotal_yuan: number
  selected: boolean
}

export interface CartData {
  items: CartItem[]
  total_yuan: number
  selected_total_yuan: number
}

export interface CartAddPayload {
  sku_id: number
  quantity?: number
}

export interface CartUpdatePayload {
  quantity?: number
  selected?: boolean
}

export interface CartSelectAllPayload {
  selected: boolean
}

export interface CartRemoveSelectedPayload {
  sku_ids: number[]
}

export function getCart(): Promise<ApiResponse<CartData>>
export function addToCart(data: CartAddPayload): Promise<ApiResponse<CartData>>
export function updateCartItem(skuId: number, data: CartUpdatePayload): Promise<ApiResponse<CartData>>
export function removeCartItem(skuId: number): Promise<ApiResponse<null>>
export function selectAll(data: CartSelectAllPayload): Promise<ApiResponse<CartData>>
export function removeSelected(data: CartRemoveSelectedPayload): Promise<ApiResponse<null>>
export function clearCart(): Promise<ApiResponse<null>>
