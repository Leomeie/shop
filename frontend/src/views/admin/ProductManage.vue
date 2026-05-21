<template>
  <div class="workbench-page">
    <section class="workbench-header">
      <div>
        <h2 class="workbench-title">商品管理</h2>
        <p class="workbench-desc">集中查看商品状态、下载热度和上架节奏，支持批量启停、详情抽屉和复杂编辑页。</p>
      </div>

      <div class="workbench-actions">
        <router-link class="primary-btn" to="/admin/products/new">新建商品</router-link>
        <button class="ghost-btn" type="button" :disabled="!selected.length" @click="handleBatch('deactivate')">批量下架</button>
        <button class="primary-btn" type="button" :disabled="!selected.length" @click="handleBatch('activate')">批量上架</button>
      </div>
    </section>

    <section class="workbench-stats">
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">商品总数</span>
        <strong class="stat-tile__value">{{ total }}</strong>
      </article>
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">当前上架</span>
        <strong class="stat-tile__value">{{ activeCount }}</strong>
      </article>
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">草稿待发</span>
        <strong class="stat-tile__value">{{ draftCount }}</strong>
      </article>
      <article class="store-surface stat-tile">
        <span class="stat-tile__label">已选条目</span>
        <strong class="stat-tile__value">{{ selected.length }}</strong>
      </article>
    </section>

    <section class="workbench-filters store-surface">
      <div class="workbench-filters__row">
        <div class="table-toolbar-search workbench-filters__grow">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>
          <input v-model="search" type="text" placeholder="搜索商品名称或分类" @keyup.enter="fetchData" />
        </div>

        <div class="filter-cluster">
          <button :class="['result-chip', { 'is-active': !statusFilter }]" type="button" @click="setStatus('')">全部</button>
          <button :class="['result-chip', { 'is-active': statusFilter === 'active' }]" type="button" @click="setStatus('active')">上架</button>
          <button :class="['result-chip', { 'is-active': statusFilter === 'draft' }]" type="button" @click="setStatus('draft')">草稿</button>
          <button :class="['result-chip', { 'is-active': statusFilter === 'inactive' }]" type="button" @click="setStatus('inactive')">下架</button>
        </div>
      </div>
    </section>

    <section class="table-panel store-surface">
      <div class="table-panel__head">
        <div>
          <div class="table-panel__title">商品列表</div>
          <div class="table-panel__meta">共 {{ total }} 条记录，点击行可查看详情</div>
        </div>
      </div>

      <table class="workbench-table">
        <thead>
          <tr>
            <th class="col-check"><input type="checkbox" @change="toggleAll" :checked="allSelected" /></th>
            <th>商品信息</th>
            <th>分类</th>
            <th>状态</th>
            <th>下载量</th>
            <th>创建时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in products" :key="row.id" class="clickable-row" @click="openDetail(row.id)">
            <td class="col-check" @click.stop><input type="checkbox" :checked="selected.includes(row.id)" @change="toggleOne(row.id)" /></td>
            <td>
              <span class="workbench-table__primary">{{ row.name }}</span>
              <span class="workbench-table__secondary">ID {{ row.id }}</span>
            </td>
            <td>{{ row.category_name || '未分类' }}</td>
            <td>
              <StatusBadge
                :label="row.status === 'active' ? '上架' : row.status === 'draft' ? '草稿' : '下架'"
                :status="row.status"
                size="sm"
              />
            </td>
            <td>{{ row.download_count }}</td>
            <td>{{ row.created_at }}</td>
            <td class="actions-cell" @click.stop>
              <button class="table-link" type="button" @click="router.push(`/admin/products/${row.id}/edit`)">编辑</button>
              <button class="table-link danger" type="button" @click="handleDelete(row)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="!loading && !products.length" class="table-empty">暂无商品</div>
    </section>

    <div class="table-footer" v-if="total > 20">
      <el-pagination background layout="prev, pager, next" :total="total" :page-size="20" v-model:current-page="page" @current-change="fetchData" />
    </div>

    <el-drawer v-model="drawerOpen" size="460px" :with-header="false" destroy-on-close>
      <div class="drawer-shell" v-loading="detailLoading">
        <div v-if="detail" class="drawer-content">
          <div class="drawer-top">
            <div>
              <div class="drawer-kicker">Product Detail</div>
              <h3>{{ detail.name }}</h3>
              <p>{{ detail.category_name || '未分类' }}</p>
            </div>
            <StatusBadge :label="detail.status === 'active' ? '上架' : detail.status === 'draft' ? '草稿' : '下架'" :status="detail.status" />
          </div>

          <div class="drawer-hero">
            <img v-if="detail.main_image" :src="detail.main_image" alt="商品主图" />
            <span v-else>暂无主图</span>
          </div>

          <div class="drawer-block">
            <div class="drawer-block__title">商品概览</div>
            <div class="drawer-metrics">
              <div>
                <span>版本</span>
                <strong>{{ detail.version || '1.0.0' }}</strong>
              </div>
              <div>
                <span>下载量</span>
                <strong>{{ detail.download_count }}</strong>
              </div>
              <div>
                <span>精选推荐</span>
                <strong>{{ detail.is_featured ? '是' : '否' }}</strong>
              </div>
            </div>
          </div>

          <div class="drawer-block" v-if="detail.description">
            <div class="drawer-block__title">商品描述</div>
            <p class="drawer-text">{{ detail.description }}</p>
          </div>

          <div class="drawer-block">
            <div class="drawer-block__title">SKU 列表</div>
            <div v-if="detail.skus_data?.length" class="drawer-skus">
              <div v-for="sku in detail.skus_data" :key="sku.id" class="drawer-sku">
                <div>
                  <strong>{{ sku.name }}</strong>
                  <p>{{ sku.license_description || '未填写授权说明' }}</p>
                </div>
                <span>¥{{ sku.price_yuan }}</span>
              </div>
            </div>
            <div v-else class="empty-inline">暂无 SKU</div>
          </div>

          <div class="drawer-actions">
            <button class="ghost-btn" type="button" @click="drawerOpen = false">关闭</button>
            <button class="primary-btn" type="button" @click="router.push(`/admin/products/${detail.id}/edit`)">前往编辑</button>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  batchAdminProducts,
  deleteAdminProduct,
  getAdminProduct,
  getAdminProducts,
} from '../../api/adminProduct'
import StatusBadge from '../../components/StatusBadge.vue'

