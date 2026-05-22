<template>
  <div class="store-page" v-loading="loading">
    <StorePageHeader eyebrow="Order Detail" icon="package" title="订单详情" :subtitle="order ? `订单号：${order.order_no}` : '查看订单状态、商品内容与支付动作。'" compact />

    <div class="store-page-body" v-if="order">
      <div class="container">
        <div class="transaction-shell">
          <div class="transaction-main">
            <section class="store-surface status-panel">
              <div class="status-panel__icon">
                <AnimatedIcons :name="statusIcon" :size="28" />
              </div>
              <div>
                <div class="store-panel-title">{{ order.status_display }}</div>
                <p class="status-panel__desc" v-if="order.status === 'pending'">请在有效时间内完成支付，订单会保留在你的账户记录里。</p>
                <p class="status-panel__desc" v-else-if="order.status === 'completed'">订单已完成，可前往下载中心获取资源。</p>
                <p class="status-panel__desc" v-else-if="order.status === 'cancelled'">订单已取消，如需购买可重新下单。</p>
                <p class="status-panel__desc" v-else>订单已支付，等待系统完成交付流程。</p>
              </div>
            </section>

            <section class="store-surface store-surface--soft">
              <div class="store-panel-header">
                <div>
                  <div class="store-panel-title">商品清单</div>
                  <div class="store-panel-subtitle">本次订单包含的资源</div>
                </div>
              </div>

              <div class="detail-items">
                <article v-for="item in order.items" :key="item.id" class="detail-item">
                  <div>
                    <h4>{{ item.product_name }}</h4>
                    <p>{{ item.sku_name }}</p>
                  </div>
                  <div class="detail-item__price">¥{{ item.price_yuan }}</div>
                </article>
              </div>
            </section>

            <section class="store-surface store-surface--soft">
              <div class="store-panel-header">
                <div>
                  <div class="store-panel-title">订单信息</div>
                  <div class="store-panel-subtitle">用于追踪支付、创建时间与备注</div>
                </div>
              </div>

              <div class="info-grid">
                <div class="info-row">
                  <span class="info-label">订单号</span>
                  <span class="info-value mono">{{ order.order_no }}</span>
                </div>
                <div class="info-row">
                  <span class="info-label">创建时间</span>
                  <span class="info-value">{{ order.created_at }}</span>
                </div>
                <div v-if="order.pay_time" class="info-row">
                  <span class="info-label">支付时间</span>
                  <span class="info-value">{{ order.pay_time }}</span>
                </div>
                <div v-if="order.remark" class="info-row">
                  <span class="info-label">备注</span>
                  <span class="info-value">{{ order.remark }}</span>
                </div>
              </div>
            </section>
          </div>

          <aside class="summary-rail">
            <div class="summary-rail__inner store-surface store-surface--elevated">
              <div class="store-panel-title">订单摘要</div>
              <div class="store-panel-subtitle">金额与操作入口</div>

              <div class="summary-rail__rows">
                <div class="summary-rail__row">
                  <span>商品合计</span>
                  <span>¥{{ order.total_amount_yuan }}</span>
                </div>
                <div v-if="order.discount_amount_yuan > 0" class="summary-rail__row">
                  <span>优惠减免</span>
                  <span class="discount">-¥{{ order.discount_amount_yuan }}</span>
                </div>
              </div>

              <div class="summary-rail__divider" />

              <div class="summary-rail__row total">
                <span>应付金额</span>
                <span class="summary-rail__price">¥{{ order.pay_amount_yuan }}</span>
              </div>

              <div class="summary-rail__actions">
                <template v-if="order.status === 'pending'">
                  <button class="action-primary" type="button" @click="handlePayConfirm">立即支付</button>
                  <button class="action-ghost" type="button" @click="handleCancel">取消订单</button>
                </template>

                <router-link v-if="order.status === 'completed'" to="/downloads" class="action-primary action-link">
                  <AnimatedIcons name="download" :size="18" />
                  前往下载
                </router-link>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { cancelOrder, getOrder } from '../../api/order'
import { createPayment } from '../../api/payment'

const route = useRoute()
const order = ref(null)
const loading = ref(false)

const statusIcon = computed(() => {
  const map = { pending: 'calendar', completed: 'check', cancelled: 'close', paid: 'send' }
  return map[order.value?.status] || 'shield'
})

async function refreshOrder() {
  const res = await getOrder(route.params.id)
  order.value = res.data
}

onMounted(async () => {
  loading.value = true
  try {
    await refreshOrder()
  } finally {
    loading.value = false
  }
})

async function handlePayConfirm() {
  try {
    const payRes = await createPayment({ order_id: order.value.id, method: 'alipay' })
    const payUrl = payRes.data.pay_url
    if (payUrl) {
      window.location.href = payUrl
    } else {
      ElMessage.error('获取支付链接失败')
    }
  } catch (err) {
    ElMessage.error(err.message || '支付失败')
  }
}

async function handleCancel() {
  try {
    await ElMessageBox.confirm('确定取消这笔订单吗？', '取消订单')
    await cancelOrder(order.value.id)
    ElMessage.success('订单已取消')
    await refreshOrder()
  } catch {}
}
</script>

<style scoped>
.status-panel {
  display: flex;
  gap: var(--sp-4);
  align-items: center;
  padding: var(--sp-6);
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.12), rgba(139, 92, 246, 0.06));
}

.status-panel__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 18px;
  background: var(--glass-bg);
  color: var(--accent);
}

.status-panel__desc {
  margin-top: var(--sp-2);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.8;
}

.detail-items {
  display: grid;
}

.detail-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
  padding: var(--sp-5) var(--sp-6);
  border-top: 1px solid var(--glass-border);
}

.detail-item h4 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.detail-item p {
  margin-top: 4px;
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.detail-item__price {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 800;
}

.info-grid {
  padding: 0 var(--sp-6) var(--sp-6);
}

.info-row {
  display: flex;
  justify-content: space-between;
  gap: var(--sp-4);
  padding: var(--sp-4) 0;
  border-top: 1px solid var(--glass-border);
}

.info-label {
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.info-value {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.mono {
  font-family: 'SF Mono', 'Fira Code', monospace;
}

.discount {
  color: var(--success);
}

.action-primary,
.action-ghost {
  width: 100%;
  height: 48px;
  border-radius: 14px;
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.action-primary {
  border: none;
  background: var(--gradient-blue);
  color: var(--white);
}

.action-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  text-decoration: none;
}

.action-ghost {
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  color: var(--text-secondary);
}
</style>
