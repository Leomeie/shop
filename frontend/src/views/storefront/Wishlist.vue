<template>
  <div class="store-page">
    <StorePageHeader eyebrow="Wishlist" icon="heart" title="我的收藏" subtitle="把关注中的资源放在一起，方便后续比较与回看。" compact />

    <div class="store-page-body">
      <div class="container">
        <div class="account-shell">
          <StoreAccountNav />

          <div class="account-content">
            <section v-if="loading" class="wishlist-grid">
              <div v-for="i in 6" :key="i" class="skeleton-card">
                <div class="skeleton skeleton-img" />
                <div class="skeleton-body">
                  <div class="skeleton skeleton-cat" />
                  <div class="skeleton skeleton-title" />
                  <div class="skeleton skeleton-price" />
                </div>
              </div>
            </section>

            <section v-else-if="items.length" class="wishlist-grid">
              <div v-for="item in items" :key="item.id" class="grid-item">
                <ProductCard :product="item" />
              </div>
            </section>

            <div v-else class="empty-state store-surface store-surface--soft">
              <div class="empty-icon">
                <AnimatedIcons name="heart" :size="32" />
              </div>
              <h3>收藏夹还是空的</h3>
              <p>浏览商品时点击收藏，把想对比的资源先存下来。</p>
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
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import ProductCard from '../../components/ProductCard.vue'
import StoreAccountNav from '../../components/StoreAccountNav.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { getProducts } from '../../api/product'

const items = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await getProducts({ is_featured: true, page_size: 12 })
    items.value = res.data.results || []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-5);
}

.grid-item {
  min-width: 0;
}

.skeleton-card {
  overflow: hidden;
  border: 1px solid var(--glass-border);
  border-radius: var(--r-lg);
  background: var(--glass-bg);
}

.skeleton-img {
  aspect-ratio: 4 / 3;
}

.skeleton-body {
  padding: var(--sp-4) var(--sp-5) var(--sp-5);
}

.skeleton-cat {
  height: 12px;
  width: 60px;
  margin-bottom: var(--sp-3);
}

.skeleton-title {
  height: 16px;
  width: 100%;
  margin-bottom: var(--sp-3);
}

.skeleton-price {
  height: 20px;
  width: 60px;
}

@media (max-width: 1200px) {
  .wishlist-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .wishlist-grid {
    grid-template-columns: 1fr;
  }
}
</style>
