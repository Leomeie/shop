import type { ApiResponse, PaginatedResponse } from './types'
import type { ProductListItem, ProductDetail, SKU, ProductImage, Category } from './product'

export interface AdminProductListParams {
  page?: number
  status?: string
  category?: number
  search?: string
}

export interface AdminProductCreatePayload {
  name: string
  category: number
  description: string
  main_image?: string
  file?: string
  demo_file?: string
  version?: string
  changelog?: string
  status?: string
  is_featured?: boolean
}

export interface AdminBatchPayload {
  action: string
  ids: number[]
}

export interface AdminCategoryCreatePayload {
  name: string
  parent?: number | null
  icon?: string
  sort_order?: number
}

export interface AdminSkuCreatePayload {
  name: string
  price: number
  original_price?: number
  license_description?: string
  sort_order?: number
  is_active?: boolean
}

export function getAdminProducts(params?: AdminProductListParams): Promise<ApiResponse<PaginatedResponse<ProductListItem>>>
export function getAdminProduct(id: number): Promise<ApiResponse<ProductDetail>>
export function createAdminProduct(data: AdminProductCreatePayload): Promise<ApiResponse<ProductDetail>>
export function updateAdminProduct(id: number, data: Partial<AdminProductCreatePayload>): Promise<ApiResponse<ProductDetail>>
export function deleteAdminProduct(id: number): Promise<ApiResponse<null>>
export function batchAdminProducts(data: AdminBatchPayload): Promise<ApiResponse<null>>

export function getAdminCategories(): Promise<ApiResponse<Category[]>>
export function createAdminCategory(data: AdminCategoryCreatePayload): Promise<ApiResponse<Category>>

export function createAdminProductImage(productId: number, data: FormData): Promise<ApiResponse<ProductImage>>
export function deleteAdminProductImage(productId: number, imageId: number): Promise<ApiResponse<null>>

export function createAdminSku(productId: number, data: AdminSkuCreatePayload): Promise<ApiResponse<SKU>>
export function updateAdminSku(productId: number, skuId: number, data: Partial<AdminSkuCreatePayload>): Promise<ApiResponse<SKU>>
export function deleteAdminSku(productId: number, skuId: number): Promise<ApiResponse<null>>
