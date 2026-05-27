<template>
  <div class="store-page">
    <StorePageHeader
      eyebrow="Checkout"
      icon="zap"
      title="确认订单"
      subtitle="再次核对资源内容与备注信息，然后提交订单。"
      compact
    />

    <div class="store-page-body">
      <div class="container">
        <div class="transaction-shell">
          <div class="transaction-main">
            <section class="store-surface store-surface--soft">
              <div class="store-panel-header">
                <div>
                  <div class="store-panel-title">商品清单</div>
                  <div class="store-panel-subtitle">本次将一并创建订单的资源</div>
                </div>
              </div>

              <div class="checkout-items">
                <article v-for="item in cartStore.selectedItems" :key="item.sku_id" class="checkout-row">
                  <div class="checkout-row__thumb">
                    <img :src="item.image" :alt="item.product_name" loading="lazy" />
                  </div>
                  <div class="checkout-row__main">
                    <h3>{{ item.product_name }}</h3>
                    <p>{{ item.sku_name }}</p>
                  </div>
                  <div class="checkout-row__price">¥{{ item.price_yuan }} × {{ item.quantity }}</div>
                  <div class="checkout-row__subtotal">¥{{ item.subtotal_yuan }}</div>
                </article>
              </div>
            </section>

            <section class="store-surface store-surface--soft note-panel">
              <div class="store-panel-header">
                <div>
                  <div class="store-panel-title">订单备注</div>
                  <div class="store-panel-subtitle">可选，用于补充交付说明或特殊需求</div>
                </div>
              </div>

              <div class="note-body">
                <textarea v-model="remark" class="remark-input" rows="4" placeholder="例如：请优先提供适用于商业项目的版本说明。" />
              </div>
            </section>
          </div>

          <aside class="summary-rail">
            <div class="summary-rail__inner store-surface store-surface--elevated">
              <div class="store-panel-title">订单摘要</div>
              <div class="store-panel-subtitle">提交后将跳转到订单详情页</div>

              <div class="summary-rail__rows">
                <div class="summary-rail__row">
                  <span>商品数量</span>
                  <span>{{ cartStore.selectedItems.length }} 件</span>
                </div>
                <div class="summary-rail__row">
                  <span>支付方式</span>
                  <span>系统默认</span>
                </div>
              </div>

              <div class="summary-rail__divider" />

              <div class="summary-rail__row total">
                <span>应付金额</span>
                <span class="summary-rail__price">¥{{ cartStore.selectedTotal }}</span>
              </div>

              <div class="summary-rail__actions">
                <button class="submit-btn" type="button" :disabled="loading" @click="handleCreateOrder">
                  <AnimatedIcons v-if="loading" name="spinner" :size="20" speed="fast" />
                  <span v-else class="submit-btn__content">
                    提交订单
                    <AnimatedIcons name="arrow-right" :size="18" />
                  </span>
                </button>
                <div class="secure-note">
                  <AnimatedIcons name="shield" :size="14" />
                  <span>订单创建后将保留下载与支付记录</span>
                </div>
              </div>
            </div>
          </aside>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { gsap } from '../../composables/useGsap.js'
import { ElMessage } from 'element-plus'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { createOrder } from '../../api/order'
import { useCartStore } from '../../stores/cart'

const router = useRouter()
const cartStore = useCartStore()
const remark = ref('')
const loading = ref(false)

let ctx = null

onMounted(() => {
  // GSAP entrance animations removed — gsap.from() caused elements to stay invisible
})

onUnmounted(() => ctx?.revert())

async function handleCreateOrder() {
  loading.value = true
  try {
    const res = await createOrder({ remark: remark.value })
    ElMessage.success('订单已创建')
    router.push(`/orders/${res.data.id}`)
  } catch {} finally {
    loading.value = false
  }
}
</script>

<style scoped>
.checkout-items {
  display: grid;
}

.checkout-row {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr) 132px 110px;
  gap: var(--sp-4);
  align-items: center;
  padding: var(--sp-5) var(--sp-6);
  border-top: 1px solid var(--glass-border);
}

.checkout-row__thumb {
  overflow: hidden;
  width: 72px;
  height: 72px;
  border-radius: 14px;
  background: var(--surface-2);
}

.checkout-row__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.checkout-row__main h3 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.checkout-row__main p {
  margin-top: var(--sp-1);
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.checkout-row__price {
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.checkout-row__subtotal {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 800;
  text-align: right;
}

.note-body {
  padding: 0 var(--sp-6) var(--sp-6);
}

.remark-input {
  width: 100%;
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: var(--sp-4);
  background: var(--glass-bg);
  font-size: var(--text-sm);
  line-height: 1.8;
  color: var(--text-primary);
  resize: vertical;
}

.remark-input:focus {
  outline: none;
  border-color: rgba(59, 130, 246, 0.45);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.12);
}

.submit-btn {
  width: 100%;
  height: 52px;
  border: none;
  border-radius: 14px;
  background: var(--gradient-blue);
  color: var(--white);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.submit-btn__content {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
}

@media (max-width: 768px) {
  .checkout-row {
    grid-template-columns: 72px minmax(0, 1fr);
    gap: var(--sp-3);
  }

  .checkout-row__price,
  .checkout-row__subtotal {
    grid-column: 2;
    text-align: left;
    margin-top: var(--sp-2);
  }

  .checkout-row__subtotal {
    margin-top: var(--sp-1);
  }
}
</style>
