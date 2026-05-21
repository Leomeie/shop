<template>
  <div class="editor-page">
    <section class="editor-topbar store-surface">
      <div class="editor-topbar__left">
        <router-link to="/admin/products" class="editor-back">返回商品列表</router-link>
        <div>
          <div class="editor-kicker">Product Editor</div>
          <h2 class="editor-title">{{ isNew ? '新建商品' : form.name || '编辑商品' }}</h2>
        </div>
      </div>

      <div class="editor-topbar__right">
        <StatusBadge v-if="!isNew" :label="statusLabel" :status="form.status || 'draft'" size="sm" />
        <button class="ghost-btn" type="button" @click="saveDraft" :disabled="saving">保存草稿</button>
        <button class="primary-btn" type="button" @click="saveAndPublish" :disabled="saving">
          {{ saving ? '保存中...' : '保存并发布' }}
        </button>
      </div>
    </section>

    <div class="editor-layout">
      <aside class="editor-sidebar store-surface">
        <div class="store-panel-title">编辑章节</div>
        <div class="store-panel-subtitle">按照从上到下的顺序补全商品信息</div>
        <nav class="editor-nav">
          <button
            v-for="section in sections"
            :key="section.id"
            :class="['editor-nav__item', { 'is-active': activeSection === section.id }]"
            type="button"
            @click="scrollToSection(section.id)"
          >
            <span>{{ section.label }}</span>
          </button>
        </nav>
      </aside>

      <div class="editor-content">
        <section :id="sections[0].id" class="editor-section store-surface">
          <div class="store-panel-header">
            <div>
              <div class="store-panel-title">基础信息</div>
              <div class="store-panel-subtitle">商品标题、分类、状态和推荐设置</div>
            </div>
          </div>

          <div class="form-grid">
            <div class="field field-span-2">
              <label>商品名称</label>
              <input v-model="form.name" type="text" placeholder="例如：Prompt Bundle Pro" />
            </div>
            <div class="field">
              <label>分类</label>
              <select v-model="form.category">
                <option value="">未分类</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
              </select>
            </div>
            <div class="field">
              <label>状态</label>
              <select v-model="form.status">
                <option value="draft">草稿</option>
                <option value="active">上架</option>
                <option value="inactive">下架</option>
              </select>
            </div>
            <div class="field field-span-2">
              <label class="inline-toggle">
                <input v-model="form.is_featured" type="checkbox" />
                <span>加入精选推荐</span>
              </label>
            </div>
          </div>
        </section>

        <section :id="sections[1].id" class="editor-section store-surface">
          <div class="store-panel-header">
            <div>
              <div class="store-panel-title">资源内容</div>
              <div class="store-panel-subtitle">版本、描述和更新日志</div>
            </div>
          </div>

          <div class="form-grid">
            <div class="field">
              <label>版本号</label>
              <input v-model="form.version" type="text" placeholder="例如：1.0.0" />
            </div>
            <div class="field field-span-2">
              <label>商品描述</label>
              <textarea v-model="form.description" rows="6" placeholder="描述资源用途、适合场景和交付内容。" />
            </div>
            <div class="field field-span-2">
              <label>更新日志</label>
              <textarea v-model="form.changelog" rows="4" placeholder="记录版本变更内容。" />
            </div>
          </div>
        </section>

        <section :id="sections[2].id" class="editor-section store-surface">
          <div class="store-panel-header">
            <div>
              <div class="store-panel-title">主资源与预览</div>
              <div class="store-panel-subtitle">管理主图、交付文件和 Demo 文件</div>
            </div>
          </div>

          <div class="asset-grid">
            <div class="asset-card">
              <div class="asset-card__title">主图</div>
              <div class="asset-preview">
                <img v-if="preview.main_image || form.main_image_url" :src="preview.main_image || form.main_image_url" alt="主图预览" />
                <span v-else>暂无主图</span>
              </div>
              <input type="file" accept="image/*" @change="handleFileChange($event, 'main_image')" />
            </div>

            <div class="asset-card">
              <div class="asset-card__title">商品文件</div>
              <div class="asset-file">{{ selectedFileName('file', form.file_url, '尚未选择商品文件') }}</div>
              <input type="file" @change="handleFileChange($event, 'file')" />
            </div>

            <div class="asset-card">
              <div class="asset-card__title">Demo 文件</div>
              <div class="asset-file">{{ selectedFileName('demo_file', form.demo_file_url, '尚未选择 Demo 文件') }}</div>
              <input type="file" @change="handleFileChange($event, 'demo_file')" />
            </div>
          </div>

          <div class="sub-block">
            <div class="sub-block__header">
              <div class="store-panel-title">预览图集</div>
              <div class="store-panel-subtitle">最多可维护多张详情预览图</div>
            </div>

            <div v-if="images.length" class="gallery-list">
              <article v-for="image in images" :key="image.id" class="gallery-row">
                <img :src="image.image" alt="预览图" />
                <span>排序 {{ image.sort_order }}</span>
                <button class="table-link danger" type="button" @click="removeImage(image.id)">删除</button>
              </article>
            </div>

            <div v-else class="empty-inline">暂无额外预览图</div>

            <div class="gallery-upload">
              <input type="file" accept="image/*" @change="handleExtraImageChange" />
              <input v-model.number="newImageSort" type="number" min="0" placeholder="排序值" />
              <button class="ghost-btn" type="button" @click="uploadImage" :disabled="!pendingImageFile || !productId">上传预览图</button>
            </div>
          </div>
        </section>

        <section :id="sections[3].id" class="editor-section store-surface">
          <div class="store-panel-header">
            <div>
              <div class="store-panel-title">价格与 SKU</div>
              <div class="store-panel-subtitle">不同授权版本、价格和启用状态</div>
            </div>
          </div>

          <div class="sku-stack">
            <article v-for="sku in skus" :key="sku.localId" class="sku-card">
              <div class="sku-grid">
                <div class="field">
                  <label>版本名称</label>
                  <input v-model="sku.name" type="text" />
                </div>
                <div class="field">
                  <label>售价（元）</label>
                  <input v-model.number="sku.price_yuan" type="number" min="0" step="0.01" />
                </div>
                <div class="field">
                  <label>原价（元）</label>
                  <input v-model.number="sku.original_price_yuan" type="number" min="0" step="0.01" />
                </div>
                <div class="field">
                  <label>排序</label>
                  <input v-model.number="sku.sort_order" type="number" min="0" />
                </div>
                <div class="field field-span-2">
                  <label>授权说明</label>
                  <input v-model="sku.license_description" type="text" placeholder="例如：商业授权 / 个人授权" />
                </div>
                <div class="field">
                  <label class="inline-toggle">
                    <input v-model="sku.is_active" type="checkbox" />
                    <span>启用该版本</span>
                  </label>
                </div>
              </div>

              <div class="sku-actions">
                <button class="ghost-btn" type="button" @click="saveSku(sku)" :disabled="!productId">保存 SKU</button>
                <button class="ghost-btn danger" type="button" @click="deleteSkuRow(sku)">删除 SKU</button>
              </div>
            </article>
          </div>

          <button class="ghost-btn" type="button" @click="addSkuRow">新增一个 SKU</button>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  createAdminProduct,
  createAdminProductImage,
  createAdminSku,
  deleteAdminProductImage,
  deleteAdminSku,
  getAdminCategories,
  getAdminProduct,
  updateAdminProduct,
  updateAdminSku,
} from '../../api/adminProduct'
import StatusBadge from '../../components/StatusBadge.vue'

