<template>
  <div class="store-page">
    <template v-if="loading">
      <div class="store-page-body">
        <div class="container">
          <div class="detail-shell">
            <div class="store-surface skeleton-card">
              <div class="skeleton skeleton-gallery" />
            </div>
            <div class="store-surface skeleton-card">
              <div class="skeleton skeleton-title-lg" />
              <div class="skeleton skeleton-meta" />
              <div class="skeleton skeleton-price-block" />
              <div class="skeleton skeleton-btn" />
            </div>
          </div>
        </div>
      </div>
    </template>

    <template v-else-if="product">
      <StorePageHeader
        :eyebrow="product.category_name || 'Product'"
        icon="layers"
        :title="product.name"
        :subtitle="`${product.download_count} 次下载 · v${product.version}`"
        compact
      />

      <div class="store-page-body">
        <div class="container">
          <div class="detail-shell">
            <section class="store-surface store-surface--soft detail-gallery">
              <div class="gallery-main" @mousemove="onGalleryMove" @mouseleave="onGalleryLeave" ref="galleryRef">
                <img :src="activeImage || product.main_image" :alt="product.name" ref="galleryImgRef" />
                <div class="gallery-lens" v-show="showLens" :style="lensStyle" />
              </div>

              <div class="gallery-thumbs" v-if="product.images?.length">
                <button :class="['thumb', { active: !activeImage }]" type="button" @click="activeImage = null">
                  <img :src="product.main_image" alt="主图" />
                </button>
                <button v-for="img in product.images" :key="img.id" :class="['thumb', { active: activeImage === img.image }]" type="button" @click="activeImage = img.image">
                  <img :src="img.image" alt="预览图" />
                </button>
              </div>
            </section>

            <aside class="store-surface store-surface--elevated detail-sidebar">
              <div class="detail-sidebar__top">
                <span v-if="product.category_name" class="category-pill">{{ product.category_name }}</span>
                <h2>{{ product.name }}</h2>
                <div class="detail-meta">
                  <span>{{ product.download_count }} 次下载</span>
                  <span>版本 v{{ product.version }}</span>
                </div>
              </div>

              <div class="price-block">
                <span class="price-current">¥{{ displayPrice }}</span>
                <span v-if="selectedSku?.original_price_yuan" class="price-original">¥{{ selectedSku.original_price_yuan }}</span>
              </div>

              <div v-if="product.skus?.length" class="sku-section">
                <label class="sku-label">选择版本</label>
                <div class="sku-grid">
                  <button
                    v-for="sku in product.skus"
                    :key="sku.id"
                    :class="['sku-card', { active: selectedSku?.id === sku.id }]"
                    type="button"
                    @click="selectedSku = sku"
                  >
                    <span class="sku-name">{{ sku.name }}</span>
                    <span class="sku-price">¥{{ sku.price_yuan }}</span>
                    <span v-if="sku.license_description" class="sku-desc">{{ sku.license_description }}</span>
                  </button>
                </div>
              </div>

              <div class="detail-actions">
                <button :class="['buy-btn', { success: addedToCart }]" type="button" @click="handleBuyNow">
                  <span class="btn-content">
                    <AnimatedIcons :name="addedToCart ? 'check' : 'zap'" :size="18" />
                    {{ addedToCart ? '已加入购物车' : '立即购买' }}
                  </span>
                </button>
                <button class="cart-btn" type="button" @click="handleAddToCart">
                  <AnimatedIcons v-if="addingToCart" name="spinner" :size="18" speed="fast" />
                  <template v-else>
                    <AnimatedIcons :name="addedToCart ? 'check' : 'cart'" :size="18" />
                    {{ addedToCart ? '已加入' : '加入购物车' }}
                  </template>
                </button>
              </div>

              <div class="detail-benefits">
                <div v-for="feature in features" :key="feature.text" class="benefit-row">
                  <AnimatedIcons :name="feature.icon" :size="16" />
                  <span>{{ feature.text }}</span>
                </div>
              </div>
            </aside>
          </div>

          <section class="store-surface store-surface--soft detail-tabs">
            <div class="tab-nav">
              <button v-for="tab in tabs" :key="tab.key" :class="['tab-btn', { active: activeTab === tab.key }]" type="button" @click="activeTab = tab.key">
                {{ tab.label }}
              </button>
            </div>
            <div class="tab-content">
              <div v-if="activeTab === 'desc'" class="desc-content" v-html="safeDescription || '暂无描述'" />
              <div v-else-if="activeTab === 'changelog'" class="desc-content">{{ product.changelog || '暂无更新日志' }}</div>
              <div v-else class="desc-content">评价模块将在下一轮重构中接入。</div>
            </div>
          </section>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { getProduct } from '../../api/product'
