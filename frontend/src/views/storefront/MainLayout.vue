<template>
  <div class="layout">
    <div v-if="!isHome" class="scroll-progress" :style="{ width: scrollProgress + '%' }" />

    <header :class="navClasses">
      <div class="container nav-inner">
        <router-link to="/" class="logo">
          <span class="logo-mark">S</span>
          <span class="logo-text"><GradientText variant="blue">ShopEase</GradientText></span>
        </router-link>

        <div :class="['nav-search', { 'is-open': searchOpen }]">
          <div class="search-box">
            <AnimatedIcons name="search" :size="18" />
            <input
              v-model="keyword"
              class="search-input"
              type="text"
              placeholder="搜索 Prompt、工作流、模型..."
              @keyup.enter="handleSearch"
            />
          </div>
        </div>

        <nav class="nav-actions">
          <button class="nav-btn" type="button" @click="searchOpen = !searchOpen">
            <AnimatedIcons name="search" :size="18" />
          </button>
          <router-link to="/showcase" class="nav-link">
            <AnimatedIcons name="star" :size="18" />
            <span>商品</span>
          </router-link>

          <router-link to="/categories" class="nav-link">
            <AnimatedIcons name="globe" :size="18" />
            <span>分类</span>
          </router-link>

          <router-link to="/cart" class="nav-btn cart-btn">
            <AnimatedIcons name="cart" :size="20" />
            <Transition name="badge-pop">
              <span v-if="cartStore.count" :key="cartStore.count" class="cart-badge">{{ cartStore.count }}</span>
            </Transition>
          </router-link>

          <template v-if="userStore.isLoggedIn">
            <div class="user-menu" @mouseenter="menuOpen = true" @mouseleave="menuOpen = false">
              <button class="nav-btn user-btn" type="button">
                <div class="user-avatar">
                  {{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}
                </div>
              </button>

              <Transition name="dropdown">
                <div v-if="menuOpen" class="dropdown">
                  <div class="dropdown-header">
                    <div class="dropdown-avatar">
                      {{ userStore.userInfo?.username?.charAt(0)?.toUpperCase() || 'U' }}
                    </div>
                    <div>
                      <div class="dropdown-name">{{ userStore.userInfo?.username || '用户' }}</div>
                      <div class="dropdown-role">{{ userStore.isAdmin ? '管理员' : '会员' }}</div>
                    </div>
                  </div>

                  <div class="dropdown-divider" />

                  <router-link to="/profile" class="dropdown-item" @click="menuOpen = false">
                    <AnimatedIcons name="user" :size="16" />
                    个人中心
                  </router-link>
                  <router-link to="/orders" class="dropdown-item" @click="menuOpen = false">
                    <AnimatedIcons name="package" :size="16" />
                    我的订单
                  </router-link>
                  <router-link to="/downloads" class="dropdown-item" @click="menuOpen = false">
                    <AnimatedIcons name="download" :size="16" />
                    我的下载
                  </router-link>
                  <router-link to="/wishlist" class="dropdown-item" @click="menuOpen = false">
                    <AnimatedIcons name="heart" :size="16" />
                    我的收藏
                  </router-link>
                  <router-link v-if="userStore.isAdmin" to="/admin" class="dropdown-item" @click="menuOpen = false">
                    <AnimatedIcons name="settings" :size="16" />
                    后台管理
                  </router-link>

                  <div class="dropdown-divider" />

                  <button class="dropdown-item dropdown-logout" type="button" @click="handleLogout">
                    <AnimatedIcons name="close" :size="16" />
                    退出登录
                  </button>
                </div>
              </Transition>
            </div>
          </template>

          <template v-else>
            <router-link to="/login" class="nav-btn login-btn">登录</router-link>
          </template>
        </nav>
      </div>
    </header>

    <main :class="['main', { 'main-home': isHome }]">
      <router-view v-slot="{ Component }">
        <Transition name="page" mode="out-in">
          <component :is="Component" />
        </Transition>
      </router-view>
    </main>

    <footer class="footer">
      <div class="container footer-inner">
        <div class="footer-left">
          <div class="footer-brand">
            <span class="logo-mark">S</span>
            <span>ShopEase</span>
          </div>
          <p class="footer-copy">© 2026 ShopEase · AI 数字精品店</p>
        </div>

        <div class="footer-links">
          <router-link to="/categories">分类</router-link>
          <router-link to="/help">帮助中心</router-link>
          <router-link to="/products">全部商品</router-link>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { useCartStore } from '../../stores/cart'
import { useAppStore } from '../../stores/app'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import GradientText from '../../components/GradientText.vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const cartStore = useCartStore()
const appStore = useAppStore()

const keyword = ref('')
const menuOpen = ref(false)
const isScrolled = ref(false)
const scrollProgress = ref(0)
const searchOpen = ref(false)

const isHome = computed(() => route.name === 'Home')
const navHidden = computed(() => isHome.value && appStore.homeSlide === 0)
const isHomeDark = computed(() => isHome.value && (appStore.homeSlide === 1 || appStore.homeSlide === 3))
const isHomeTransparent = computed(() => isHome.value && appStore.homeSlide === 0)
const isHomeLight = computed(() => isHome.value && appStore.homeSlide === 2)

const navClasses = computed(() => [
  'nav',
  {
    scrolled: isScrolled.value && (!isHome.value || isHomeLight.value),
    'nav-home': isHome.value,
    'nav-hidden': navHidden.value,
    'nav-on-dark': isHomeDark.value,
    'nav-transparent': isHomeTransparent.value,
    'nav-home-light': isHomeLight.value,
  },
])

function onScroll() {
  isScrolled.value = window.scrollY > 10
  const docHeight = document.documentElement.scrollHeight - window.innerHeight
  scrollProgress.value = docHeight > 0 ? (window.scrollY / docHeight) * 100 : 0
}

function handleSearch() {
  if (!keyword.value.trim()) return
  router.push({ path: '/products', query: { search: keyword.value.trim() } })
}

function handleLogout() {
  userStore.logout()
  router.push('/')
}

onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })

  if (userStore.isLoggedIn) {
    cartStore.fetchCart()
    if (!userStore.userInfo) userStore.fetchUserInfo().catch(() => {})
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--ink);
}

