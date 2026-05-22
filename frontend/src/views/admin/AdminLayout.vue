<template>
  <div class="admin-layout admin-shell">
    <aside class="admin-sidebar">
      <div class="admin-sidebar__brand">
        <img src="/images/logo.png" alt="ShopEase" class="brand-icon" width="42" height="42" />
        <div>
          <div class="brand-name">ShopEase</div>
          <div class="brand-subtitle">Operator Console</div>
        </div>
      </div>

      <nav class="admin-nav">
        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          :class="['admin-nav__item', { 'is-active': isMenuActive(item.path) }]"
        >
          <span class="admin-nav__icon" v-html="item.icon" />
          <span class="admin-nav__label">{{ item.label }}</span>
        </router-link>
      </nav>

      <div class="admin-sidebar__footer">
        <router-link to="/" class="admin-back-link">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6" /></svg>
          返回前台
        </router-link>
      </div>
    </aside>

    <div class="admin-main-shell">
      <header class="admin-topbar">
        <div>
          <div class="admin-topbar__eyebrow">Control Panel</div>
          <h1 class="admin-topbar__title">{{ activeMenuName }}</h1>
        </div>

        <div class="admin-topbar__user">
          <div class="user-avatar">{{ (userStore.userInfo?.username || 'A').charAt(0).toUpperCase() }}</div>
          <div>
            <div class="user-name">{{ userStore.userInfo?.username }}</div>
            <div class="user-role">管理员</div>
          </div>
        </div>
      </header>

      <main class="admin-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../../stores/user'

const route = useRoute()
const userStore = useUserStore()

const menuItems = [
  { path: '/admin', label: '数据总览', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>' },
  { path: '/admin/products', label: '商品管理', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><line x1="3" y1="6" x2="21" y2="6"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>' },
  { path: '/admin/orders', label: '订单管理', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>' },
  { path: '/admin/coupons', label: '优惠券', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 12v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-6"/><path d="M2 8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v4a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8z"/><line x1="12" y1="8" x2="12" y2="16"/></svg>' },
  { path: '/admin/users', label: '用户管理', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>' },
]

const menuNames = {
  '/admin': '数据总览',
  '/admin/products': '商品管理',
  '/admin/orders': '订单管理',
  '/admin/coupons': '优惠券',
  '/admin/users': '用户管理',
}

function isMenuActive(path) {
  if (path === '/admin') return route.path === '/admin'
  return route.path.startsWith(path)
}

const activeMenuName = computed(() => {
  if (route.path.startsWith('/admin/products')) return '商品管理'
  if (route.path.startsWith('/admin/orders')) return '订单管理'
  if (route.path.startsWith('/admin/coupons')) return '优惠券'
  if (route.path.startsWith('/admin/users')) return '用户管理'
  return menuNames[route.path] || '运营后台'
})
</script>

<style scoped>
.admin-layout {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  min-height: 100vh;
}

.admin-sidebar {
  display: flex;
  flex-direction: column;
  padding: var(--sp-5);
  background:
    radial-gradient(circle at top, rgba(198, 168, 106, 0.14), transparent 30%),
    linear-gradient(180deg, #111827 0%, #182235 100%);
  color: rgba(255, 255, 255, 0.82);
}

.admin-sidebar__brand {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.04);
}

.brand-icon {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  object-fit: contain;
}

.brand-name {
  color: var(--white);
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
}

.brand-subtitle {
  color: rgba(255, 255, 255, 0.6);
  font-size: var(--text-xs);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.admin-nav {
  display: grid;
  gap: var(--sp-2);
  margin-top: var(--sp-5);
}

.admin-nav__item {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-3) var(--sp-4);
  border-radius: 14px;
  color: rgba(255, 255, 255, 0.7);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 500;
  transition: color var(--dur-fast) var(--ease-out), background var(--dur-fast) var(--ease-out);
}

.admin-nav__item:hover {
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.88);
}

.admin-nav__item.is-active {
  background: rgba(255, 255, 255, 0.1);
  color: var(--white);
}

.admin-sidebar__footer {
  margin-top: auto;
  padding: var(--sp-4);
}

.admin-back-link {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  color: rgba(255, 255, 255, 0.65);
  font-family: var(--font-display);
  font-size: var(--text-sm);
}

.admin-main-shell {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  min-width: 0;
}

.admin-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
  padding: var(--sp-5) var(--sp-8);
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(16px);
}

.admin-topbar__eyebrow {
  color: #60a5fa;
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.admin-topbar__title {
  margin-top: 6px;
  color: #e2e8f0;
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.admin-topbar__user {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.user-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 38px;
  height: 38px;
  border-radius: 999px;
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.user-name {
  color: #e2e8f0;
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.user-role {
  color: #64748b;
  font-size: 11px;
}

.admin-main {
  overflow-y: auto;
  padding: var(--sp-6);
}

@media (max-width: 1024px) {
  .admin-layout {
    grid-template-columns: 92px minmax(0, 1fr);
  }

  .brand-name,
  .brand-subtitle,
  .admin-nav__label,
  .admin-back-link {
    display: none;
  }

  .admin-sidebar {
    padding: var(--sp-4);
  }
}
</style>