import { useCartStore } from '../../stores/cart'
import { useUserStore } from '../../stores/user'

const route = useRoute()
const router = useRouter()
const cartStore = useCartStore()
const userStore = useUserStore()

const product = ref(null)
const selectedSku = ref(null)
const activeImage = ref(null)
const activeTab = ref('desc')
const loading = ref(false)
const addingToCart = ref(false)
const addedToCart = ref(false)

function sanitizeHTML(html) {
  const div = document.createElement('div')
  div.textContent = html
  return div.innerHTML
}

const safeDescription = computed(() => product.value?.description ? sanitizeHTML(product.value.description) : '')

const galleryRef = ref(null)
const galleryImgRef = ref(null)
const showLens = ref(false)
const lensStyle = ref({})

const displayPrice = computed(() => (selectedSku.value ? selectedSku.value.price_yuan : product.value?.min_price_yuan))

const features = [
  { icon: 'download', text: '购买后即时下载' },
  { icon: 'refresh', text: '资源持续维护更新' },
  { icon: 'shield', text: '授权与交付说明清晰' },
]

const tabs = [
  { key: 'desc', label: '商品描述' },
  { key: 'changelog', label: '更新日志' },
  { key: 'reviews', label: '评价' },
]

onMounted(async () => {
  loading.value = true
  try {
    const res = await getProduct(route.params.id)
    product.value = res.data
    if (product.value.skus?.length) selectedSku.value = product.value.skus[0]
  } finally {
    loading.value = false
  }
})

function onGalleryMove(e) {
  const rect = galleryRef.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  showLens.value = true
  lensStyle.value = {
    left: `${x}px`,
    top: `${y}px`,
    background: `radial-gradient(circle 80px at ${x}px ${y}px, rgba(255,255,255,0.18) 0%, transparent 100%)`,
  }
}

function onGalleryLeave() {
  showLens.value = false
}

function ensureAuth() {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return false
  }
  return true
}

function handleAddToCart() {
  if (!ensureAuth()) return
  if (!selectedSku.value) {
    ElMessage.warning('请先选择一个版本')
    return
  }

  addingToCart.value = true
  cartStore.addItem(selectedSku.value.id).then(() => {
    addingToCart.value = false
    addedToCart.value = true
    ElMessage.success('已加入购物车')
    setTimeout(() => {
      addedToCart.value = false
    }, 2000)
  })
}

function handleBuyNow() {
  if (!ensureAuth()) return
  if (!selectedSku.value) {
    ElMessage.warning('请先选择一个版本')
    return
  }
  cartStore.addItem(selectedSku.value.id).then(() => router.push('/cart'))
}
</script>

<style scoped>
.detail-shell {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 420px;
  gap: var(--sp-6);
  margin-bottom: var(--sp-6);
}

.detail-gallery {
  padding: var(--sp-6);
}

.gallery-main {
  position: relative;
  overflow: hidden;
  aspect-ratio: 4 / 3;
  border-radius: 20px;
  background: var(--surface-2);
}

.gallery-main img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery-lens {
  position: absolute;
  width: 160px;
  height: 160px;
  border-radius: 999px;
  transform: translate(-50%, -50%);
  pointer-events: none;
  mix-blend-mode: screen;
}

