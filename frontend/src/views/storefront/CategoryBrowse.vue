<template>
  <div class="store-page">
    <StorePageHeader eyebrow="Categories" icon="globe" title="分类浏览" subtitle="按资源方向快速进入适合当前任务的数字资产目录。" compact />

    <div class="store-page-body">
      <div class="container">
        <div v-if="loading" class="category-grid">
          <div v-for="i in 6" :key="i" class="skeleton-card">
            <div class="skeleton skeleton-icon" />
            <div class="skeleton skeleton-cat-name" />
            <div class="skeleton skeleton-cat-count" />
          </div>
        </div>

        <div v-else-if="categories.length" class="category-grid">
          <article
            v-for="(category, index) in categories"
            :key="category.id"
            class="store-surface store-surface--soft category-card"
            @click="$router.push(`/products?category=${category.id}`)"
          >
            <div class="category-card__icon" :style="{ background: iconColors[index % iconColors.length].bg, color: iconColors[index % iconColors.length].fg }">
              <AnimatedIcons :name="iconNames[index % iconNames.length]" :size="26" />
            </div>
            <h3>{{ category.name }}</h3>
            <p>{{ category.description || '查看该分类下的所有可用资源。' }}</p>
            <div class="category-card__footer">
              <span>{{ category.product_count || 0 }} 件商品</span>
              <AnimatedIcons name="arrow-right" :size="16" />
            </div>
          </article>
        </div>

        <div v-else class="empty-state store-surface store-surface--soft">
          <div class="empty-icon">
            <AnimatedIcons name="globe" :size="32" />
          </div>
          <h3>暂无分类</h3>
          <p>分类结构正在整理中，你也可以先从全部商品开始浏览。</p>
          <router-link to="/products" class="empty-action">浏览全部商品</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { gsap } from '../../composables/useGsap.js'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { getCategories } from '../../api/product'

const categories = ref([])
const loading = ref(false)

const iconNames = ['zap', 'layers', 'globe', 'image', 'shield', 'send', 'package', 'calendar']
const iconColors = [
  { bg: '#eef4ff', fg: '#305896' },
  { bg: '#f9f2e3', fg: '#8a6b2d' },
  { bg: '#eff8f2', fg: '#1f8f63' },
  { bg: '#f4efff', fg: '#6953c7' },
]

let ctx = null

onMounted(async () => {
  loading.value = true
  try {
    const res = await getCategories()
    categories.value = res.data.results || res.data || []
  } catch {
    categories.value = []
  } finally {
    loading.value = false
    nextTick(animateCards)
  }
})

onUnmounted(() => ctx?.revert())

watch(categories, () => nextTick(animateCards))

function animateCards() {
  ctx?.revert()
  const cards = document.querySelectorAll('.category-card')
  if (!cards.length) return
  ctx = gsap.context(() => {
    gsap.from(cards, {
      opacity: 0, y: 24, duration: 0.5, stagger: 0.06, ease: 'power3.out',
    })
  })
}
</script>

<style scoped>
.category-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-5);
}

.category-card {
  cursor: pointer;
  padding: var(--sp-7) var(--sp-6);
  transition: transform var(--dur-normal) var(--ease-spring), box-shadow var(--dur-normal);
}

.category-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--glass-shadow-hover);
}

.category-card__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 20px;
  margin-bottom: var(--sp-5);
}

.category-card h3 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
}

.category-card p {
  margin-top: var(--sp-3);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.8;
}

.category-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: var(--sp-5);
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.skeleton-card {
  display: grid;
  justify-items: start;
  gap: var(--sp-4);
  padding: var(--sp-7) var(--sp-6);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  background: var(--glass-bg);
}

.skeleton-icon {
  width: 72px;
  height: 72px;
  border-radius: 20px;
}

.skeleton-cat-name {
  width: 120px;
  height: 22px;
}

.skeleton-cat-count {
  width: 80px;
  height: 14px;
}

@media (max-width: 1200px) {
  .category-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .category-grid {
    grid-template-columns: 1fr;
  }
}
</style>
