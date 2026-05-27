import type { ApiResponse } from './types'

export interface UserData {
  id: number
  username: string
  nickname: string | null
  phone: string | null
  avatar: string | null
  date_joined: string
  is_staff: boolean
  is_superuser: boolean
  is_active: boolean
}

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  password: string
  password_confirm: string
}

export interface AuthTokens {
  access: string
  refresh: string
  user: UserData
}

export function register(data: RegisterData): Promise<ApiResponse<AuthTokens>>
export function login(data: LoginData): Promise<ApiResponse<AuthTokens>>
export function refreshToken(data: { refresh: string }): Promise<ApiResponse<{ access: string }>>
export function getUserInfo(): Promise<ApiResponse<UserData>>
export function updateUserInfo(data: Partial<Pick<UserData, 'nickname' | 'phone' | 'avatar'>>): Promise<ApiResponse<UserData>>