.gallery-thumbs {
  display: flex;
  gap: var(--sp-2);
  margin-top: var(--sp-3);
}

.thumb {
  overflow: hidden;
  width: 72px;
  height: 72px;
  border: 2px solid transparent;
  border-radius: 14px;
  padding: 0;
  background: none;
}

.thumb.active {
  border-color: var(--accent);
}

.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.detail-sidebar {
  padding: var(--sp-6);
}

.category-pill {
  display: inline-flex;
  align-items: center;
  height: 30px;
  padding: 0 var(--sp-3);
  border-radius: 999px;
  background: rgba(59, 130, 246, 0.12);
  color: var(--accent);
  font-family: var(--font-display);
  font-size: var(--text-xs);
  font-weight: 700;
}

.detail-sidebar__top h2 {
  margin-top: var(--sp-4);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(1.8rem, 2.5vw, 2.4rem);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.04em;
}

.detail-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--sp-3);
  margin-top: var(--sp-4);
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.price-block {
  display: flex;
  align-items: baseline;
  gap: var(--sp-3);
  margin-top: var(--sp-6);
}

.price-current {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: 800;
  letter-spacing: -0.04em;
}

.price-original {
  color: var(--text-muted);
  font-size: var(--text-base);
  text-decoration: line-through;
}

.sku-section {
  margin-top: var(--sp-6);
}

.sku-label {
  display: inline-flex;
  margin-bottom: var(--sp-3);
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.sku-grid {
  display: grid;
  gap: var(--sp-3);
}

.sku-card {
  display: grid;
  gap: 6px;
  padding: var(--sp-4);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  background: var(--glass-bg);
  text-align: left;
}

.sku-card.active {
  border-color: rgba(59, 130, 246, 0.36);
  background: rgba(59, 130, 246, 0.08);
}

.sku-name {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.sku-price {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.sku-desc {
  color: var(--text-secondary);
  font-size: var(--text-xs);
  line-height: 1.7;
}

.detail-actions {
  display: grid;
  gap: var(--sp-3);
  margin-top: var(--sp-6);
}

.buy-btn,
.cart-btn {
  width: 100%;
  height: 50px;
  border-radius: 14px;
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.buy-btn {
  border: none;
  background: var(--gradient-blue);
  color: var(--white);
}

.buy-btn.success {
  background: var(--success);
}

.cart-btn {
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  color: var(--text-primary);
}

.btn-content {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
}

.detail-benefits {
  display: grid;
  gap: var(--sp-3);
  margin-top: var(--sp-6);
}

.benefit-row {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.detail-tabs {
  overflow: hidden;
}

.tab-nav {
  display: flex;
  gap: var(--sp-2);
  padding: var(--sp-5) var(--sp-6) var(--sp-4);
}

.tab-btn {
  height: 38px;
  padding: 0 var(--sp-4);
  border: none;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.06);
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.tab-btn.active {
  background: var(--accent);
  color: var(--white);
}

.tab-content {
  padding: 0 var(--sp-6) var(--sp-6);
}

.desc-content {
  color: var(--text-secondary);
  line-height: 1.9;
}

.skeleton-card {
  padding: var(--sp-6);
}

.skeleton-gallery {
  aspect-ratio: 4 / 3;
  border-radius: 20px;
}

.skeleton-title-lg {
  height: 32px;
  width: 80%;
  margin-bottom: var(--sp-4);
}

.skeleton-meta {
  height: 18px;
  width: 45%;
  margin-bottom: var(--sp-4);
}

.skeleton-price-block {
  height: 80px;
  border-radius: 20px;
  margin-bottom: var(--sp-4);
}

.skeleton-btn {
  height: 50px;
  border-radius: 14px;
}

@media (max-width: 1200px) {
  .detail-shell {
    grid-template-columns: 1fr;
  }

  .detail-sidebar {
    position: sticky;
    top: calc(var(--nav-h) + var(--sp-4));
  }
}
</style>
