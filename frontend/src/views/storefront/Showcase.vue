<template>
  <div class="store-page">
    <StorePageHeader eyebrow="Showcase" icon="image" title="精选专题" subtitle="围绕热门资源与最新上架内容整理的专题展示页。" compact />

    <div class="store-page-body">
      <div class="container showcase-stack">
        <section class="store-surface store-surface--soft showcase-section">
          <div class="store-panel-header">
            <div>
              <div class="store-panel-title">精选推荐</div>
              <div class="store-panel-subtitle">编辑精选的高质量 AI 资源</div>
            </div>
            <router-link to="/products?is_featured=true" class="showcase-link">查看全部</router-link>
          </div>

          <div class="showcase-grid">
            <div v-for="product in featured" :key="product.id" class="showcase-grid__item">
              <ProductCard :product="product" />
            </div>
          </div>
        </section>

        <section class="store-surface store-surface--soft showcase-section">
          <div class="store-panel-header">
            <div>
              <div class="store-panel-title">最新上架</div>
              <div class="store-panel-subtitle">最近发布的资源与模板</div>
            </div>
            <router-link to="/products" class="showcase-link">浏览全部</router-link>
          </div>

          <div class="showcase-grid">
            <div v-for="product in products" :key="product.id" class="showcase-grid__item">
              <ProductCard :product="product" />
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import ProductCard from '../../components/ProductCard.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { getProducts } from '../../api/product'

const featured = ref([])
const products = ref([])

onMounted(async () => {
  try {
    const [featRes, allRes] = await Promise.all([
      getProducts({ is_featured: true, page_size: 4 }),
      getProducts({ page_size: 8 }),
    ])

    featured.value = featRes.data.results || []
    products.value = allRes.data.results || []
  } catch {
    // API not available
  }
})
</script>

<style scoped>
.showcase-stack {
  display: grid;
  gap: var(--sp-6);
}

.showcase-section {
  overflow: hidden;
}

.showcase-link {
  color: var(--accent);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.showcase-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--sp-5);
  padding: 0 var(--sp-6) var(--sp-6);
}

@media (max-width: 1200px) {
  .showcase-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .showcase-grid {
    grid-template-columns: 1fr;
  }
}
</style>
