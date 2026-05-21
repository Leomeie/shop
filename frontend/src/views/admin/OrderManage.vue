<template>
  <div class="workbench-page">
    <section class="workbench-header">
      <div>
        <h2 class="workbench-title">订单管理</h2>
        <p class="workbench-desc">筛选订单状态、查看支付进度与订单内容，点击行即可在侧边抽屉中查看完整详情。</p>
      </div>
    </section>

    <section class="workbench-filters store-surface">
      <div class="workbench-filters__row">
        <div class="table-toolbar-search workbench-filters__grow">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>
          <input v-model="search" type="text" placeholder="搜索订单号" @keyup.enter="fetchData" />
        </div>

        <div class="filter-cluster">
          <button :class="['result-chip', { 'is-active': !statusFilter }]" type="button" @click="setStatus('')">全部</button>
          <button :class="['result-chip', { 'is-active': statusFilter === 'pending' }]" type="button" @click="setStatus('pending')">待支付</button>
          <button :class="['result-chip', { 'is-active': statusFilter === 'completed' }]" type="button" @click="setStatus('completed')">已完成</button>
          <button :class="['result-chip', { 'is-active': statusFilter === 'cancelled' }]" type="button" @click="setStatus('cancelled')">已取消</button>
        </div>
      </div>
    </section>

    <section class="table-panel store-surface">
      <div class="table-panel__head">
        <div>
          <div class="table-panel__title">订单列表</div>
          <div class="table-panel__meta">共 {{ total }} 条订单记录，点击行查看详情</div>
        </div>
      </div>

      <table class="workbench-table">
        <thead>
          <tr>
            <th>订单号</th>
            <th>状态</th>
            <th>下单用户</th>
            <th>商品信息</th>
            <th>金额</th>
            <th>下单时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in orders" :key="row.id" class="clickable-row" @click="openDetail(row.id)">
            <td>
              <span class="workbench-table__primary mono">{{ row.order_no }}</span>
            </td>
            <td>
              <StatusBadge :label="row.status_display" :status="row.status" size="sm" />
            </td>
            <td>
              <span class="workbench-table__primary">{{ row.user?.nickname || row.user?.username || '-' }}</span>
              <span class="workbench-table__secondary">@{{ row.user?.username || 'unknown' }}</span>
            </td>
            <td>
              <span class="workbench-table__primary">{{ row.items?.[0]?.product_name || '未命名商品' }}</span>
              <span class="workbench-table__secondary">{{ row.items?.[0]?.sku_name || '—' }}</span>
            </td>
            <td class="amount-cell">¥{{ row.pay_amount_yuan }}</td>
            <td>{{ row.created_at }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="!loading && !orders.length" class="table-empty">暂无订单</div>
    </section>

    <div class="table-footer" v-if="total > 20">
      <el-pagination background layout="prev, pager, next" :total="total" :page-size="20" v-model:current-page="page" @current-change="fetchData" />
    </div>

    <el-drawer v-model="drawerOpen" size="480px" :with-header="false" destroy-on-close>
      <div class="drawer-shell" v-loading="detailLoading">
        <div v-if="detail" class="drawer-content">
          <div class="drawer-top">
            <div>
              <div class="drawer-kicker">Order Detail</div>
              <h3>{{ detail.order_no }}</h3>
              <p>{{ detail.user?.nickname || detail.user?.username || '未知用户' }}</p>
            </div>
            <StatusBadge :label="detail.status_display" :status="detail.status" />
          </div>

          <div class="drawer-block">
            <div class="drawer-block__title">订单摘要</div>
            <div class="drawer-metrics">
              <div>
                <span>应付金额</span>
                <strong>¥{{ detail.pay_amount_yuan }}</strong>
              </div>
              <div>
                <span>下单时间</span>
                <strong>{{ detail.created_at }}</strong>
              </div>
              <div>
                <span>支付时间</span>
                <strong>{{ detail.pay_time || '未支付' }}</strong>
              </div>
            </div>
          </div>

          <div class="drawer-block">
            <div class="drawer-block__title">用户信息</div>
            <p class="drawer-text">{{ detail.user?.nickname || '-' }}（@{{ detail.user?.username || '-' }}）</p>
            <p class="drawer-text">{{ detail.user?.phone || '未填写手机号' }}</p>
            <p class="drawer-text">{{ detail.user?.email || '未填写邮箱' }}</p>
          </div>

          <div class="drawer-block">
            <div class="drawer-block__title">商品清单</div>
            <div class="drawer-skus">
              <div v-for="item in detail.items" :key="item.id" class="drawer-sku">
                <div>
                  <strong>{{ item.product_name }}</strong>
                  <p>{{ item.sku_name }}</p>
                </div>
                <span>¥{{ item.price_yuan }}</span>
              </div>
            </div>
          </div>

          <div v-if="detail.remark" class="drawer-block">
            <div class="drawer-block__title">备注</div>
            <p class="drawer-text">{{ detail.remark }}</p>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getAdminOrder, getAdminOrders } from '../../api/adminPanel'
import StatusBadge from '../../components/StatusBadge.vue'

const orders = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const search = ref('')
const statusFilter = ref('')
const drawerOpen = ref(false)
const detailLoading = ref(false)
const detail = ref(null)

function setStatus(status) {
  statusFilter.value = status
  page.value = 1
  fetchData()
}

async function fetchData() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: 20 }
    if (search.value) params.search = search.value
    if (statusFilter.value) params.status = statusFilter.value
    const res = await getAdminOrders(params)
    orders.value = res.data.results || []
    total.value = res.data.count || 0
  } finally {
    loading.value = false
  }
}

async function openDetail(id) {
  drawerOpen.value = true
  detailLoading.value = true
  detail.value = null
  try {
    const res = await getAdminOrder(id)
    detail.value = res.data
  } finally {
    detailLoading.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.mono {
  font-family: 'SF Mono', 'Fira Code', monospace;
}

.clickable-row {
  cursor: pointer;
}

.amount-cell {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-weight: 700;
}

.table-empty {
  padding: var(--sp-8);
  color: var(--text-muted);
  text-align: center;
}

.table-footer {
  display: flex;
  justify-content: flex-end;
}

.drawer-shell {
  min-height: 100%;
}

.drawer-content {
  display: grid;
  gap: var(--sp-5);
  padding: var(--sp-2);
}

.drawer-top h3 {
  margin-top: var(--sp-2);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 800;
  letter-spacing: -0.03em;
}

.drawer-top p,
.drawer-kicker {
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.drawer-kicker {
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.drawer-block {
  display: grid;
  gap: var(--sp-3);
  padding: var(--sp-4);
  border: 1px solid var(--glass-border);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.03);
}

.drawer-block__title {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.drawer-metrics {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--sp-3);
}

.drawer-metrics span,
.drawer-sku p,
.drawer-text {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.7;
}

.drawer-metrics strong,
.drawer-sku strong {
  display: block;
  margin-top: 4px;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.drawer-skus {
  display: grid;
  gap: var(--sp-3);
}

.drawer-sku {
  display: flex;
  justify-content: space-between;
  gap: var(--sp-4);
}
</style>