.scroll-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  z-index: 9999;
  background: linear-gradient(90deg, var(--accent), var(--accent-light));
  box-shadow: 0 0 8px var(--accent-glow);
  transition: width 0.1s linear;
}

.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 40;
  height: var(--nav-h);
  background: var(--glass-bg);
  border-bottom: 1px solid var(--glass-border);
  backdrop-filter: blur(20px) saturate(1.2);
  -webkit-backdrop-filter: blur(20px) saturate(1.2);
  transition:
    background var(--dur-normal) var(--ease-out),
    border-color var(--dur-normal) var(--ease-out),
    box-shadow var(--dur-normal) var(--ease-out),
    transform var(--dur-normal) var(--ease-out);
}

.nav.scrolled {
  box-shadow: var(--glass-shadow);
}

.nav-hidden {
  opacity: 0;
  visibility: hidden;
  pointer-events: none;
  transform: translateY(-100%);
  box-shadow: none;
}

.nav-home.nav-on-dark {
  border-bottom-color: var(--glass-border);
  background: var(--glass-bg);
}

.nav-home.nav-transparent {
  border-bottom-color: transparent;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.66) 0%, rgba(15, 23, 42, 0.18) 70%, rgba(15, 23, 42, 0) 100%);
  box-shadow: none;
  transition-property: opacity, transform, box-shadow;
}

.nav-home.nav-home-light {
  background: var(--glass-bg-light);
  border-bottom-color: var(--glass-border);
}

.nav-inner {
  display: flex;
  align-items: center;
  gap: var(--sp-8);
  height: 100%;
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  white-space: nowrap;
}

.logo-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--r-sm);
  background: var(--gradient-blue);
  color: var(--white);
  font-size: var(--text-lg);
  font-weight: 800;
  transition: transform var(--dur-normal) var(--ease-spring);
}

.logo:hover .logo-mark {
  transform: rotate(-8deg) scale(1.05);
}

.nav-search {
  flex: 1;
  max-width: 480px;
}

.search-box {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  height: 44px;
  padding: 0 var(--sp-4);
  border: 1px solid var(--glass-border);
  border-radius: var(--r-full);
  background: var(--glass-bg);
  color: var(--text-faint);
  transition: all var(--dur-normal) var(--ease-out);
}

.search-box:focus-within {
  transform: translateY(-1px);
  border-color: var(--accent);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  color: var(--text-primary);
  font-size: var(--text-sm);
}

.search-input::placeholder {
  color: var(--text-muted);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.nav-link {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-1);
  height: 40px;
  padding: 0 var(--sp-3);
  border-radius: var(--r-full);
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 500;
  text-decoration: none;
  transition: all var(--dur-fast);
}

.nav-link:hover {
  background: rgba(59, 130, 246, 0.1);
  color: var(--text-primary);
}

.nav-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: var(--r-full);
  background: transparent;
  color: var(--text-secondary);
  transition: all var(--dur-normal) var(--ease-spring);
}

.nav-btn:hover {
  transform: scale(1.05);
  background: rgba(59, 130, 246, 0.1);
  color: var(--text-primary);
}