const router = useRouter()
const products = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const search = ref('')
const statusFilter = ref('')
const selected = ref([])
const drawerOpen = ref(false)
const detailLoading = ref(false)
const detail = ref(null)

const allSelected = computed(() => products.value.length > 0 && selected.value.length === products.value.length)
const activeCount = computed(() => products.value.filter((item) => item.status === 'active').length)
const draftCount = computed(() => products.value.filter((item) => item.status === 'draft').length)

function toggleAll(event) {
  selected.value = event.target.checked ? products.value.map((row) => row.id) : []
}

function toggleOne(id) {
  const idx = selected.value.indexOf(id)
  if (idx === -1) selected.value.push(id)
  else selected.value.splice(idx, 1)
}

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
    const res = await getAdminProducts(params)
    products.value = res.data.results || []
    total.value = res.data.count || 0
    selected.value = []
  } finally {
    loading.value = false
  }
}

async function handleBatch(action) {
  await batchAdminProducts({ action, ids: selected.value })
  ElMessage.success('批量操作成功')
  fetchData()
}

async function openDetail(id) {
  drawerOpen.value = true
  detailLoading.value = true
  detail.value = null
  try {
    const res = await getAdminProduct(id)
    detail.value = res.data
  } finally {
    detailLoading.value = false
  }
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除「${row.name}」吗？`, '删除确认')
  await deleteAdminProduct(row.id)
  ElMessage.success('商品已删除')
  fetchData()
}

onMounted(fetchData)
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

.primary-btn,
.ghost-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 42px;
  padding: 0 var(--sp-5);
  border-radius: 12px;
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
  text-decoration: none;
}

.primary-btn {
  border: none;
  background: var(--text-primary);
  color: var(--white);
}

.ghost-btn {
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  color: var(--text-secondary);
}

.primary-btn:disabled,
.ghost-btn:disabled {
  opacity: 0.4;
}

.col-check {
  width: 48px;
}

.col-check input {
  accent-color: var(--text-primary);
}

.clickable-row {
  cursor: pointer;
}

.actions-cell {
  display: flex;
  gap: var(--sp-3);
}

.table-link {
  border: none;
  background: none;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.table-link.danger {
  color: var(--error);
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

.drawer-hero {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 220px;
  border-radius: 20px;
  background: var(--glass-border);
  overflow: hidden;
  color: var(--text-muted);
}

.drawer-hero img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  grid-template-columns: repeat(3, minmax(0, 1fr));
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

.drawer-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-3);
}
</style>
