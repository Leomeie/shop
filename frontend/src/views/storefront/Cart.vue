<template>
  <div class="store-page">
    <StorePageHeader
      eyebrow="Cart"
      icon="cart"
      title="购物车"
      :subtitle="cartStore.items.length ? `已加入 ${cartStore.items.length} 项资源，随时准备结算。` : '还没有加入资源，先去逛逛商品库。'"
      compact
    />

    <div class="store-page-body">
      <div class="container">
        <div v-if="cartStore.items.length" class="transaction-shell">
          <div class="transaction-main">
            <section class="store-surface store-surface--soft cart-panel">
              <div class="store-panel-header">
                <div>
                  <div class="store-panel-title">待结算资源</div>
                  <div class="store-panel-subtitle">管理商品、数量与勾选状态</div>
                </div>
              </div>

              <TransitionGroup name="cart-item" tag="div" class="cart-items">
                <article v-for="item in cartStore.items" :key="item.sku_id" class="cart-row">
                  <label class="item-check">
                    <input type="checkbox" :checked="item.selected" @change="(e) => cartStore.updateItem(item.sku_id, { selected: e.target.checked })" />
                    <span class="checkmark">
                      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                    </span>
                  </label>

                  <div class="item-thumb">
                    <img :src="item.image" :alt="item.product_name" loading="lazy" />
                  </div>

                  <div class="item-main">
                    <h3>{{ item.product_name }}</h3>
                    <p>{{ item.sku_name }}</p>
                  </div>

                  <div class="item-meta">
                    <div class="meta-label">单价</div>
                    <div class="meta-value">¥{{ item.price_yuan }}</div>
                  </div>

                  <div class="item-qty">
                    <button class="qty-btn" type="button" @click="cartStore.updateItem(item.sku_id, { quantity: Math.max(1, item.quantity - 1) })">
                      <AnimatedIcons name="minus" :size="14" />
                    </button>
                    <span :class="['qty-val', { 'qty-pulse': qtyPulse === item.sku_id }]">{{ item.quantity }}</span>
                    <button class="qty-btn" type="button" @click="handleQtyChange(item.sku_id, item.quantity + 1)">
                      <AnimatedIcons name="plus" :size="14" />
                    </button>
                  </div>

                  <div class="item-meta item-meta--total">
                    <div class="meta-label">小计</div>
                    <div class="meta-value">¥{{ item.subtotal_yuan }}</div>
                  </div>

                  <button class="item-remove" type="button" @click="cartStore.removeItem(item.sku_id)">
                    <AnimatedIcons name="close" :size="16" />
                  </button>
                </article>
              </TransitionGroup>
            </section>
          </div>

          <aside class="summary-rail">
            <div class="summary-rail__inner store-surface store-surface--elevated">
              <div class="store-panel-title">订单摘要</div>
              <div class="store-panel-subtitle">只统计已勾选的商品</div>

              <div class="summary-rail__rows">
                <div class="summary-rail__row">
                  <span>商品数量</span>
                  <span>{{ cartStore.selectedItems.length }} 件</span>
                </div>
                <div class="summary-rail__row">
                  <span>结算状态</span>
                  <span>{{ cartStore.selectedItems.length ? '可提交' : '未选择' }}</span>
                </div>
              </div>

              <div class="summary-rail__divider" />

              <div class="summary-rail__row total">
                <span>应付金额</span>
                <span class="summary-rail__price">¥{{ cartStore.selectedTotal }}</span>
              </div>

              <div class="summary-rail__actions">
                <button class="checkout-btn" type="button" :disabled="!cartStore.selectedItems.length" @click="$router.push('/checkout')">
                  <span class="checkout-content">
                    继续结算
                    <AnimatedIcons name="arrow-right" :size="18" />
                  </span>
                </button>
                <div class="secure-note">
                  <AnimatedIcons name="shield" :size="14" />
                  <span>安全支付与资源交付保障</span>
                </div>
              </div>
            </div>
          </aside>
        </div>

        <div v-else class="empty-state store-surface store-surface--soft">
          <div class="empty-icon">
            <AnimatedIcons name="cart" :size="32" />
          </div>
          <h3>购物车还是空的</h3>
          <p>去挑几件适合当前工作流的资源，再回来统一结算。</p>
          <router-link to="/products" class="empty-action">浏览商品</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { useCartStore } from '../../stores/cart'

const cartStore = useCartStore()
const qtyPulse = ref(null)
let qtyTimer = null

function handleQtyChange(skuId, qty) {
  cartStore.updateItem(skuId, { quantity: qty })
  qtyPulse.value = skuId
  clearTimeout(qtyTimer)
  qtyTimer = setTimeout(() => {
    qtyPulse.value = null
  }, 400)
}

onUnmounted(() => clearTimeout(qtyTimer))
</script>

<style scoped>
.cart-panel {
  overflow: hidden;
}

.cart-items {
  display: grid;
}

.cart-row {
  display: grid;
  grid-template-columns: auto 84px minmax(0, 1fr) 120px 132px 120px auto;
  gap: var(--sp-4);
  align-items: center;
  padding: var(--sp-5) var(--sp-6);
  border-top: 1px solid var(--glass-border);
}

.item-check {
  position: relative;
  display: flex;
  cursor: pointer;
}

.item-check input {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
}

.checkmark {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border: 1px solid var(--glass-border);
  border-radius: 8px;
  color: transparent;
  transition: color var(--dur-fast) var(--ease-out), background var(--dur-fast) var(--ease-out);
}

.item-check input:checked + .checkmark {
  border-color: var(--accent);
  background: var(--accent);
  color: var(--white);
}

.item-thumb {
  overflow: hidden;
  width: 84px;
  height: 84px;
  border-radius: 16px;
  background: var(--surface-2);
}

.item-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-main h3 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.item-main p {
  margin-top: var(--sp-1);
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.item-meta {
  display: grid;
  gap: 4px;
}

.meta-label {
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.meta-value {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.item-meta--total .meta-value {
  font-size: var(--text-lg);
}

.item-qty {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--glass-border);
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.03);
}

.qty-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--text-secondary);
}

.qty-val {
  width: 40px;
  text-align: center;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-weight: 700;
}

.qty-pulse {
  animation: qtyPulseAnim 0.4s var(--ease-spring);
}

.item-remove {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 12px;
  background: transparent;
  color: var(--text-muted);
}

.item-remove:hover {
  background: rgba(214, 69, 69, 0.08);
  color: var(--error);
}

.checkout-btn {
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

.checkout-btn:disabled {
  opacity: 0.4;
}

.checkout-content {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
}

.secure-note {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  color: var(--text-muted);
  font-size: var(--text-xs);
}

@keyframes qtyPulseAnim {
  0% { transform: scale(1); }
  50% { transform: scale(1.22); }
  100% { transform: scale(1); }
}

@media (max-width: 1200px) {
  .cart-row {
    grid-template-columns: auto 72px minmax(0, 1fr) 90px 110px;
    grid-template-areas:
      "check thumb main price remove"
      "check thumb qty total";
  }

  .item-check { grid-area: check; }
  .item-thumb { grid-area: thumb; }
  .item-main { grid-area: main; }
  .item-qty { grid-area: qty; }
  .item-meta { grid-area: price; }
  .item-meta--total { grid-area: total; }
  .item-remove { grid-area: remove; justify-self: end; }
}

@media (max-width: 768px) {
  .cart-row {
    grid-template-columns: auto 72px minmax(0, 1fr);
    grid-template-areas:
      "check thumb main"
      ". qty total";
    padding: var(--sp-4);
  }
}
</style>