.cart-badge {
  position: absolute;
  top: 2px;
  right: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: var(--r-full);
  background: var(--accent);
  color: var(--white);
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 600;
  line-height: 1;
}

.login-btn {
  width: auto;
  padding: 0 var(--sp-5);
  background: var(--gradient-blue);
  color: var(--white);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 500;
  text-decoration: none;
}

.login-btn:hover {
  background: var(--accent-light);
  color: var(--white);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

.user-avatar,
.dropdown-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--r-full);
  background: var(--gradient-blue);
  color: var(--white);
  font-family: var(--font-display);
  font-weight: 700;
}

.user-avatar {
  width: 32px;
  height: 32px;
  font-size: var(--text-sm);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.user-btn:hover .user-avatar {
  transform: scale(1.08);
  border-color: var(--accent);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
}

.user-menu {
  position: relative;
}

.dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  z-index: 60;
  min-width: 220px;
  padding: var(--sp-2);
  border: 1px solid var(--glass-border);
  border-radius: var(--r-md);
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: var(--glass-shadow);
}

.dropdown-header {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-3);
}

.dropdown-avatar {
  width: 40px;
  height: 40px;
  font-size: var(--text-base);
}

.dropdown-name {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.dropdown-role {
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.dropdown-divider {
  height: 1px;
  margin: var(--sp-1) 0;
  background: var(--glass-border);
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  width: 100%;
  padding: var(--sp-2) var(--sp-3);
  border: none;
  border-radius: var(--r-sm);
  background: none;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  text-align: left;
  text-decoration: none;
  transition: all var(--dur-fast);
}

.dropdown-item:hover {
  transform: translateX(2px);
  background: rgba(59, 130, 246, 0.1);
  color: var(--text-primary);
}

.dropdown-logout:hover {
  background: rgba(239, 68, 68, 0.15);
  color: var(--error);
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all var(--dur-normal) var(--ease-out);
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.96);
}

.badge-pop-enter-active {
  animation: badgePop 0.35s var(--ease-spring);
}

.badge-pop-leave-active {
  transition: all 0.2s ease-in;
}

.badge-pop-leave-to {
  opacity: 0;
  transform: scale(0.5);
}

.page-enter-active {
  transition: all 0.45s var(--ease-out);
}

.page-leave-active {
  transition: all 0.2s ease-in;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(16px) scale(0.99);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

.main {
  flex: 1;
  padding-top: var(--nav-h);
}

.main-home {
  padding-top: 0;
}

.footer {
  margin-top: auto;
  padding: var(--sp-12) 0;
  border-top: 1px solid var(--glass-border);
  background: var(--surface-1);
}

.footer-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--sp-6);
}

.footer-left {
  display: flex;
  align-items: center;
  gap: var(--sp-6);
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  font-family: var(--font-display);
  font-weight: 600;
}

.footer-brand .logo-mark {
  width: 28px;
  height: 28px;
  font-size: var(--text-sm);
}

.footer-copy {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.footer-links {
  display: flex;
  gap: var(--sp-5);
}

.footer-links a {
  color: var(--text-muted);
  font-size: var(--text-sm);
  transition: color var(--dur-fast);
}

.footer-links a:hover {
  color: var(--accent-light);
}

.nav-on-dark .logo,
.nav-on-dark .logo-text {
  color: var(--text-primary);
}

.nav-on-dark .nav-link,
.nav-on-dark .nav-btn {
  color: var(--text-secondary);
}

.nav-on-dark .nav-link:hover,
.nav-on-dark .nav-btn:hover {
  background: rgba(59, 130, 246, 0.1);
  color: var(--text-primary);
}

.nav-on-dark .search-box {
  border-color: var(--glass-border);
  background: var(--glass-bg);
  color: var(--text-faint);
}

.nav-on-dark .search-input {
  color: var(--text-primary);
}

.nav-on-dark .search-input::placeholder {
  color: var(--text-muted);
}

.nav-on-dark .login-btn {
  background: var(--gradient-blue);
  color: var(--white);
}

.nav-on-dark .login-btn:hover {
  background: var(--accent-light);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
}

@media (max-width: 900px) {
  .nav-search {
    position: fixed;
    top: var(--nav-h);
    left: 0;
    right: 0;
    max-width: none;
    padding: var(--sp-4);
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    z-index: 39;
    box-shadow: var(--glass-shadow);
    transform: translateY(-100%);
    transition: transform var(--dur-normal) var(--ease-out);
  }

  .nav-search.is-open {
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .nav-inner {
    gap: var(--sp-4);
  }

  .nav-link span {
    display: none;
  }

  .footer-inner,
  .footer-left {
    flex-direction: column;
    text-align: center;
  }
}

@media (prefers-reduced-motion: reduce) {
  .scroll-progress {
    transition: none;
  }
}
</style>
