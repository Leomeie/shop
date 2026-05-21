<template>
  <div class="store-page">
    <StorePageHeader eyebrow="Orders" icon="package" title="我的订单" subtitle="集中查看所有交易记录、订单状态与支付进度。" compact />

    <div class="store-page-body">
      <div class="container">
        <div class="account-shell">
          <StoreAccountNav />

          <div class="account-content">
            <section class="workbench-stats">
              <article class="store-surface stat-tile">
                <span class="stat-tile__label">待支付</span>
                <strong class="stat-tile__value">{{ statusCounts.pending || 0 }}</strong>
              </article>
              <article class="store-surface stat-tile">
                <span class="stat-tile__label">已支付</span>
                <strong class="stat-tile__value">{{ statusCounts.paid || 0 }}</strong>
              </article>
              <article class="store-surface stat-tile">
                <span class="stat-tile__label">已完成</span>
                <strong class="stat-tile__value">{{ statusCounts.completed || 0 }}</strong>
              </article>
              <article class="store-surface stat-tile">
                <span class="stat-tile__label">全部订单</span>
                <strong class="stat-tile__value">{{ orders.length }}</strong>
              </article>
            </section>

            <section class="store-surface store-surface--soft filters-panel">
              <div class="results-actions">
                <button v-for="tab in tabs" :key="tab.value" :class="['result-chip', { 'is-active': statusFilter === tab.value }]" type="button" @click="setFilter(tab.value)">
                  {{ tab.label }}
                </button>
              </div>
            </section>

            <section v-loading="loading" class="orders-list">
              <article
                v-for="(order, index) in orders"
                :key="order.id"
                class="store-surface store-surface--soft order-card"
                :style="{ animationDelay: `${index * 60}ms` }"
                @click="$router.push(`/orders/${order.id}`)"
              >
                <div class="order-card__top">
                  <div>
                    <div class="order-no">订单号 {{ order.order_no }}</div>
                    <div class="order-time">{{ order.created_at }}</div>
                  </div>
                  <StatusBadge :label="order.status_display" :status="order.status" />
                </div>

                <div class="order-items">
                  <div v-for="item in order.items" :key="item.id" class="order-item">
                    <div>
                      <div class="order-item__name">{{ item.product_name }}</div>
                      <div class="order-item__sku">{{ item.sku_name }}</div>
                    </div>
                    <div class="order-item__price">¥{{ item.price_yuan }}</div>
                  </div>
                </div>

                <div class="order-card__bottom">
                  <span class="order-total-label">应付金额</span>
                  <span class="order-total-value">¥{{ order.pay_amount_yuan }}</span>
                </div>
              </article>

              <div v-if="!loading && !orders.length" class="empty-state store-surface store-surface--soft">
                <div class="empty-icon">
                  <AnimatedIcons name="package" :size="32" />
                </div>
                <h3>暂无订单</h3>
                <p>先去商品页挑选适合你的数字资源。</p>
                <router-link to="/products" class="empty-action">浏览商品</router-link>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { getOrders } from '../../api/order'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StatusBadge from '../../components/StatusBadge.vue'
import StoreAccountNav from '../../components/StoreAccountNav.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'

const tabs = [
  { label: '全部', value: '' },
  { label: '待支付', value: 'pending' },
  { label: '已支付', value: 'paid' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'cancelled' },
]

const orders = ref([])
const loading = ref(false)
const statusFilter = ref('')

const statusCounts = computed(() => {
  const counts = {}
  orders.value.forEach((order) => {
    counts[order.status] = (counts[order.status] || 0) + 1
  })
  return counts
})

function setFilter(value) {
  statusFilter.value = value
  fetchOrders()
}

async function fetchOrders() {
  loading.value = true
  try {
    const params = {}
    if (statusFilter.value) params.status = statusFilter.value
    const res = await getOrders(params)
    orders.value = res.data.results || []
  } finally {
    loading.value = false
  }
}

onMounted(fetchOrders)
</script>

<style scoped>
.stat-tile {
  display: grid;
  gap: var(--sp-2);
  padding: var(--sp-5);
}

.stat-tile__label {
  color: var(--text-muted);
  font-size: var(--text-xs);
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.stat-tile__value {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 800;
}

.filters-panel {
  padding: var(--sp-4) var(--sp-5);
}

.orders-list {
  display: grid;
  gap: var(--sp-4);
}

.order-card {
  cursor: pointer;
  padding: var(--sp-5);
  animation: fadeInUp 0.45s var(--ease-out) both;
}

.order-card__top,
.order-card__bottom,
.order-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
}

.order-card__top {
  margin-bottom: var(--sp-4);
}

.order-no {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.order-time {
  margin-top: 4px;
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.order-items {
  display: grid;
  gap: var(--sp-3);
}

.order-item {
  padding: var(--sp-3) 0;
  border-top: 1px solid var(--glass-border);
}

.order-item__name {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.order-item__sku {
  color: var(--text-secondary);
  font-size: var(--text-xs);
  margin-top: 4px;
}

.order-item__price,
.order-total-value {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-weight: 800;
}

.order-card__bottom {
  margin-top: var(--sp-4);
  padding-top: var(--sp-4);
  border-top: 1px solid var(--glass-border);
}

.order-total-label {
  color: var(--text-secondary);
  font-size: var(--text-sm);
}
</style>
