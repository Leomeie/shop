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
                <button v-if="route.query.search || route.query.category || route.query.is_featured" class="result-chip" type="button" @click="clearFilters">
                  清空筛选
                </button>
              </div>
            </div>

            <div v-if="loading && !products.length" class="product-grid">
              <div v-for="i in 8" :key="i" class="skeleton-card">
                <div class="skeleton skeleton-img" />
                <div class="skeleton-body">
                  <div class="skeleton skeleton-cat" />
                  <div class="skeleton skeleton-title" />
                  <div class="skeleton skeleton-title short" />
                  <div class="skeleton-footer">
                    <div class="skeleton skeleton-price" />
                    <div class="skeleton skeleton-meta" />
                  </div>
                </div>
              </div>
            </div>

            <div v-else-if="products.length" class="product-grid">
              <div v-for="(product, index) in products" :key="product.id" class="grid-item" :style="{ '--i': index }">
                <ProductCard :product="product" />
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
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
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

watch(
  () => route.query,
  () => {
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
  opacity: 0;
  transform: translateY(24px);
  animation: fadeInUp 0.45s var(--ease-out) both;
  animation-delay: calc(var(--i, 0) * 70ms);
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
  margin-bottom: var(--sp-2);
}

.skeleton-title.short {
  width: 72%;
  margin-bottom: var(--sp-4);
}

.skeleton-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.skeleton-price {
  height: 20px;
  width: 60px;
}

.skeleton-meta {
  height: 14px;
  width: 44px;
}

.pagination {
  display: flex;
  justify-content: center;
  padding-top: var(--sp-6);
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
