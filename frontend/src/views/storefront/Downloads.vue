<template>
  <div class="store-page">
    <StorePageHeader eyebrow="Downloads" icon="download" title="我的下载" subtitle="所有已购买并可再次获取的资源都会集中在这里。" compact />

    <div class="store-page-body">
      <div class="container">
        <div class="account-shell">
          <StoreAccountNav />

          <div class="account-content" v-loading="loading">
            <section v-for="order in orders" :key="order.id" class="store-surface store-surface--soft download-section">
              <div class="store-panel-header">
                <div>
                  <div class="store-panel-title">订单 {{ order.order_no }}</div>
                  <div class="store-panel-subtitle">{{ order.created_at }}</div>
                </div>
              </div>

              <div class="download-grid">
                <article v-for="item in order.items" :key="item.id" class="download-card">
                  <div class="download-card__icon">
                    <AnimatedIcons name="layers" :size="22" />
                  </div>
                  <div class="download-card__copy">
                    <h3>{{ item.product_name }}</h3>
                    <p>{{ item.sku_name }}</p>
                  </div>
                  <button class="download-card__action" type="button" @click="handleDownload(order.id, item.id)">
                    <AnimatedIcons name="download" :size="18" />
                    下载
                  </button>
                </article>
              </div>
            </section>

            <div v-if="!loading && !orders.length" class="empty-state store-surface store-surface--soft">
              <div class="empty-icon">
                <AnimatedIcons name="download" :size="32" />
              </div>
              <h3>暂无可下载内容</h3>
              <p>完成购买后，这里会显示你已获得的资源。</p>
              <router-link to="/products" class="empty-action">浏览商品</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StoreAccountNav from '../../components/StoreAccountNav.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { getDownloadToken, getDownloads } from '../../api/order'

const orders = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await getDownloads()
    orders.value = res.data.results || []
  } finally {
    loading.value = false
  }
})

async function handleDownload(orderId, itemId) {
  try {
    const res = await getDownloadToken(orderId, itemId)
    ElMessage.success(`下载令牌：${res.data.download_token}`)
  } catch (error) {
    ElMessage.error(error.message || '下载失败')
  }
}
</script>

<style scoped>
.download-section {
  overflow: hidden;
}

.download-grid {
  display: grid;
  gap: var(--sp-3);
  padding: 0 var(--sp-6) var(--sp-6);
}

.download-card {
  display: grid;
  grid-template-columns: 56px minmax(0, 1fr) auto;
  gap: var(--sp-4);
  align-items: center;
  padding: var(--sp-4);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  background: var(--glass-bg);
}

.download-card__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: rgba(59, 130, 246, 0.12);
  color: var(--accent);
}

.download-card__copy h3 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.download-card__copy p {
  margin-top: 4px;
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.download-card__action {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  height: 40px;
  padding: 0 var(--sp-5);
  border: none;
  border-radius: 12px;
  background: var(--gradient-blue);
  color: var(--white);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

@media (max-width: 768px) {
  .download-card {
    grid-template-columns: 56px 1fr;
  }

  .download-card__action {
    grid-column: 1 / -1;
    justify-content: center;
  }
}
</style>
