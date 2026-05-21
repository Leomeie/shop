<template>
  <router-link :to="`/products/${product.id}`" class="card" @mousemove="onMouseMove" @mouseleave="onMouseLeave" ref="cardRef">
    <div class="card-visual">
      <div class="card-img-wrap">
        <img :src="product.main_image" :alt="product.name" loading="lazy" />
      </div>
      <div v-if="product.is_featured" class="card-badge">精选</div>
      <div class="card-shine" />
    </div>
    <div class="card-body">
      <p v-if="product.category_name" class="card-cat">{{ product.category_name }}</p>
      <h3 class="card-title">{{ product.name }}</h3>
      <div class="card-footer">
        <span class="card-price">¥{{ product.min_price_yuan }}</span>
        <span class="card-meta">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          {{ product.download_count }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { ref } from 'vue'

defineProps({ product: { type: Object, required: true } })

const cardRef = ref(null)
let rafId = 0
let cachedRect = null

function onMouseMove(e) {
  if (rafId) cancelAnimationFrame(rafId)
  rafId = requestAnimationFrame(() => {
    const card = cardRef.value?.$el || cardRef.value
    if (!card) return
    cachedRect = card.getBoundingClientRect()
    const rect = cachedRect
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const centerX = rect.width / 2
    const centerY = rect.height / 2
    const rotateX = (y - centerY) / centerY * -4
    const rotateY = (x - centerX) / centerX * 4

    card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-4px)`

    const shine = card.querySelector('.card-shine')
    if (shine) {
      shine.style.opacity = '1'
      shine.style.background = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.15) 0%, transparent 60%)`
    }
  })
}

function onMouseLeave() {
  if (rafId) cancelAnimationFrame(rafId)
  rafId = 0
  const card = cardRef.value?.$el || cardRef.value
  if (!card) return
  card.style.transform = ''
  const shine = card.querySelector('.card-shine')
  if (shine) shine.style.opacity = '0'
}
</script>

<style scoped>
.card {
  display: flex; flex-direction: column;
  background: var(--glass-bg);
  border-radius: var(--r-lg);
  overflow: hidden;
  border: 1px solid var(--glass-border);
  transition: transform 0.4s var(--ease-spring), box-shadow var(--dur-normal) var(--ease-out), border-color var(--dur-normal);
  text-decoration: none;
  transform-style: preserve-3d;
}
.card:hover {
  box-shadow: 0 20px 40px rgba(10,10,26,0.12);
  border-color: rgba(59,130,246,0.3);
}

.card-visual { position: relative; overflow: hidden; }
.card-img-wrap {
  aspect-ratio: 4 / 3; overflow: hidden;
  background: linear-gradient(135deg, var(--surface-2), var(--surface-3));
}
.card-img-wrap img {
  width: 100%; height: 100%; object-fit: cover;
  transition: transform 0.6s var(--ease-out);
}
.card:hover .card-img-wrap img { transform: scale(1.06); }

.card-shine {
  position: absolute; inset: 0; opacity: 0;
  transition: opacity var(--dur-fast); pointer-events: none;
  z-index: 2;
}

.card-badge {
  position: absolute; top: var(--sp-3); left: var(--sp-3); z-index: 3;
  padding: var(--sp-1) var(--sp-3);
  background: var(--accent); color: var(--white);
  font-family: var(--font-display); font-size: 11px; font-weight: 600;
  border-radius: var(--r-full); letter-spacing: 0.04em;
  box-shadow: 0 2px 8px rgba(59,130,246,0.3);
}

.card-body { padding: var(--sp-4) var(--sp-5) var(--sp-5); flex: 1; display: flex; flex-direction: column; }
.card-cat {
  font-family: var(--font-display); font-size: 11px; font-weight: 500;
  color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.06em;
  margin-bottom: var(--sp-2);
}
.card-title {
  font-family: var(--font-display); font-weight: 600;
  font-size: var(--text-base); line-height: 1.4;
  color: var(--text-primary); flex: 1;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  margin-bottom: var(--sp-3);
  transition: color var(--dur-fast);
}
.card:hover .card-title { color: var(--accent); }

.card-footer { display: flex; justify-content: space-between; align-items: center; }
.card-price {
  font-family: var(--font-display); font-weight: 700;
  font-size: var(--text-lg); color: var(--text-primary);
  transition: color var(--dur-fast);
}
.card:hover .card-price { color: var(--accent); }
.card-meta {
  display: flex; align-items: center; gap: var(--sp-1);
  font-size: var(--text-xs); color: var(--text-muted);
  transition: color var(--dur-fast);
}
.card:hover .card-meta { color: var(--text-secondary); }
</style>