const route = useRoute()
const router = useRouter()

const isNew = computed(() => route.name === 'AdminProductNew')
const productId = computed(() => (!isNew.value ? route.params.id : ''))
const statusLabel = computed(() => (form.status === 'active' ? '上架' : form.status === 'inactive' ? '下架' : '草稿'))

const sections = [
  { id: 'basic', label: '基础信息' },
  { id: 'content', label: '资源内容' },
  { id: 'assets', label: '主资源与预览' },
  { id: 'pricing', label: '价格与 SKU' },
]

const activeSection = ref('basic')
const saving = ref(false)
const categories = ref([])
const images = ref([])
const skus = ref([])
const pendingImageFile = ref(null)
const newImageSort = ref(0)
const sectionObserver = ref(null)

const form = reactive({
  name: '',
  category: '',
  description: '',
  version: '1.0.0',
  changelog: '',
  status: 'draft',
  is_featured: false,
  main_image: null,
  file: null,
  demo_file: null,
  main_image_url: '',
  file_url: '',
  demo_file_url: '',
})

const preview = reactive({
  main_image: '',
})

function createSkuDraft(sku = {}) {
  const draftId = globalThis.crypto?.randomUUID?.() || `${Date.now()}-${Math.random().toString(16).slice(2)}`
  return {
    localId: sku.id || `new-${draftId}`,
    id: sku.id || null,
    name: sku.name || '',
    price_yuan: sku.price_yuan || 0,
    original_price_yuan: sku.original_price_yuan || 0,
    license_description: sku.license_description || '',
    sort_order: sku.sort_order || 0,
    is_active: sku.is_active ?? true,
  }
}

async function loadCategories() {
  const res = await getAdminCategories()
  categories.value = res.data || []
}

