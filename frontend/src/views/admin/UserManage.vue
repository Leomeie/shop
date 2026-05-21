<template>
  <div class="workbench-page">
    <section class="workbench-header">
      <div>
        <h2 class="workbench-title">用户管理</h2>
        <p class="workbench-desc">统一查看用户资料、注册时间与基础联系方式，点击行即可在侧边抽屉中查看用户详情。</p>
      </div>
    </section>

    <section class="workbench-filters store-surface">
      <div class="workbench-filters__row">
        <div class="table-toolbar-search workbench-filters__grow">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>
          <input v-model="search" type="text" placeholder="搜索用户昵称、用户名、手机号或邮箱" @keyup.enter="fetchData" />
        </div>
      </div>
    </section>

    <section class="table-panel store-surface">
      <div class="table-panel__head">
        <div>
          <div class="table-panel__title">用户列表</div>
          <div class="table-panel__meta">共 {{ total }} 条用户记录，点击行查看详情</div>
        </div>
      </div>

      <table class="workbench-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>用户信息</th>
            <th>昵称</th>
            <th>手机号</th>
            <th>邮箱</th>
            <th>注册时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in users" :key="row.id" class="clickable-row" @click="openDetail(row.id)">
            <td>{{ row.id }}</td>
            <td>
              <div class="user-cell">
                <div class="mini-avatar">{{ (row.username || 'U').charAt(0).toUpperCase() }}</div>
                <div>
                  <span class="workbench-table__primary">{{ row.username }}</span>
                  <span class="workbench-table__secondary">{{ row.is_staff ? '管理员账户' : '普通用户' }}</span>
                </div>
              </div>
            </td>
            <td>{{ row.nickname || '-' }}</td>
            <td class="mono">{{ row.phone || '-' }}</td>
            <td>{{ row.email || '-' }}</td>
            <td>{{ row.date_joined }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="!loading && !users.length" class="table-empty">暂无用户</div>
    </section>

    <div class="table-footer" v-if="total > 20">
      <el-pagination background layout="prev, pager, next" :total="total" :page-size="20" v-model:current-page="page" @current-change="fetchData" />
    </div>

    <el-drawer v-model="drawerOpen" size="460px" :with-header="false" destroy-on-close>
      <div class="drawer-shell" v-loading="detailLoading">
        <div v-if="detail" class="drawer-content">
          <div class="drawer-top">
            <div class="mini-avatar large">{{ (detail.username || 'U').charAt(0).toUpperCase() }}</div>
            <div>
              <div class="drawer-kicker">User Detail</div>
              <h3>{{ detail.username }}</h3>
              <p>{{ detail.nickname || '未设置昵称' }}</p>
            </div>
          </div>

          <div class="drawer-block">
            <div class="drawer-block__title">账户状态</div>
            <div class="drawer-tags">
              <StatusBadge :label="detail.is_active ? '启用' : '禁用'" :status="detail.is_active ? 'success' : 'neutral'" size="sm" />
              <StatusBadge :label="detail.is_staff ? '管理员' : '普通用户'" :status="detail.is_staff ? 'info' : 'neutral'" size="sm" />
              <StatusBadge :label="detail.is_superuser ? '超级管理员' : '非超级管理员'" :status="detail.is_superuser ? 'warning' : 'neutral'" size="sm" />
            </div>
          </div>

          <div class="drawer-block">
            <div class="drawer-block__title">联系信息</div>
            <p class="drawer-text">手机号：{{ detail.phone || '未填写' }}</p>
            <p class="drawer-text">邮箱：{{ detail.email || '未填写' }}</p>
          </div>

          <div class="drawer-block">
            <div class="drawer-block__title">账户时间线</div>
            <p class="drawer-text">注册时间：{{ detail.date_joined }}</p>
            <p class="drawer-text">最近登录：{{ detail.last_login || '暂无登录记录' }}</p>
          </div>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getAdminUser, getAdminUsers } from '../../api/adminPanel'
import StatusBadge from '../../components/StatusBadge.vue'

const users = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const search = ref('')
const drawerOpen = ref(false)
const detailLoading = ref(false)
const detail = ref(null)

async function fetchData() {
  loading.value = true
  try {
    const res = await getAdminUsers({ page: page.value, search: search.value })
    users.value = res.data.results || []
    total.value = res.data.count || 0
  } catch {
    users.value = []
  } finally {
    loading.value = false
  }
}

async function openDetail(id) {
  drawerOpen.value = true
  detailLoading.value = true
  detail.value = null
  try {
    const res = await getAdminUser(id)
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

.user-cell {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
}

.mini-avatar {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 999px;
  background: rgba(198, 168, 106, 0.14);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xs);
  font-weight: 700;
}

.mini-avatar.large {
  width: 56px;
  height: 56px;
  font-size: var(--text-base);
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

.drawer-top {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
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

.drawer-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-2);
}

.drawer-text {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.8;
}
</style>
