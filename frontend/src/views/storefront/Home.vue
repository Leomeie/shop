<template>
  <div class="home">
    <div class="home-scroll-wrapper">
    <section ref="videoSectionRef" class="screen screen-video" id="home-video">
      <ParticleCanvas />

      <div class="video-cta-wrap">
        <div class="video-auth">
          <template v-if="userStore.isLoggedIn">
            <router-link to="/products" class="auth-btn auth-btn-secondary">浏览商品</router-link>
            <router-link to="/downloads" class="auth-btn auth-btn-primary">我的下载</router-link>
          </template>
          <template v-else>
            <router-link to="/login" class="auth-btn auth-btn-secondary">登录</router-link>
            <router-link to="/register" class="auth-btn auth-btn-primary">免费注册</router-link>
          </template>
        </div>
      </div>

      <button class="scroll-hint" type="button" @click="scrollToScene(1)">
        <div class="scroll-mouse">
          <div class="scroll-dot" />
        </div>
        <span>继续浏览</span>
      </button>
    </section>

    <section ref="heroSectionRef" class="screen screen-hero" id="home-hero">
      <div class="hero-bg">
        <div class="hero-orb orb-1" />
        <div class="hero-orb orb-2" />
        <div class="hero-orb orb-3" />
        <div class="hero-grid" />
      </div>

      <div class="container hero-content">
        <div class="hero-badge">
          <span class="badge-dot" />
          AI 创作者的数字精品店
        </div>

        <h1 class="hero-title">
          <GradientText variant="blue">发现最好的</GradientText>
          <br />
          <span class="title-line">AI 工具与模板</span>
        </h1>

        <p class="hero-desc">
          精选 Prompt 模板、ComfyUI 工作流、LoRA 模型与设计素材，
          <br />
          让创作效率、交付质量与灵感探索落在同一条路径里。
        </p>

        <div class="hero-actions">
          <router-link to="/products" class="btn btn-gradient">
            浏览全部商品
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12" />
              <polyline points="12 5 19 12 12 19" />
            </svg>
          </router-link>
          <router-link to="/products?is_featured=true" class="btn btn-glass">精选推荐</router-link>
        </div>
      </div>

        <div class="hero-particles">
          <ParticleBackground />
        </div>
    </section>

    <section ref="systemSectionRef" class="screen screen-system" id="home-system">
      <div class="container system-shell">
        <div class="system-head">
          <div class="system-copy">
            <span class="section-kicker">Delivery System</span>
            <h2 class="section-title">
              <GradientText variant="purple">为创作者设计的交付系统</GradientText>
            </h2>
            <p class="section-desc">
              首页不再只是展示，而是一条完整的决策路径。
              用户从看到资源、理解价值、完成购买，到拿到资产，都能在几步内完成。
            </p>
          </div>

          <div class="system-board">
            <div class="system-board__header">
              <span class="system-board__eyebrow">Operator Flow</span>
              <p>把发现、判断与交付压缩进一条更顺的路径里。</p>
            </div>

            <div class="system-steps">
              <article v-for="step in workflowSteps" :key="step.id" class="step-card">
                <div class="step-index">{{ step.id }}</div>
                <div class="step-copy">
                  <h3><GradientText variant="blue">{{ step.title }}</GradientText></h3>
                  <p>{{ step.desc }}</p>
                </div>
              </article>
            </div>
          </div>
        </div>

        <div class="system-metrics">
          <div class="metric-card glass-card">
            <strong><GradientText variant="blue">即时下载</GradientText></strong>
            <span>支付后立刻可用，不把时间耗在等待上。</span>
          </div>
          <div class="metric-card glass-card">
            <strong><GradientText variant="purple">结构清晰</GradientText></strong>
            <span>资源按工作流和用途组织，减少来回跳转。</span>
          </div>
          <div class="metric-card glass-card">
            <strong><GradientText variant="pink">持续维护</GradientText></strong>
            <span>版本迭代与资源更新可长期获取。</span>
          </div>
        </div>
      </div>
    </section>

    <section ref="showcaseSectionRef" class="screen screen-showcase" id="home-showcase">
      <div class="showcase-bg">
        <div class="showcase-glow glow-left" />
        <div class="showcase-glow glow-right" />
        <div class="showcase-grid" />
      </div>

      <div class="container showcase-shell">
        <div class="showcase-header">
          <div>
            <span class="section-kicker section-kicker-on-dark">Curated Picks</span>
            <h2 class="section-title section-title-on-dark">
              <GradientText variant="purple">直接进入高价值资源</GradientText>
            </h2>
            <p class="section-desc section-desc-on-dark">
              我把第四屏设计成入口矩阵，而不是空白结束页。你可以直接从这里进入热门资源、模板方向和工作流分类。
            </p>
          </div>

          <router-link to="/products" class="btn btn-gradient">
            进入商品库
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12" />
              <polyline points="12 5 19 12 12 19" />
            </svg>
          </router-link>
        </div>

        <div class="showcase-grid-cards">
          <router-link
            v-for="item in showcaseItems"
            :key="item.id"
            :to="item.to"
            class="showcase-card glass-card"
          >
            <div class="showcase-card-media" :style="item.cover ? { backgroundImage: `url(${item.cover})` } : undefined" />
            <div class="showcase-card-body">
              <span class="showcase-card-label">{{ item.label }}</span>
              <h3><GradientText variant="blue">{{ item.title }}</GradientText></h3>
              <p>{{ item.desc }}</p>
              <div class="showcase-card-meta">
                <span>{{ item.meta }}</span>
                <span class="showcase-card-arrow">→</span>
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <div class="hero-controls" :class="{ 'is-hidden': activeStage === 0 }">
      <div class="snap-dots">
        <button
          v-for="(label, index) in sceneLabels"
          :key="label"
          :class="['dot', { active: activeStage === index }]"
          type="button"
          :aria-label="label"
          @click="scrollToScene(index)"
        >
          <span class="dot-inner" />
        </button>
      </div>

      <div class="snap-counter">
        <span class="counter-current">{{ String(activeStage + 1).padStart(2, '0') }}</span>
        <span class="counter-sep">/</span>
        <span class="counter-total">{{ String(sceneLabels.length).padStart(2, '0') }}</span>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { getProducts } from '../../api/product'