async function loadProduct() {
  if (!productId.value) return
  const res = await getAdminProduct(productId.value)
  const data = res.data
  form.name = data.name || ''
  form.category = data.category || ''
  form.description = data.description || ''
  form.version = data.version || '1.0.0'
  form.changelog = data.changelog || ''
  form.status = data.status || 'draft'
  form.is_featured = Boolean(data.is_featured)
  form.main_image_url = data.main_image || ''
  form.file_url = data.file || ''
  form.demo_file_url = data.demo_file || ''
  preview.main_image = ''
  images.value = data.images || []
  skus.value = (data.skus_data || []).map(createSkuDraft)
}

function selectedFileName(key, currentUrl, fallback) {
  if (form[key] instanceof File) return form[key].name
  if (currentUrl) return currentUrl.split('/').pop()
  return fallback
}

function handleFileChange(event, key) {
  const file = event.target.files?.[0]
  if (!file) return
  form[key] = file
  if (key === 'main_image') {
    preview.main_image = URL.createObjectURL(file)
  }
}

function handleExtraImageChange(event) {
  pendingImageFile.value = event.target.files?.[0] || null
}

async function uploadImage() {
  if (!productId.value || !pendingImageFile.value) return
  const data = new FormData()
  data.append('image', pendingImageFile.value)
  data.append('sort_order', String(newImageSort.value || 0))
  await createAdminProductImage(productId.value, data)
  pendingImageFile.value = null
  newImageSort.value = 0
  ElMessage.success('预览图已上传')
  await loadProduct()
}

async function removeImage(imageId) {
  if (!productId.value) return
  await deleteAdminProductImage(productId.value, imageId)
  ElMessage.success('预览图已删除')
  await loadProduct()
}

function addSkuRow() {
  skus.value.push(createSkuDraft())
}

async function saveSku(sku) {
  if (!productId.value) {
    ElMessage.warning('请先保存商品，再配置 SKU')
    return
  }

  const payload = {
    name: sku.name,
    price: Math.round(Number(sku.price_yuan || 0) * 100),
    original_price: Math.round(Number(sku.original_price_yuan || 0) * 100),
    license_description: sku.license_description,
    sort_order: sku.sort_order || 0,
    is_active: sku.is_active,
  }

  if (sku.id) await updateAdminSku(productId.value, sku.id, payload)
  else await createAdminSku(productId.value, payload)

  ElMessage.success('SKU 已保存')
  await loadProduct()
}

async function deleteSkuRow(sku) {
  if (!sku.id) {
    skus.value = skus.value.filter((item) => item.localId !== sku.localId)
    return
  }

  await ElMessageBox.confirm(`确定删除 SKU「${sku.name}」吗？`, '删除 SKU')
  await deleteAdminSku(productId.value, sku.id)
  ElMessage.success('SKU 已删除')
  await loadProduct()
}

function buildProductPayload(statusOverride) {
  const payload = new FormData()
  payload.append('name', form.name)
  if (form.category) payload.append('category', String(form.category))
  payload.append('description', form.description || '')
  payload.append('version', form.version || '1.0.0')
  payload.append('changelog', form.changelog || '')
  payload.append('status', statusOverride || form.status || 'draft')
  payload.append('is_featured', String(Boolean(form.is_featured)))
  if (form.main_image instanceof File) payload.append('main_image', form.main_image)
  if (form.file instanceof File) payload.append('file', form.file)
  if (form.demo_file instanceof File) payload.append('demo_file', form.demo_file)
  return payload
}

function validateEditor() {
  if (!form.name.trim()) {
    ElMessage.error('商品名称不能为空')
    scrollToSection('basic')
    return false
  }
  if (isNew.value && !(form.main_image instanceof File)) {
    ElMessage.error('新建商品时必须上传主图')
    scrollToSection('assets')
    return false
  }
  if (isNew.value && !(form.file instanceof File)) {
    ElMessage.error('新建商品时必须上传商品文件')
    scrollToSection('assets')
    return false
  }
  return true
}

async function persistProduct(statusOverride) {
  if (!validateEditor()) return null
  saving.value = true
  try {
    const payload = buildProductPayload(statusOverride)
    const res = isNew.value ? await createAdminProduct(payload) : await updateAdminProduct(productId.value, payload)
    const id = res.data.id
    ElMessage.success(isNew.value ? '商品已创建' : '商品已保存')
    if (isNew.value) {
      await router.replace(`/admin/products/${id}/edit`)
    } else {
      await loadProduct()
    }
    return id
  } finally {
    saving.value = false
  }
}

async function saveDraft() {
  await persistProduct('draft')
}

async function saveAndPublish() {
  await persistProduct('active')
}

function scrollToSection(sectionId) {
  activeSection.value = sectionId
  document.getElementById(sectionId)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function setupSectionObserver() {
  sectionObserver.value = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0]
      if (visible?.target?.id) activeSection.value = visible.target.id
    },
    { rootMargin: '-20% 0px -55% 0px', threshold: [0.2, 0.5, 0.8] },
  )

  sections.forEach((section) => {
    const el = document.getElementById(section.id)
    if (el) sectionObserver.value.observe(el)
  })
}

