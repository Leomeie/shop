import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, register as registerApi, getUserInfo } from '../api/user'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const refreshTokenVal = ref(localStorage.getItem('refresh_token') || '')
  const userInfo = ref(null)

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.is_staff || false)

  function setTokens(access, refresh) {
    token.value = access
    refreshTokenVal.value = refresh
    localStorage.setItem('token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  function logout() {
    token.value = ''
    refreshTokenVal.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
  }

  async function login(data) {
    const res = await loginApi(data)
    setTokens(res.data.access, res.data.refresh)
    userInfo.value = res.data.user
    return res
  }

  async function register(data) {
    const res = await registerApi(data)
    setTokens(res.data.access, res.data.refresh)
    userInfo.value = res.data.user
    return res
  }

  async function fetchUserInfo() {
    const res = await getUserInfo()
    userInfo.value = res.data
    return res.data
  }

  return { token, refreshTokenVal, userInfo, isLoggedIn, isAdmin, login, register, logout, fetchUserInfo, setTokens }
})