import { useAppStore } from '../../stores/app'
import { useUserStore } from '../../stores/user'
import GradientText from '../../components/GradientText.vue'
import ParticleBackground from '../../components/ParticleBackground.vue'
import ParticleCanvas from '../../components/ParticleCanvas.vue'

const appStore = useAppStore()
const userStore = useUserStore()

const sceneLabels = ['视频首屏', '品牌 Hero', '交付系统', '精选资源']
const activeStage = ref(0)
const featured = ref([])
const videoSectionRef = ref(null)
const heroSectionRef = ref(null)
const systemSectionRef = ref(null)
const showcaseSectionRef = ref(null)

const workflowSteps = [
  {
    id: '01',
    title: '快速发现',
    desc: '在品牌 Hero 和精选入口里先建立判断，再决定看哪类资源，不再被杂乱的信息面板分散注意力。',
  },
  {
    id: '02',
    title: '低成本决策',
    desc: '每个资源都带着明确的用途、工作流方向和交付价值，让用户不用猜它能解决什么问题。',
  },
  {
    id: '03',
    title: '完成交付',
    desc: '从购买到下载形成闭环，减少跳转、减少等待、减少“买了却不会用”的断层。',
  },
]

const fallbackShowcase = [
  {
    id: 'prompt-bundle',
    label: 'Prompt Bundle',
    title: '高转化 Prompt 模板',
    desc: '适合营销文案、图像生成和角色设定的成套模板，开箱即用。',
    meta: '模板集合',
    to: '/products?search=prompt',
    cover: '',
  },
  {
    id: 'comfyui-workflow',
    label: 'Workflow',
    title: 'ComfyUI 工作流',
    desc: '把常用节点链路整理成可重复使用的工作流，降低试错成本。',
    meta: '工作流方向',
    to: '/products?search=workflow',
    cover: '',
  },
  {
    id: 'lora-models',
    label: 'LoRA Models',
    title: '风格 LoRA 模型',
    desc: '针对角色、材质、海报和品牌风格整理的训练模型合集。',
    meta: '模型资源',
    to: '/products?search=LoRA',
    cover: '',
  },
  {
    id: 'design-assets',
    label: 'Design Assets',
    title: '设计交付素材包',
    desc: '围绕封面、海报、社媒图和演示文稿场景准备的交付级素材。',
    meta: '素材方向',
    to: '/products?search=设计',
    cover: '',
  },
]