onMounted(async () => {
  await loadCategories()
  await loadProduct()
  if (!skus.value.length) addSkuRow()
  setupSectionObserver()
})

onUnmounted(() => {
  sectionObserver.value?.disconnect()
  if (preview.main_image) URL.revokeObjectURL(preview.main_image)
})
</script>

<style scoped>
.editor-page {
  display: grid;
  gap: var(--sp-5);
}

.editor-topbar {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--sp-4);
  padding: var(--sp-5);
}

.editor-topbar__left,
.editor-topbar__right {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  flex-wrap: wrap;
}

.editor-back {
  color: var(--accent);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.editor-kicker {
  color: var(--text-muted);
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.editor-title {
  margin-top: 6px;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 2vw, 2.2rem);
  font-weight: 800;
  letter-spacing: -0.03em;
}

.editor-layout {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  gap: var(--sp-5);
  align-items: start;
}

.editor-sidebar {
  position: sticky;
  top: var(--sp-5);
  padding: var(--sp-5);
}

.editor-nav {
  display: grid;
  gap: var(--sp-2);
  margin-top: var(--sp-4);
}

.editor-nav__item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--sp-3) var(--sp-4);
  border: 1px solid transparent;
  border-radius: 14px;
  background: transparent;
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
  text-align: left;
}

.editor-nav__item.is-active {
  border-color: rgba(198, 168, 106, 0.3);
  background: rgba(198, 168, 106, 0.12);
  color: var(--text-primary);
}

.editor-content {
  display: grid;
  gap: var(--sp-5);
}

.editor-section {
  overflow: hidden;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: var(--sp-4);
  padding: 0 var(--sp-6) var(--sp-6);
}

.field,
.sub-block,
.asset-card {
  display: grid;
  gap: var(--sp-3);
}

.field-span-2 {
  grid-column: span 2;
}

.field label,
.asset-card__title {
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.field input,
.field select,
.field textarea,
.gallery-upload input {
  width: 100%;
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.74);
  padding: 0 var(--sp-4);
  color: var(--text-primary);
  font-size: var(--text-sm);
}

.field input,
.field select {
  height: 44px;
}

.field textarea {
  padding-top: var(--sp-3);
  padding-bottom: var(--sp-3);
  resize: vertical;
}

.field input:focus,
.field select:focus,
.field textarea:focus,
.gallery-upload input:focus {
  outline: none;
  border-color: rgba(198, 168, 106, 0.4);
  box-shadow: 0 0 0 4px rgba(198, 168, 106, 0.12);
}

.inline-toggle {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
}

.asset-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-4);
  padding: 0 var(--sp-6) var(--sp-6);
}

.asset-card {
  padding: var(--sp-4);
  border: 1px solid var(--glass-border);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.68);
}

.asset-preview {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 4 / 3;
  border-radius: 16px;
  background: var(--glass-border);
  overflow: hidden;
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.asset-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.asset-file {
  min-height: 44px;
  padding: var(--sp-3) var(--sp-4);
  border-radius: 12px;
  background: var(--glass-border);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.7;
}

.sub-block {
  padding: 0 var(--sp-6) var(--sp-6);
}

.sub-block__header {
  display: grid;
  gap: var(--sp-1);
  margin-bottom: var(--sp-4);
}

.gallery-list,
.sku-stack {
  display: grid;
  gap: var(--sp-3);
}

.gallery-row,
.sku-card {
  display: grid;
  gap: var(--sp-3);
  padding: var(--sp-4);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.68);
}

.gallery-row {
  grid-template-columns: 88px 1fr auto;
  align-items: center;
}

.gallery-row img {
  width: 88px;
  height: 88px;
  border-radius: 14px;
  object-fit: cover;
}

.gallery-upload {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 120px auto;
  gap: var(--sp-3);
}

.sku-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--sp-4);
}

.sku-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--sp-3);
}

.primary-btn,
.ghost-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 42px;
  padding: 0 var(--sp-5);
  border-radius: 12px;
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.primary-btn {
  border: none;
  background: var(--text-primary);
  color: var(--white);
}

.ghost-btn {
  border: 1px solid var(--glass-border);
  background: var(--glass-bg);
  color: var(--text-secondary);
}

.ghost-btn.danger {
  color: var(--error);
}

.empty-inline {
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.table-link {
  border: none;
  background: none;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.table-link.danger {
  color: var(--error);
}

@media (max-width: 1200px) {
  .editor-layout {
    grid-template-columns: 1fr;
  }

  .editor-sidebar {
    position: static;
  }

  .asset-grid,
  .sku-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }

  .field-span-2 {
    grid-column: span 1;
  }

  .gallery-row,
  .gallery-upload {
    grid-template-columns: 1fr;
  }
}
</style>
