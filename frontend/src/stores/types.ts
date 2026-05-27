import type { UserData } from '../api/user'
import type { CartItem } from '../api/cart'

export interface UserState {
  token: string
  refreshTokenVal: string
  userInfo: UserData | null
}

export interface CartState {
  items: CartItem[]
  loading: boolean
}

export interface AppState {
  homeSlide: number
}