const showcaseItems = computed(() => {
  if (!featured.value.length) return fallbackShowcase

  return featured.value.slice(0, 4).map((item, index) => ({
    id: `product-${item.id}`,
    label: item.category_name || `精选资源 ${index + 1}`,
    title: item.name,
    desc: item.description || '可直接购买并下载使用的精选资源，适合纳入实际创作工作流。',
    meta: item.min_price_yuan ? `¥${item.min_price_yuan}` : `${item.download_count || 0} 次下载`,
    to: `/products/${item.id}`,
    cover: item.main_image || '',
  }))
})

let scrollRafId = 0
let resizeRafId = 0

function setActiveStage(nextStage) {
  if (activeStage.value === nextStage) return
  activeStage.value = nextStage
}

function getSceneElements() {
  return [
    videoSectionRef.value,
    heroSectionRef.value,
    systemSectionRef.value,
    showcaseSectionRef.value,
  ].filter(Boolean)
}

function updateActiveStage() {
  const viewportCenter = (window.innerHeight || 1) / 2
  const scenes = getSceneElements()

  let nextStage = 0
  let closestDistance = Number.POSITIVE_INFINITY

  scenes.forEach((scene, index) => {
    const rect = scene.getBoundingClientRect()
    const sceneCenter = rect.top + rect.height / 2
    const distance = Math.abs(sceneCenter - viewportCenter)

    if (distance < closestDistance) {
      closestDistance = distance
      nextStage = index
    }
  })

  setActiveStage(nextStage)
}

function onScroll() {
  if (scrollRafId) return
  scrollRafId = window.requestAnimationFrame(() => {
    scrollRafId = 0
    updateActiveStage()
  })
}

function onResize() {
  if (resizeRafId) return
  resizeRafId = window.requestAnimationFrame(() => {
    resizeRafId = 0
    updateActiveStage()
  })
}

function scrollToScene(index) {
  const scenes = [
    videoSectionRef.value,
    heroSectionRef.value,
    systemSectionRef.value,
    showcaseSectionRef.value,
  ]

  scenes[index]?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

watch(activeStage, (stage) => {
  appStore.homeSlide = stage
})

onMounted(async () => {
  appStore.homeSlide = 0
  updateActiveStage()

  window.addEventListener('scroll', onScroll, { passive: true })
  window.addEventListener('resize', onResize, { passive: true })

  try {
    const res = await getProducts({ is_featured: true, page_size: 4 })
    featured.value = res.data.results || []
  } catch {
    featured.value = []
  }
})

onUnmounted(() => {
  appStore.homeSlide = -1

  if (scrollRafId) {
    window.cancelAnimationFrame(scrollRafId)
    scrollRafId = 0
  }

  window.removeEventListener('scroll', onScroll)
  window.removeEventListener('resize', onResize)
})
</script>

<style scoped>
.home {
  position: relative;
  background: var(--ink);
}

.home-scroll-wrapper {
  scroll-snap-type: y mandatory;
}

.screen {
  position: relative;
  min-height: 100svh;
  overflow: clip;
  scroll-snap-align: start;
}

.screen-video {
  background: var(--ink);
  overflow: hidden;
}

.video-cta-wrap {
  position: absolute;
  left: 50%;
  bottom: calc(var(--sp-12) + 52px);
  z-index: 2;
  transform: translateX(-50%);
}

.video-auth {
  display: flex;
  align-items: center;
  gap: var(--sp-4);
  padding: var(--sp-2);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--r-full);
  background: rgba(10, 10, 26, 0.55);
}

.auth-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 148px;
  height: 52px;
  padding: 0 var(--sp-8);
  border-radius: var(--r-full);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  backdrop-filter: blur(20px);
}

.auth-btn-primary {
  background: var(--accent);
  color: var(--white);
  border: 1px solid var(--accent);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.34);
}

.auth-btn-primary:hover {
  transform: translateY(-2px);
  background: var(--accent-light);
  box-shadow: 0 16px 36px rgba(59, 130, 246, 0.42);
}

