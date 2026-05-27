import { ref, watchEffect } from 'vue'

const STORAGE_KEY = 'shopease-theme'
const THEME_LIGHT = 'light'
const THEME_DARK = 'dark'

const theme = ref(THEME_DARK)
let initialized = false

function getSystemPreference() {
  return window.matchMedia('(prefers-color-scheme: light)').matches ? THEME_LIGHT : THEME_DARK
}

function applyTheme(t) {
  document.documentElement.setAttribute('data-theme', t)
}

function initTheme() {
  if (initialized) return
  initialized = true

  const saved = localStorage.getItem(STORAGE_KEY)
  theme.value = saved || getSystemPreference()
  applyTheme(theme.value)

  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
    if (!localStorage.getItem(STORAGE_KEY)) {
      theme.value = e.matches ? THEME_LIGHT : THEME_DARK
      applyTheme(theme.value)
    }
  })
}

export function useTheme() {
  initTheme()

  watchEffect(() => {
    applyTheme(theme.value)
  })

  function toggle() {
    theme.value = theme.value === THEME_DARK ? THEME_LIGHT : THEME_DARK
    localStorage.setItem(STORAGE_KEY, theme.value)
  }

  function set(t) {
    theme.value = t
    localStorage.setItem(STORAGE_KEY, t)
  }

  const isDark = () => theme.value === THEME_DARK

  return { theme, toggle, set, isDark }
}
