<template>
  <div class="home">
    <section class="screen-hero" id="home-hero">
      <div class="hero-bg">
        <div class="hero-orb orb-1" />
        <div class="hero-orb orb-2" />
        <div class="hero-orb orb-3" />
        <div class="hero-logo-glow">
          <img src="/images/logo.png" alt="" />
        </div>
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
    </section>

    <section class="screen screen-system" id="home-system">
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
                  <h3>
                    <img :src="step.icon" alt="" class="step-title-icon" width="20" height="20" />
                    <GradientText variant="blue">{{ step.title }}</GradientText>
                  </h3>
                  <p>{{ step.desc }}</p>
                </div>
              </article>
            </div>
          </div>
        </div>

        <div class="system-metrics">
          <div class="metric-card glass-card">
            <div class="metric-icon"><img src="/icons/dingdan.svg" alt="" width="24" height="24" /></div>
            <strong><GradientText variant="blue">即时下载</GradientText></strong>
            <span>支付后立刻可用，不把时间耗在等待上。</span>
          </div>
          <div class="metric-card glass-card">
            <div class="metric-icon"><img src="/icons/pingtai.svg" alt="" width="24" height="24" /></div>
            <strong><GradientText variant="purple">结构清晰</GradientText></strong>
            <span>资源按工作流和用途组织，减少来回跳转。</span>
          </div>
          <div class="metric-card glass-card">
            <div class="metric-icon"><img src="/icons/guanli.svg" alt="" width="24" height="24" /></div>
            <strong><GradientText variant="pink">持续维护</GradientText></strong>
            <span>版本迭代与资源更新可长期获取。</span>
          </div>
        </div>
      </div>
    </section>

    <section class="screen screen-showcase" id="home-showcase">
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
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { gsap, ScrollTrigger } from '../../composables/useGsap.js'
import { getProducts } from '../../api/product'
import GradientText from '../../components/GradientText.vue'

const featured = ref([])
let ctx = null

const workflowSteps = [
  { id: '01', title: '快速发现', desc: '在品牌 Hero 和精选入口里先建立判断，再决定看哪类资源，不再被杂乱的信息面板分散注意力。', icon: '/icons/tupian.svg' },
  { id: '02', title: '低成本决策', desc: '每个资源都带着明确的用途、工作流方向和交付价值，让用户不用猜它能解决什么问题。', icon: '/icons/wendang.svg' },
  { id: '03', title: '完成交付', desc: '从购买到下载形成闭环，减少跳转、减少等待、减少"买了却不会用"的断层。', icon: '/icons/cunchu.svg' },
]

const fallbackShowcase = [
  { id: 'prompt-bundle', label: 'Prompt Bundle', title: '高转化 Prompt 模板', desc: '适合营销文案、图像生成和角色设定的成套模板，开箱即用。', meta: '模板集合', to: '/products?search=prompt', cover: '' },
  { id: 'comfyui-workflow', label: 'Workflow', title: 'ComfyUI 工作流', desc: '把常用节点链路整理成可重复使用的工作流，降低试错成本。', meta: '工作流方向', to: '/products?search=workflow', cover: '' },
  { id: 'lora-models', label: 'LoRA Models', title: '风格 LoRA 模板', desc: '针对角色、材质、海报和品牌风格整理的训练模型合集。', meta: '模型资源', to: '/products?search=LoRA', cover: '' },
  { id: 'design-assets', label: 'Design Assets', title: '设计交付素材包', desc: '围绕封面、海报、社媒图和演示文稿场景准备的交付级素材。', meta: '素材方向', to: '/products?search=设计', cover: '' },
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

onMounted(async () => {
  try {
    const res = await getProducts({ is_featured: true, page_size: 4 })
    featured.value = res.data.results || []
  } catch {
    featured.value = []
  }

  ctx = gsap.context(() => {
    // Hero entrance timeline
    const heroTl = gsap.timeline({ defaults: { ease: 'power3.out' } })
    heroTl
      .fromTo('.hero-logo-glow', { opacity: 0, scale: 0.3 }, { opacity: 0.28, scale: 1, duration: 2, ease: 'power2.out' }, 0)
      .fromTo('.hero-orb', { scale: 0, opacity: 0 }, { scale: 1, opacity: 0.45, duration: 1.2, stagger: 0.15 }, 0)
      .fromTo('.hero-badge', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6 }, 0.2)
      .fromTo('.hero-title', { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7 }, 0.35)
      .fromTo('.hero-desc', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6 }, 0.55)
      .fromTo('.hero-actions', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6 }, 0.7)

    // Showcase background glow parallax
    gsap.to('.glow-left', {
      y: -60,
      scrollTrigger: {
        trigger: '.screen-showcase',
        start: 'top bottom',
        end: 'bottom top',
        scrub: 1,
      },
    })
    gsap.to('.glow-right', {
      y: 40,
      scrollTrigger: {
        trigger: '.screen-showcase',
        start: 'top bottom',
        end: 'bottom top',
        scrub: 1,
      },
    })
  })
})