.auth-btn-secondary {
  background: var(--glass-bg);
  color: var(--text-primary);
  border: 1px solid var(--glass-border);
}

.auth-btn-secondary:hover {
  border-color: var(--accent);
  box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
}

.scroll-hint {
  position: absolute;
  left: 50%;
  bottom: var(--sp-8);
  z-index: 2;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: var(--sp-2);
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.76);
  font-family: var(--font-display);
  font-size: var(--text-xs);
  letter-spacing: 0.08em;
  transform: translateX(-50%);
}

.scroll-mouse {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  width: 22px;
  height: 36px;
  padding-top: 6px;
  border: 2px solid rgba(255, 255, 255, 0.28);
  border-radius: 999px;
}

.scroll-dot {
  width: 3px;
  height: 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.72);
  animation: scrollDot 2s ease-in-out infinite;
}

.screen-hero {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--ink);
  color: var(--white);
}

.hero-bg {
  position: absolute;
  inset: 0;
}

.hero-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.5;
}

.orb-1 {
  top: -180px;
  right: -80px;
  width: 560px;
  height: 560px;
  background: var(--accent-glow);
  animation: floatSlow 20s ease-in-out infinite;
}

.orb-2 {
  bottom: -120px;
  left: -50px;
  width: 420px;
  height: 420px;
  background: var(--purple-glow);
  animation: floatSlow 24s ease-in-out infinite reverse;
}

.orb-3 {
  top: 42%;
  left: 45%;
  width: 320px;
  height: 320px;
  background: var(--pink-glow);
  animation: floatSlow 18s ease-in-out infinite;
}

.hero-grid,
.showcase-grid {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 56px 56px;
}

.hero-content {
  position: relative;
  z-index: 2;
  max-width: 780px;
  padding-top: calc(var(--nav-h) + var(--sp-10));
  text-align: center;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
  margin-bottom: var(--sp-8);
  padding: var(--sp-2) var(--sp-5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--r-full);
  background: rgba(255, 255, 255, 0.1);
  font-family: var(--font-display);
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-light);
  animation: pulse 2s ease-in-out infinite;
}

.hero-title {
  margin-bottom: var(--sp-6);
  font-family: var(--font-display);
  font-size: var(--text-hero);
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.04em;
}

.accent {
  color: var(--accent-light);
}

.title-line {
  background: linear-gradient(90deg, var(--white) 0%, var(--accent-light) 45%, var(--white) 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientShift 6s ease-in-out infinite;
}

.hero-desc {
  margin-bottom: var(--sp-10);
  color: rgba(255, 255, 255, 0.64);
  font-size: var(--text-lg);
  line-height: 1.75;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: var(--sp-4);
}

.hero-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.32);
  animation: float 6s ease-in-out infinite;
}

.p-1 { top: 15%; left: 10%; animation-duration: 7s; }
.p-2 { top: 55%; left: 85%; width: 3px; height: 3px; animation-delay: 1s; }
.p-3 { top: 25%; left: 65%; width: 2px; height: 2px; opacity: 0.45; animation-delay: 2s; }
.p-4 { top: 75%; left: 20%; animation-delay: 3s; }
.p-5 { top: 40%; left: 45%; width: 3px; height: 3px; opacity: 0.4; animation-delay: 4s; }
.p-6 { top: 10%; left: 90%; width: 2px; height: 2px; opacity: 0.6; animation-delay: 5s; }
.p-7 { top: 80%; left: 70%; width: 3px; height: 3px; opacity: 0.35; animation-delay: 1.5s; }
.p-8 { top: 60%; left: 35%; width: 2px; height: 2px; opacity: 0.5; animation-delay: 3.5s; }

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--sp-2);
  height: 48px;
  padding: 0 var(--sp-8);
  border: none;
  border-radius: var(--r-full);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
  text-decoration: none;
  transition: transform var(--dur-normal) var(--ease-spring), background var(--dur-normal), box-shadow var(--dur-normal);
}

.btn-lg {
  height: 56px;
  padding: 0 var(--sp-10);
  font-size: var(--text-base);
}

.btn-primary {
  background: var(--glass-bg);
  color: var(--text-primary);
  border: 1px solid var(--glass-border);
}

