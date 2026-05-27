import type { ApiResponse, PaginatedResponse } from './types'

export interface Category {
  id: number
  name: string
  parent: number | null
  level: number
  icon: string | null
  sort_order: number
  is_active: boolean
  children?: Category[]
}

export interface CategoryFlat {
  id: number
  name: string
  parent: number | null
  level: number
  icon: string | null
}

export interface ProductListItem {
  id: number
  name: string
  category: number
  category_name: string
  main_image: string
  min_price_yuan: number
  download_count: number
  view_count: number
  is_featured: boolean
  status: string
  created_at: string
}

export interface SKU {
  id: number
  name: string
  price: number
  original_price: number | null
  price_yuan: number
  original_price_yuan: number | null
  license_description: string
  sort_order: number
  is_active: boolean
}

export interface ProductImage {
  id: number
  image: string
  sort_order: number
}

export interface ProductDetail {
  id: number
  name: string
  category: number
  category_name: string
  description: string
  main_image: string
  demo_file: string | null
  version: string
  changelog: string
  status: string
  is_featured: boolean
  download_count: number
  view_count: number
  min_price_yuan: number
  images: ProductImage[]
  skus: SKU[]
  created_at: string
  updated_at: string
}

export interface ProductListParams {
  page?: number
  page_size?: number
  category?: number
  is_featured?: boolean
  search?: string
  ordering?: string
  min_price?: number
  max_price?: number
}

export function getProducts(params?: ProductListParams): Promise<ApiResponse<PaginatedResponse<ProductListItem>>>
export function getProduct(id: number): Promise<ApiResponse<ProductDetail>>
export function getCategories(): Promise<ApiResponse<Category[]>>
export function getCategoriesFlat(): Promise<ApiResponse<CategoryFlat[]>>
