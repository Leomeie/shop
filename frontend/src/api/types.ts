// Shared types for API responses

/** Standard API response wrapper */
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

/** Paginated list response */
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}