.btn-primary:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.2);
}

.btn-ghost {
  border: 1px solid rgba(255, 255, 255, 0.14);
  background: rgba(255, 255, 255, 0.1);
  color: var(--white);
}

.btn-ghost:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.12);
}

.screen-system {
  display: flex;
  align-items: center;
  background: var(--ink);
  color: var(--text-primary);
}

.system-shell {
  display: grid;
  gap: var(--sp-8);
  padding-top: calc(var(--nav-h) + var(--sp-8));
  padding-bottom: var(--sp-8);
}

.system-head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: var(--sp-8);
  align-items: start;
}

.system-copy {
  max-width: 560px;
  padding-top: var(--sp-4);
}

.section-kicker {
  display: inline-flex;
  margin-bottom: var(--sp-3);
  color: var(--accent);
  font-family: var(--font-display);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.section-title {
  margin-bottom: var(--sp-4);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(2.35rem, 3.8vw, 4rem);
  font-weight: 800;
  line-height: 1.02;
  letter-spacing: -0.04em;
  text-wrap: balance;
}

.section-desc {
  color: var(--text-secondary);
  max-width: 52ch;
  font-size: clamp(1rem, 1.2vw, 1.125rem);
  line-height: 1.8;
}

.system-board {
  padding: var(--sp-6);
  border: 1px solid var(--glass-border);
  border-radius: calc(var(--r-xl) + 4px);
  background: var(--glass-bg);
  box-shadow: var(--glass-shadow);
}

.system-board__header {
  display: grid;
  gap: var(--sp-2);
  margin-bottom: var(--sp-5);
}

.system-board__eyebrow {
  color: var(--accent);
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.system-board__header p {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.8;
}

.system-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--sp-4);
}

.metric-card {
  border: 1px solid var(--glass-border);
  border-radius: var(--r-lg);
  padding: var(--sp-6);
  transition: all 0.3s;
}

.metric-card:hover {
  border-color: var(--accent);
  transform: translateY(-2px);
  box-shadow: var(--glass-shadow-hover);
}

.metric-card strong {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-lg);
}

.metric-card span {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.7;
}

.system-steps {
  display: grid;
  gap: var(--sp-3);
}

.step-card {
  display: grid;
  grid-template-columns: 72px minmax(0, 1fr);
  gap: var(--sp-4);
  align-items: start;
  padding: var(--sp-5);
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  background: var(--glass-bg);
  box-shadow: var(--glass-shadow);
  transition: all 0.3s;
}

.step-card:hover {
  transform: translateY(-4px);
  border-color: var(--accent);
  box-shadow: var(--glass-shadow-hover);
}

.step-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 18px;
  background: rgba(255, 122, 92, 0.08);
  color: var(--accent);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
  letter-spacing: 0.08em;
}

.step-copy {
  min-width: 0;
}

.step-card h3 {
  margin-bottom: var(--sp-3);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(1.55rem, 2vw, 2rem);
  font-weight: 700;
  line-height: 1.12;
}

.step-card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.8;
}

.screen-showcase {
  display: flex;
  align-items: center;
  background: #090913;
  color: var(--white);
}

.showcase-bg {
  position: absolute;
  inset: 0;
}

.showcase-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
}

.glow-left {
  left: -120px;
  bottom: -80px;
  width: 340px;
  height: 340px;
  background: rgba(74, 58, 255, 0.28);
}

.glow-right {
  top: -60px;
  right: -80px;
  width: 380px;
  height: 380px;
  background: rgba(232, 89, 58, 0.26);
}

.showcase-shell {
  position: relative;
  z-index: 2;
  padding-top: calc(var(--nav-h) + var(--sp-8));
  padding-bottom: var(--sp-8);
}

.showcase-header {
  display: flex;
  justify-content: space-between;
  gap: var(--sp-8);
  align-items: flex-end;
  margin-bottom: var(--sp-8);
}

.section-kicker-on-dark {
  color: rgba(255, 122, 92, 0.9);
}

.section-title-on-dark {
  color: var(--white);
}

.section-desc-on-dark {
  max-width: 720px;
  color: rgba(255, 255, 255, 0.64);
}

