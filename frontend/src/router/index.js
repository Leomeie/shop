import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  // Storefront
  {
    path: '/',
    component: () => import('../views/storefront/MainLayout.vue'),
    children: [
      { path: '', name: 'Home', component: () => import('../views/storefront/Home.vue') },
      { path: 'products', name: 'ProductList', component: () => import('../views/storefront/ProductList.vue') },
      { path: 'products/:id', name: 'ProductDetail', component: () => import('../views/storefront/ProductDetail.vue') },
      { path: 'showcase', name: 'Showcase', component: () => import('../views/storefront/Showcase.vue') },
      { path: 'categories', name: 'Categories', component: () => import('../views/storefront/CategoryBrowse.vue') },
      { path: 'cart', name: 'Cart', component: () => import('../views/storefront/Cart.vue'), meta: { auth: true } },
      { path: 'checkout', name: 'Checkout', component: () => import('../views/storefront/Checkout.vue'), meta: { auth: true } },
      { path: 'orders', name: 'Orders', component: () => import('../views/storefront/Orders.vue'), meta: { auth: true } },
      { path: 'orders/:id', name: 'OrderDetail', component: () => import('../views/storefront/OrderDetail.vue'), meta: { auth: true } },
      { path: 'downloads', name: 'Downloads', component: () => import('../views/storefront/Downloads.vue'), meta: { auth: true } },
      { path: 'wishlist', name: 'Wishlist', component: () => import('../views/storefront/Wishlist.vue'), meta: { auth: true } },
      { path: 'profile', name: 'Profile', component: () => import('../views/storefront/Profile.vue'), meta: { auth: true } },
      { path: 'help', name: 'Help', component: () => import('../views/storefront/Help.vue') },
    ],
  },
  { path: '/login', name: 'Login', component: () => import('../views/storefront/Login.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/storefront/Register.vue') },

  // Admin
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { auth: true, admin: true },
    children: [
      { path: '', name: 'Dashboard', component: () => import('../views/admin/Dashboard.vue') },
      { path: 'products', name: 'AdminProducts', component: () => import('../views/admin/ProductManage.vue') },
      { path: 'products/new', name: 'AdminProductNew', component: () => import('../views/admin/ProductEditor.vue') },
      { path: 'products/:id/edit', name: 'AdminProductEdit', component: () => import('../views/admin/ProductEditor.vue') },
      { path: 'orders', name: 'AdminOrders', component: () => import('../views/admin/OrderManage.vue') },
      { path: 'coupons', name: 'AdminCoupons', component: () => import('../views/admin/CouponManage.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('../views/admin/UserManage.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  if (to.meta.auth && !userStore.isLoggedIn) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
    return
  }

  if ((to.meta.auth || to.meta.admin) && userStore.isLoggedIn && !userStore.userInfo) {
    try {
      await userStore.fetchUserInfo()
    } catch {
      userStore.logout()
      next({ name: 'Login', query: { redirect: to.fullPath } })
      return
    }
  }

  if (to.meta.admin && !userStore.isAdmin) {
    next({ name: 'Home' })
    return
  }

  next()
})

export default router