onUnmounted(() => {
  ctx?.revert()
})
</script>

<style scoped>
.home {
  position: relative;
  background: var(--ink);
}

/* ── Hero (首屏) ── */
.screen-hero {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100dvh;
  overflow: hidden;
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
  filter: blur(24px);
  opacity: 0;
  transform: scale(0);
  will-change: transform, opacity;
}

.orb-1 {
  top: -120px;
  right: -60px;
  width: 320px;
  height: 320px;
  background: var(--accent-glow);
  animation: floatSlow 20s ease-in-out infinite;
}

.orb-2 {
  bottom: -80px;
  left: -40px;
  width: 240px;
  height: 240px;
  background: var(--purple-glow);
  animation: floatSlow 24s ease-in-out infinite reverse;
}

.orb-3 {
  top: 42%;
  left: 45%;
  width: 220px;
  height: 220px;
  background: var(--pink-glow);
  animation: floatSlow 18s ease-in-out infinite;
}

.hero-logo-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%) scale(0.5);
  width: 600px;
  height: 600px;
  opacity: 0;
  pointer-events: none;
  z-index: 1;
  mix-blend-mode: screen;
  will-change: transform, opacity;
}
.hero-logo-glow img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: brightness(1.8) saturate(1.2);
  mask-image: radial-gradient(circle at center, black 30%, transparent 72%);
  -webkit-mask-image: radial-gradient(circle at center, black 30%, transparent 72%);
  animation: logoPulse 4s ease-in-out infinite;
}
.hero-logo-glow::after {
  content: '';
  position: absolute;
  inset: -30%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.25) 0%, rgba(168, 85, 247, 0.15) 35%, rgba(59, 130, 246, 0.06) 60%, transparent 75%);
  pointer-events: none;
  animation: logoPulse 4s ease-in-out infinite;
}

@keyframes logoPulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.04); opacity: 0.85; }
}

.hero-grid {
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

.hero-badge,
.hero-title,
.hero-desc,
.hero-actions {
  opacity: 0;
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

.btn-gradient {
  background: var(--gradient-blue);
  color: var(--white);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.28);
}

.btn-gradient:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(59, 130, 246, 0.38);
}

.btn-glass {
  background: rgba(255, 255, 255, 0.08);
  color: var(--white);
  border: 1px solid rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(8px);
}

.btn-glass:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.12);
}

/* ── System section ── */
.screen {
  position: relative;
  min-height: 100svh;
  overflow: clip;
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
  transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
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

.metric-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--r-md);
  background: rgba(99, 102, 241, 0.1);
  margin-bottom: var(--sp-3);
}
.metric-icon img {
  width: 24px;
  height: 24px;
  object-fit: contain;
  filter: brightness(0) invert(1);
  opacity: 0.7;
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
  transition: transform 0.3s, border-color 0.3s, box-shadow 0.3s;
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
  width: 64px;
  height: 64px;
  border-radius: 16px;
  background: rgba(59, 130, 246, 0.08);
  color: var(--accent);
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  letter-spacing: 0.08em;
}

.step-copy {
  min-width: 0;
}

.step-card h3 {
  display: flex;
  align-items: center;
  gap: var(--sp-2);
  margin-bottom: var(--sp-3);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(1.55rem, 2vw, 2rem);
  font-weight: 700;
  line-height: 1.12;
}

.step-title-icon {
  width: 20px;
  height: 20px;
  object-fit: contain;
  filter: brightness(0) invert(1);
  opacity: 0.5;
  flex-shrink: 0;
}

.step-card p {
  color: var(--text-secondary);
  font-size: 0.95rem;
  line-height: 1.8;
}

/* ── Showcase section ── */
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
  filter: blur(60px);
}

.glow-left {
  left: -120px;
  bottom: -80px;
  width: 280px;
  height: 280px;
  background: rgba(74, 58, 255, 0.28);
}

.glow-right {
  top: -60px;
  right: -80px;
  width: 300px;
  height: 300px;
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
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.3s, box-shadow 0.3s;
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

/* ── Responsive ── */
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
  .hero-logo-glow {
    width: 360px;
    height: 360px;
  }

  .hero-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .hero-desc br {
    display: none;
  }

  .showcase-grid-cards {
    grid-template-columns: 1fr;
  }

  .step-card {
    grid-template-columns: 56px 1fr;
  }

  .step-index {
    width: 56px;
    height: 56px;
    border-radius: 14px;
    font-size: var(--text-base);
  }
}

@media (prefers-reduced-motion: reduce) {
  .orb-1,
  .orb-2,
  .orb-3,
  .badge-dot,
  .title-line,
  .hero-logo-glow img,
  .hero-logo-glow::after {
    animation: none !important;
  }

  .btn,
  .step-card,
  .showcase-card {
    transition: none !important;
  }
}
</style>