.showcase-grid-cards {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: var(--sp-5);
}

.showcase-card {
  display: grid;
  grid-template-rows: 180px 1fr;
  overflow: hidden;
  border: 1px solid var(--glass-border);
  border-radius: var(--r-xl);
  background: var(--glass-bg);
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.showcase-card:hover {
  transform: translateY(-8px);
  border-color: var(--accent);
  box-shadow: var(--glass-shadow-hover);
}

.showcase-card-media {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.3) 100%);
  background-position: center;
  background-size: cover;
}

.showcase-card-body {
  display: grid;
  gap: var(--sp-3);
  padding: var(--sp-5);
}

.showcase-card-label {
  color: rgba(255, 255, 255, 0.52);
  font-family: var(--font-display);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.showcase-card h3 {
  color: var(--white);
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  line-height: 1.25;
}

.showcase-card p {
  color: rgba(255, 255, 255, 0.66);
  font-size: var(--text-sm);
  line-height: 1.8;
}

.showcase-card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  color: rgba(255, 255, 255, 0.78);
  font-family: var(--font-display);
  font-size: var(--text-sm);
}

.showcase-card-arrow {
  font-size: var(--text-lg);
  line-height: 1;
}

.hero-controls {
  position: fixed;
  inset: 0;
  z-index: 50;
  pointer-events: none;
  transition: opacity var(--dur-normal) var(--ease-out);
}

.hero-controls.is-hidden {
  opacity: 0;
  pointer-events: none !important;
}

.hero-controls.is-hidden .snap-dots,
.hero-controls.is-hidden .snap-counter {
  transform: translateY(12px);
}

.snap-dots {
  position: absolute;
  top: 50%;
  left: var(--sp-8);
  display: flex;
  flex-direction: column;
  gap: var(--sp-4);
  align-items: center;
  transform: translateY(-50%);
  transition: transform var(--dur-normal) var(--ease-out);
  pointer-events: auto;
}

.dot {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  border: none;
  background: none;
}

.dot-inner {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.28);
  transition: all var(--dur-normal) var(--ease-spring);
}

.dot:hover .dot-inner {
  background: rgba(255, 255, 255, 0.5);
}

.dot.active .dot-inner {
  width: 12px;
  height: 12px;
  background: var(--white);
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.32);
}

.snap-counter {
  position: absolute;
  right: var(--sp-8);
  bottom: var(--sp-8);
  color: rgba(255, 255, 255, 0.34);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  letter-spacing: 0.06em;
  transition: transform var(--dur-normal) var(--ease-out);
}

.counter-current {
  color: var(--white);
  font-weight: 600;
}

.counter-sep {
  margin: 0 4px;
}

@keyframes scrollDot {
  0% { transform: translateY(0); opacity: 0.8; }
  50% { transform: translateY(6px); opacity: 0.24; }
  100% { transform: translateY(0); opacity: 0.8; }
}

@media (max-width: 1200px) {
  .showcase-grid-cards {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 1024px) {
  .system-head {
    grid-template-columns: 1fr;
  }

  .system-copy {
    max-width: none;
    padding-top: 0;
  }

  .system-metrics {
    grid-template-columns: 1fr;
  }

  .showcase-header {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 768px) {
  .video-cta-wrap {
    width: calc(100% - 32px);
    bottom: calc(var(--sp-12) + 56px);
  }

  .video-auth,
  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .auth-btn,
  .btn-lg {
    width: 100%;
  }

  .hero-desc br {
    display: none;
  }

  .showcase-grid-cards {
    grid-template-columns: 1fr;
  }

  .step-card {
    grid-template-columns: 1fr;
  }

  .step-index {
    width: 56px;
    height: 56px;
    border-radius: 14px;
  }

  .snap-dots {
    left: var(--sp-4);
  }

  .snap-counter {
    right: var(--sp-4);
    bottom: var(--sp-4);
  }
}

@media (prefers-reduced-motion: reduce) {
  .particle,
  .orb-1,
  .orb-2,
  .orb-3,
  .badge-dot,
  .title-line,
  .scroll-dot {
    animation: none !important;
  }

  .btn,
  .auth-btn,
  .step-card,
  .showcase-card,
  .dot-inner {
    transition: none !important;
  }
}
</style>
