<template>
  <div class="store-page">
    <StorePageHeader
      eyebrow="Catalog"
      icon="layers"
      :title="route.query.search ? `“${route.query.search}” 的搜索结果` : '全部商品'"
      :subtitle="`面向创作者的数字资源目录，共 ${total} 件商品。`"
      badge="Operator Luxe"
      compact
    >
      <template #meta>
        <span v-if="route.query.category" class="result-chip is-active">当前分类</span>
        <span v-if="route.query.is_featured" class="result-chip is-active">精选资源</span>
      </template>
    </StorePageHeader>

    <div class="store-page-body">
      <div class="container">
        <div class="catalog-shell">
          <aside class="facet-sidebar store-surface store-surface--soft">
            <div class="facet-sidebar__header">
              <div>
                <div class="facet-sidebar__title">筛选条件</div>
                <div class="store-panel-subtitle">快速缩小结果范围</div>
              </div>
              <button class="clear-link" type="button" @click="clearFilters">清空</button>
            </div>

            <div class="facet-groups">
              <section class="facet-group">
                <div class="facet-group__label">浏览范围</div>
                <div class="facet-options">
                  <button :class="['facet-option', { 'is-active': !route.query.category }]" type="button" @click="applyCategory('')">
                    全部分类
                  </button>
                  <button
                    v-for="category in categories"
                    :key="category.id"
                    :class="['facet-option', { 'is-active': String(route.query.category || '') === String(category.id) }]"
                    type="button"
                    @click="applyCategory(category.id)"
                  >
                    <span>{{ category.name }}</span>
                    <span class="facet-count">{{ category.product_count || 0 }}</span>
                  </button>
                </div>
              </section>

              <section class="facet-group">
                <div class="facet-group__label">资源标签</div>
                <div class="facet-options">
                  <button :class="['facet-option', { 'is-active': route.query.is_featured }]" type="button" @click="toggleFeatured">
                    精选推荐
                  </button>
                  <button class="facet-option" type="button" disabled>
                    持续更新
                  </button>
                  <button class="facet-option" type="button" disabled>
                    商业授权
                  </button>
                </div>
              </section>
            </div>
          </aside>

          <div class="catalog-results">
            <div class="results-toolbar store-surface">
              <div class="results-toolbar__left">
                <div class="results-summary">
                  找到 <span class="results-count-strong">{{ total }}</span> 件资源
                </div>
                <div class="results-actions">
                  <button
                    v-for="sort in sortOptions"
                    :key="sort.value"
                    :class="['result-chip', { 'is-active': ordering === sort.value }]"
                    type="button"
                    @click="setOrdering(sort.value)"
                  >
                    {{ sort.label }}
                  </button>
                </div>
              </div>

              <div class="results-toolbar__right">
                <div class="search-input-wrap">
                  <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                  <input
                    v-model="searchInput"
                    type="text"
                    class="search-input"
                    placeholder="搜索商品…"
                    @input="onSearchInput"
                  />
                  <button v-if="searchInput" class="search-clear" type="button" @click="clearSearch">×</button>
                </div>
                <button v-if="route.query.search || route.query.category || route.query.is_featured" class="result-chip" type="button" @click="clearFilters">
                  清空筛选
                </button>
              </div>
            </div>

            <div v-if="loading && !products.length" class="product-grid">
              <div v-for="i in 8" :key="i" class="skeleton-card">
                <el-skeleton :animated="true">
                  <template #template>
                    <el-skeleton-item variant="image" class="skeleton-img" />
                    <div style="padding: var(--sp-4) var(--sp-5) var(--sp-5)">
                      <el-skeleton-item variant="text" style="width: 60px; height: 12px; margin-bottom: var(--sp-3)" />
                      <el-skeleton-item variant="text" style="width: 100%; height: 16px; margin-bottom: var(--sp-2)" />
                      <el-skeleton-item variant="text" style="width: 72%; height: 16px; margin-bottom: var(--sp-4)" />
                      <div style="display: flex; justify-content: space-between; align-items: center">
                        <el-skeleton-item variant="text" style="width: 60px; height: 20px" />
                        <el-skeleton-item variant="text" style="width: 44px; height: 14px" />
                      </div>
                    </div>
                  </template>
                </el-skeleton>
              </div>
            </div>

            <div v-else-if="products.length" class="product-grid">
              <div v-for="(product, index) in products" :key="product.id" class="grid-item" :style="{ '--i': index }">
                <ProductCard :product="product" :keyword="route.query.search" />
              </div>
            </div>

            <div v-else class="empty-state store-surface store-surface--soft">
              <div class="empty-icon">
                <AnimatedIcons name="search" :size="32" />
              </div>
              <h3>没有找到匹配结果</h3>
              <p>可以尝试切换分类、清空筛选，或返回查看所有商品。</p>
              <router-link to="/products" class="empty-action">浏览全部商品</router-link>
            </div>

            <div class="pagination" v-if="total > pageSize">
              <el-pagination
                background
                layout="prev, pager, next"
                :total="total"
                :page-size="pageSize"
                v-model:current-page="page"
                @current-change="fetchData"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { gsap } from '../../composables/useGsap.js'
