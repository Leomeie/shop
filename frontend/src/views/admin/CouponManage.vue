<template>
  <div class="workbench-page">
    <section class="workbench-header">
      <div>
        <h2 class="workbench-title">优惠券管理</h2>
        <p class="workbench-desc">统一管理券码、面额、有效期和使用情况，用同一控制台逻辑处理营销资源。</p>
      </div>

      <div class="workbench-actions">
        <button class="primary-btn" type="button" @click="showCreate = true">创建优惠券</button>
      </div>
    </section>

    <section class="table-panel store-surface">
      <div class="table-panel__head">
        <div>
          <div class="table-panel__title">优惠券列表</div>
          <div class="table-panel__meta">共 {{ coupons.length }} 条券码记录</div>
        </div>
      </div>

      <table class="workbench-table">
        <thead>
          <tr>
            <th>名称</th>
            <th>优惠码</th>
            <th>类型</th>
            <th>面额</th>
            <th>最低消费</th>
            <th>领取/总量</th>
            <th>有效期</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in coupons" :key="row.id">
            <td><span class="workbench-table__primary">{{ row.name }}</span></td>
            <td class="mono">{{ row.code }}</td>
            <td><StatusBadge :label="row.type_display" status="info" size="sm" /></td>
            <td class="amount-cell">¥{{ row.value_yuan }}</td>
            <td>¥{{ row.min_amount_yuan }}</td>
            <td>{{ row.used }}/{{ row.total }}</td>
            <td>{{ row.start_time }} ~ {{ row.end_time }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="!loading && !coupons.length" class="table-empty">暂无优惠券</div>
    </section>

    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal-shell store-surface store-surface--elevated">
        <div class="modal-shell__header">
          <div>
            <div class="store-panel-title">创建优惠券</div>
            <div class="store-panel-subtitle">配置券码规则、面额和有效范围</div>
          </div>
          <button class="modal-close" type="button" @click="showCreate = false">×</button>
        </div>

        <form class="modal-form" @submit.prevent="handleCreate">
          <div class="field">
            <label>名称</label>
            <input v-model="form.name" type="text" placeholder="如：新人专享券" required />
          </div>
          <div class="field">
            <label>优惠码</label>
            <input v-model="form.code" type="text" placeholder="如：NEW2026" required />
          </div>
          <div class="field">
            <label>类型</label>
            <div class="type-select">
              <button v-for="type in typeOptions" :key="type.value" type="button" :class="['result-chip', { 'is-active': form.type === type.value }]" @click="form.type = type.value">
                {{ type.label }}
              </button>
            </div>
          </div>
          <div class="field-row">
            <div class="field">
              <label>面额</label>
              <input v-model.number="form.value" type="number" min="1" required />
            </div>
            <div class="field">
              <label>最低消费</label>
              <input v-model.number="form.min_amount" type="number" min="0" />
            </div>
          </div>
          <div class="field">
            <label>总量</label>
            <input v-model.number="form.total" type="number" min="1" required />
          </div>
          <div class="modal-actions">
            <button class="ghost-btn" type="button" @click="showCreate = false">取消</button>
            <button class="primary-btn" type="submit">创建</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import StatusBadge from '../../components/StatusBadge.vue'
import request from '../../utils/request'

const coupons = ref([])
const loading = ref(false)
const showCreate = ref(false)
const form = ref({ name: '', code: '', type: 'minus', value: 0, min_amount: 0, total: 100 })

const typeOptions = [
  { label: '满减券', value: 'minus' },
  { label: '折扣券', value: 'discount' },
  { label: '固定金额', value: 'fixed' },
]

async function fetchData() {
  loading.value = true
  try {
    const res = await request.get('/marketing/admin/coupons/')
    coupons.value = res.data.results || []
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  await request.post('/marketing/admin/coupons/', form.value)
  ElMessage.success('优惠券创建成功')
  showCreate.value = false
  form.value = { name: '', code: '', type: 'minus', value: 0, min_amount: 0, total: 100 }
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
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

.mono {
  font-family: 'SF Mono', 'Fira Code', monospace;
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

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(16, 24, 40, 0.34);
  backdrop-filter: blur(8px);
}

.modal-shell {
  width: min(560px, calc(100vw - 32px));
  padding: var(--sp-6);
}

.modal-shell__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
  margin-bottom: var(--sp-5);
}

.modal-close {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 12px;
  background: var(--glass-border);
  color: var(--text-primary);
  font-size: var(--text-lg);
}

.modal-form {
  display: grid;
  gap: var(--sp-4);
}

.field,
.field-row {
  display: grid;
  gap: var(--sp-3);
}

.field-row {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

.field label {
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.field input {
  width: 100%;
  height: 44px;
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 0 var(--sp-4);
}

.field input:focus {
  outline: none;
  border-color: rgba(198, 168, 106, 0.4);
  box-shadow: 0 0 0 4px rgba(198, 168, 106, 0.12);
}

.type-select,
.modal-actions {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-2);
}

.modal-actions {
  justify-content: flex-end;
  margin-top: var(--sp-2);
}
</style>
