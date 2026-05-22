<template>
  <div class="workbench-page" v-loading="loading">
    <section class="workbench-header">
      <div>
        <h2 class="workbench-title">经营总览</h2>
        <p class="workbench-desc">用更清晰的指标结构查看今日经营表现、近 7 天趋势和当前热销资源。</p>
      </div>
    </section>

    <section class="workbench-stats">
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">今日订单</span>
        <strong class="stat-tile__value">{{ stats.today?.order_count || 0 }}</strong>
      </article>
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">今日销售额</span>
        <strong class="stat-tile__value accent">¥{{ stats.today?.sales_amount_yuan || 0 }}</strong>
      </article>
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">今日新增用户</span>
        <strong class="stat-tile__value">{{ stats.today?.new_users || 0 }}</strong>
      </article>
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">总用户数</span>
        <strong class="stat-tile__value">{{ stats.overview?.total_users || 0 }}</strong>
      </article>
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">累计浏览次数</span>
        <strong class="stat-tile__value">{{ stats.overview?.total_product_views || 0 }}</strong>
      </article>
    </section>

    <section class="dashboard-grid">
      <div class="store-surface chart-panel">
        <div class="store-panel-header">
          <div>
            <div class="store-panel-title">近 7 天销售趋势</div>
            <div class="store-panel-subtitle">按日观察订单量和销售额</div>
          </div>
        </div>

        <div class="trend-list">
          <div v-for="day in stats.trend" :key="day.date" class="trend-row">
            <span class="trend-date">{{ day.date }}</span>
            <div class="trend-bar">
              <div class="bar-fill" :style="{ width: barWidth(day.sales_amount_yuan) + '%' }" />
            </div>
            <span class="trend-orders">{{ day.order_count }} 单</span>
            <span class="trend-amount">¥{{ day.sales_amount_yuan }}</span>
          </div>
        </div>
      </div>

      <div class="store-surface chart-panel">
        <div class="store-panel-header">
          <div>
            <div class="store-panel-title">热销资源 Top 10</div>
            <div class="store-panel-subtitle">按下载量排序的热门商品</div>
          </div>
        </div>

        <div class="top-list">
          <div v-for="(product, index) in stats.top_products" :key="product.id" class="top-item">
            <span :class="['rank', { top3: index < 3 }]">{{ index + 1 }}</span>
            <div class="top-item__copy">
              <span class="top-name">{{ product.name }}</span>
              <span class="top-count">{{ product.download_count }} 次下载</span>
            </div>
          </div>
          <div v-if="!stats.top_products?.length" class="empty-hint">暂无数据</div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import request from '../../utils/request'

const stats = ref({})
const loading = ref(false)

const maxSales = computed(() => {
  if (!stats.value.trend?.length) return 0
  return Math.max(...stats.value.trend.map((item) => item.sales_amount_yuan), 0)
})

function barWidth(value) {
  if (!maxSales.value) return 0
  return Math.round((value / maxSales.value) * 100)
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await request.get('/admin/dashboard/')
    stats.value = res.data
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: var(--sp-5);
}

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

.stat-tile__value.accent {
  color: var(--accent);
}

.chart-panel {
  overflow: hidden;
}

.trend-list,
.top-list {
  padding: 0 var(--sp-6) var(--sp-6);
}

.trend-row {
  display: grid;
  grid-template-columns: 100px minmax(0, 1fr) 70px 90px;
  gap: var(--sp-4);
  align-items: center;
  padding: var(--sp-3) 0;
}

.trend-date {
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
}

.trend-bar {
  overflow: hidden;
  height: 8px;
  border-radius: 999px;
  background: var(--glass-border);
}

.bar-fill {
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, var(--accent) 0%, var(--accent-light) 100%);
}

.trend-orders,
.trend-amount {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  text-align: right;
}

.top-item {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-3) 0;
}

.rank {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 999px;
  background: var(--glass-border);
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
}

.rank.top3 {
  background: rgba(198, 168, 106, 0.18);
  color: #8a6b2d;
}

.top-item__copy {
  display: grid;
  gap: 4px;
}

.top-name {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.top-count {
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.empty-hint {
  padding: var(--sp-6) 0;
  color: var(--text-muted);
  text-align: center;
}

@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .trend-row {
    grid-template-columns: 90px minmax(0, 1fr) 60px 80px;
  }
}
</style>