import { getCategories, getProducts } from '../../api/product'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import ProductCard from '../../components/ProductCard.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'

const route = useRoute()
const router = useRouter()

const products = ref([])
const categories = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = 20
const ordering = ref('-created_at')
const searchInput = ref(route.query.search || '')
let searchTimer = null

const sortOptions = [
  { label: '最新上架', value: '-created_at' },
  { label: '价格升序', value: 'price' },
  { label: '价格降序', value: '-price' },
  { label: '下载热度', value: '-download_count' },
]

const resolvedQuery = computed(() => ({
  search: route.query.search || '',
  category: route.query.category || '',
  is_featured: route.query.is_featured || '',
}))

function updateQuery(nextQuery) {
  router.push({
    path: '/products',
    query: {
      ...route.query,
      ...nextQuery,
    },
  })
}

function applyCategory(categoryId) {
  updateQuery({ category: categoryId || undefined })
}

function toggleFeatured() {
  updateQuery({ is_featured: route.query.is_featured ? undefined : true })
}

function clearFilters() {
  router.push({ path: '/products', query: resolvedQuery.value.search ? { search: resolvedQuery.value.search } : {} })
}

function setOrdering(value) {
  ordering.value = value
  page.value = 1
  fetchData()
}

function onSearchInput() {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    updateQuery({ search: searchInput.value || undefined })
  }, 300)
}

function clearSearch() {
  searchInput.value = ''
  updateQuery({ search: undefined })
}

async function fetchData() {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize,
      ordering: ordering.value,
    }

    if (resolvedQuery.value.search) params.search = resolvedQuery.value.search
    if (resolvedQuery.value.category) params.category = resolvedQuery.value.category
    if (resolvedQuery.value.is_featured) params.is_featured = resolvedQuery.value.is_featured

    const res = await getProducts(params)
    products.value = res.data.results || []
    total.value = res.data.count || 0
  } finally {
    loading.value = false
  }
}

async function fetchCategoriesData() {
  try {
    const res = await getCategories()
    categories.value = res.data.results || res.data || []
  } catch {
    categories.value = []
  }
}

onMounted(async () => {
  try {
    await Promise.all([fetchCategoriesData(), fetchData()])
  } catch {
    // errors already handled inside each function
  }
})

let gridCtx = null

function animateGrid() {
  gridCtx?.revert()
  const grid = document.querySelector('.product-grid')
  if (!grid) return
  const items = grid.querySelectorAll('.grid-item')
  if (!items.length) return
  gridCtx = gsap.context(() => {
    gsap.from(items, {
      opacity: 0, y: 24, duration: 0.45, ease: 'power3.out',
      stagger: 0.06, clearProps: 'all',
    })
  }, grid)
}

watch(() => products.value, () => {
  nextTick(animateGrid)
}, { flush: 'post' })

onUnmounted(() => {
  clearTimeout(searchTimer)
  gridCtx?.revert()
})

watch(
  () => route.query,
  (q) => {
    searchInput.value = q.search || ''
    page.value = 1
    fetchData()
  },
)
</script>

<style scoped>
.clear-link {
  border: none;
  background: none;
  color: var(--accent);
  font-family: var(--font-display);
  font-size: var(--text-xs);
  font-weight: 600;
}

.facet-count {
  margin-left: auto;
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-5);
}

.grid-item {
  /* GSAP handles entrance animation */
}

.skeleton-card {
  overflow: hidden;
  border: 1px solid var(--glass-border);
  border-radius: var(--r-lg);
  background: var(--glass-bg);
}

.skeleton-img {
  aspect-ratio: 4 / 3;
  width: 100%;
}

.pagination {
  display: flex;
  justify-content: center;
  padding-top: var(--sp-6);
}

.search-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 10px;
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  width: 200px;
  padding: 6px 30px 6px 32px;
  border: 1px solid var(--glass-border);
  border-radius: var(--r-full);
  background: var(--glass-bg);
  color: var(--text-primary);
  font-size: var(--text-xs);
  font-family: var(--font-body);
  outline: none;
  transition: border-color var(--dur-fast), width var(--dur-normal);
}

.search-input:focus {
  border-color: var(--accent);
  width: 260px;
}

.search-input::placeholder {
  color: var(--text-muted);
}

.search-clear {
  position: absolute;
  right: 6px;
  border: none;
  background: none;
  color: var(--text-muted);
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  padding: 2px 4px;
}

.search-clear:hover {
  color: var(--text-primary);
}

.results-toolbar__right {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
}

@media (max-width: 1200px) {
  .product-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 768px) {
  .product-grid {
    grid-template-columns: 1fr;
  }
}
</style>
