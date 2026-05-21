<template>
  <aside class="account-sidebar store-surface store-surface--soft">
    <div class="store-panel-title">账户中心</div>
    <div class="store-panel-subtitle">你的订单、下载与账户资料</div>

    <nav class="account-nav">
      <router-link
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        :class="['account-nav__item', { 'is-active': route.path === item.to }]"
      >
        <AnimatedIcons :name="item.icon" :size="18" />
        <span>{{ item.label }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
import { useRoute } from 'vue-router'
import AnimatedIcons from './AnimatedIcons.vue'

const route = useRoute()

const items = [
  { to: '/profile', label: '个人资料', icon: 'user' },
  { to: '/orders', label: '我的订单', icon: 'package' },
  { to: '/downloads', label: '我的下载', icon: 'download' },
  { to: '/wishlist', label: '我的收藏', icon: 'heart' },
  { to: '/help', label: '帮助中心', icon: 'shield' },
]
</script>
