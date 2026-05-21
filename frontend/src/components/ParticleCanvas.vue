<template>
  <canvas ref="canvasRef" class="particle-canvas" />
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvasRef = ref(null)

/* ─── Configuration ─── */
const C = {
  colors: {
    blue:   { r: 59,  g: 130, b: 246 },
    purple: { r: 139, g: 92,  b: 246 },
    pink:   { r: 236, g: 72,  b: 153 },
    indigo: { r: 99,  g: 102, b: 241 },
    cyan:   { r: 34,  g: 211, b: 238 },
  },
  palette: ['blue', 'purple', 'pink', 'indigo', 'cyan'],
  stars: { count: 120, maxSize: 1.2, twinkleSpeed: 0.008 },
  particles: { count: 60, minR: 1, maxR: 2.8, speed: 0.35, connectionDist: 160 },
  orbs: { count: 4, minR: 80, maxR: 180, speed: 0.0002 },
  meteors: { interval: 2200, speed: 8, length: 120, width: 1.5 },
  nebulae: { count: 6, minR: 100, maxR: 300, alpha: 0.03 },
  grid: { spacing: 60, alpha: 0.04 },
  mouse: { radius: 220, force: 0.025, trailMax: 18, rippleMax: 3 },
  hexagons: { count: 5, minR: 30, maxR: 60, alpha: 0.04 },
}

function rnd(a, b) { return a + Math.random() * (b - a) }
function rndInt(a, b) { return Math.floor(rnd(a, b + 1)) }
function pick(arr) { return arr[rndInt(0, arr.length - 1)] }
function rgba(c, a) { return `rgba(${c.r},${c.g},${c.b},${a})` }
function lerp(a, b, t) { return a + (b - a) * t }

/* ─── Star field ─── */
class Star {
  constructor(w, h) { this.reset(w, h, true) }
  reset(w, h, init) {
    this.x = Math.random() * w
    this.y = Math.random() * h
    this.r = rnd(0.3, C.stars.maxSize)
    this.alpha = rnd(0.2, 0.8)
    this.phase = init ? Math.random() * Math.PI * 2 : 0
    this.speed = rnd(C.stars.twinkleSpeed * 0.5, C.stars.twinkleSpeed * 1.5)
  }
  update() { this.phase += this.speed }
  draw(ctx) {
    const a = this.alpha * (0.5 + 0.5 * Math.sin(this.phase))
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
    ctx.fillStyle = `rgba(255,255,255,${a})`
    ctx.fill()
  }
}

/* ─── Drifting particle ─── */
class Particle {
  constructor(w, h) { this.reset(w, h) }
  reset(w, h) {
    this.x = Math.random() * w
    this.y = Math.random() * h
    this.vx = (Math.random() - 0.5) * C.particles.speed
    this.vy = (Math.random() - 0.5) * C.particles.speed
    this.r = rnd(C.particles.minR, C.particles.maxR)
    const col = C.colors[pick(C.palette)]
    this.color = col
    this.alpha = rnd(0.35, 0.85)
    this.pulse = Math.random() * Math.PI * 2
    this.pulseSpd = rnd(0.008, 0.025)
  }
  update(w, h, mx, my) {
    this.pulse += this.pulseSpd
    const dx = mx - this.x, dy = my - this.y
    const dist = Math.sqrt(dx * dx + dy * dy)
    if (dist < C.mouse.radius && dist > 0) {
      const f = (C.mouse.radius - dist) / C.mouse.radius * C.mouse.force
      this.vx -= (dx / dist) * f
      this.vy -= (dy / dist) * f
    }
    this.vx *= 0.988
    this.vy *= 0.988
    this.x += this.vx; this.y += this.vy
    if (this.x < -20) this.x = w + 20
    else if (this.x > w + 20) this.x = -20
    if (this.y < -20) this.y = h + 20
    else if (this.y > h + 20) this.y = -20
  }
  draw(ctx) {
    const a = this.alpha * (0.6 + 0.4 * Math.sin(this.pulse))
    const c = this.color
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
    ctx.fillStyle = rgba(c, a)
    ctx.fill()
    if (this.r > 1.6) {
      const g = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.r * 5)
      g.addColorStop(0, rgba(c, a * 0.25))
      g.addColorStop(1, rgba(c, 0))
      ctx.beginPath()
      ctx.arc(this.x, this.y, this.r * 5, 0, Math.PI * 2)
      ctx.fillStyle = g
      ctx.fill()
    }
  }
}

/* ─── Nebula cloud ─── */
class Nebula {
  constructor(w, h) { this.reset(w, h) }
  reset(w, h) {
    this.x = Math.random() * w
    this.y = Math.random() * h
    this.r = rnd(C.nebulae.minR, C.nebulae.maxR)
    this.color = C.colors[pick(C.palette)]
    this.vx = rnd(-0.08, 0.08)
    this.vy = rnd(-0.05, 0.05)
    this.phase = Math.random() * Math.PI * 2
  }
  update(w, h, dt) {
    this.phase += dt * 0.0003
    this.x += this.vx + Math.sin(this.phase) * 0.15
    this.y += this.vy + Math.cos(this.phase * 0.7) * 0.1
    if (this.x < -this.r) this.x = w + this.r
    if (this.x > w + this.r) this.x = -this.r
    if (this.y < -this.r) this.y = h + this.r
    if (this.y > h + this.r) this.y = -this.r
  }
  draw(ctx) {
    const g = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.r)
    g.addColorStop(0, rgba(this.color, C.nebulae.alpha))
    g.addColorStop(0.6, rgba(this.color, C.nebulae.alpha * 0.3))
    g.addColorStop(1, rgba(this.color, 0))
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
    ctx.fillStyle = g
    ctx.fill()
  }
}

/* ─── Glowing orb ─── */
class Orb {
  constructor(w, h) { this.reset(w, h) }
  reset(w, h) {
    this.x = Math.random() * w
    this.y = Math.random() * h
    this.r = rnd(C.orbs.minR, C.orbs.maxR)
    this.color = C.colors[pick(C.palette)]
    this.phase = Math.random() * Math.PI * 2
    this.speed = rnd(C.orbs.speed * 0.6, C.orbs.speed * 1.4)
    this.offsetX = rnd(0.3, 0.7)
    this.offsetY = rnd(0.3, 0.7)
  }
  update(w, h, time) {
    this.phase += this.speed
    this.x = w * this.offsetX + Math.sin(this.phase) * w * 0.2
    this.y = h * this.offsetY + Math.cos(this.phase * 0.8) * h * 0.15
  }
  draw(ctx) {
    const pulse = 0.7 + 0.3 * Math.sin(this.phase * 3)
    const g = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.r)
    g.addColorStop(0, rgba(this.color, 0.07 * pulse))
    g.addColorStop(0.4, rgba(this.color, 0.03 * pulse))
    g.addColorStop(1, rgba(this.color, 0))
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
    ctx.fillStyle = g
    ctx.fill()
  }
}

/* ─── Shooting star / meteor ─── */
class Meteor {
  constructor(w, h) { this.reset(w, h) }
  reset(w, h) {
    this.active = false
    this.timer = 0
    this.x = 0; this.y = 0; this.vx = 0; this.vy = 0
    this.life = 0; this.maxLife = 0
    this.color = C.colors[pick(C.palette)]
    this.nextTime = rnd(800, C.meteors.interval)
  }
  spawn(w, h) {
    this.active = true
    this.x = rnd(0, w * 0.8)
    this.y = rnd(-50, h * 0.4)
    const angle = rnd(0.35, 0.75)
    this.vx = Math.cos(angle) * C.meteors.speed
    this.vy = Math.sin(angle) * C.meteors.speed
    this.maxLife = rnd(400, 800)
    this.life = 0
    this.color = C.colors[pick(C.palette)]
  }
  update(dt) {
    if (!this.active) {
      this.timer += dt
      if (this.timer >= this.nextTime) { this.active = true; return }
      return
    }
    this.life += dt
    if (this.life >= this.maxLife) { this.active = false; this.timer = 0; this.nextTime = rnd(1200, C.meteors.interval); return }
    this.x += this.vx
    this.y += this.vy
  }
  draw(ctx) {
    if (!this.active) return
    const progress = this.life / this.maxLife
    const fade = progress < 0.2 ? progress / 0.2 : 1 - (progress - 0.2) / 0.8
    const c = this.color
    const tailX = this.x - this.vx * (C.meteors.length / C.meteors.speed)
    const tailY = this.y - this.vy * (C.meteors.length / C.meteors.speed)
    const g = ctx.createLinearGradient(tailX, tailY, this.x, this.y)
    g.addColorStop(0, rgba(c, 0))
    g.addColorStop(0.7, rgba(c, fade * 0.4))
    g.addColorStop(1, rgba(c, fade * 0.9))
    ctx.beginPath()
    ctx.moveTo(tailX, tailY)
    ctx.lineTo(this.x, this.y)
    ctx.strokeStyle = g
    ctx.lineWidth = C.meteors.width
    ctx.lineCap = 'round'
    ctx.stroke()
    ctx.beginPath()
    ctx.arc(this.x, this.y, 2, 0, Math.PI * 2)
    ctx.fillStyle = rgba({ r: 255, g: 255, b: 255 }, fade * 0.9)
    ctx.fill()
  }
}

/* ─── Hexagon outline ─── */
class Hexagon {
  constructor(w, h) { this.reset(w, h) }
  reset(w, h) {
    this.x = Math.random() * w
    this.y = Math.random() * h
    this.r = rnd(C.hexagons.minR, C.hexagons.maxR)
    this.rot = Math.random() * Math.PI
    this.rotSpeed = rnd(-0.0003, 0.0003)
    this.alpha = C.hexagons.alpha
    this.color = C.colors[pick(C.palette)]
    this.phase = Math.random() * Math.PI * 2
  }
  update(dt) {
    this.rot += this.rotSpeed
    this.phase += dt * 0.0005
  }
  draw(ctx) {
    const a = this.alpha * (0.5 + 0.5 * Math.sin(this.phase))
    ctx.beginPath()
    for (let i = 0; i < 6; i++) {
      const angle = this.rot + (Math.PI / 3) * i
      const px = this.x + this.r * Math.cos(angle)
      const py = this.y + this.r * Math.sin(angle)
      i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py)
    }
    ctx.closePath()
    ctx.strokeStyle = rgba(this.color, a)
    ctx.lineWidth = 0.6
    ctx.stroke()
  }
}

/* ─── Mouse trail spark ─── */
class Spark {
  constructor(x, y, color) {
    this.x = x; this.y = y
    this.vx = (Math.random() - 0.5) * 3
    this.vy = (Math.random() - 0.5) * 3
    this.r = rnd(0.8, 2)
    this.life = 0
    this.maxLife = rnd(300, 700)
    this.color = color
  }
  update(dt) {
    this.life += dt
    this.x += this.vx; this.y += this.vy
    this.vx *= 0.97; this.vy *= 0.97
    return this.life < this.maxLife
  }
  draw(ctx) {
    const fade = 1 - this.life / this.maxLife
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.r * fade, 0, Math.PI * 2)
    ctx.fillStyle = rgba(this.color, fade * 0.8)
    ctx.fill()
  }
}

/* ─── Click ripple ─── */
class Ripple {
  constructor(x, y, color) {
    this.x = x; this.y = y
    this.r = 0; this.maxR = rnd(80, 160)
    this.life = 0; this.maxLife = 800
    this.color = color
  }
  update(dt) {
    this.life += dt
    this.r = (this.life / this.maxLife) * this.maxR
    return this.life < this.maxLife
  }
  draw(ctx) {
    const fade = 1 - this.life / this.maxLife
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2)
    ctx.strokeStyle = rgba(this.color, fade * 0.5)
    ctx.lineWidth = 1.5
    ctx.stroke()
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.r * 0.6, 0, Math.PI * 2)
    ctx.strokeStyle = rgba(this.color, fade * 0.25)
    ctx.lineWidth = 0.8
    ctx.stroke()
  }
}

/* ─── Main setup ─── */
onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  let w, h, dpr
  const state = {
    stars: [], particles: [], nebulae: [], orbs: [], meteors: [], hexagons: [],
    sparks: [], ripples: [],
    mouseX: -9999, mouseY: -9999,
    lastTime: 0, running: true,
  }

  function resize() {
    dpr = window.devicePixelRatio || 1
    const rect = canvas.parentElement.getBoundingClientRect()
    w = rect.width; h = rect.height
    canvas.width = w * dpr; canvas.height = h * dpr
    canvas.style.width = w + 'px'; canvas.style.height = h + 'px'
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  }

  function init() {
    state.stars = Array.from({ length: C.stars.count }, () => new Star(w, h))
    state.particles = Array.from({ length: C.particles.count }, () => new Particle(w, h))
    state.nebulae = Array.from({ length: C.nebulae.count }, () => new Nebula(w, h))
    state.orbs = Array.from({ length: C.orbs.count }, () => new Orb(w, h))
    state.meteors = Array.from({ length: 3 }, () => new Meteor(w, h))
    state.hexagons = Array.from({ length: C.hexagons.count }, () => new Hexagon(w, h))
  }

  resize(); init()

  /* ─── Background gradient ─── */
  function drawBg(time) {
    ctx.fillStyle = '#0a0a1a'
    ctx.fillRect(0, 0, w, h)
    const t = time * 0.0001
    const positions = [
      { x: w * (0.3 + 0.2 * Math.sin(t)), y: h * (0.3 + 0.2 * Math.cos(t * 0.7)), color: C.colors.blue },
      { x: w * (0.7 + 0.2 * Math.cos(t * 1.1)), y: h * (0.6 + 0.2 * Math.sin(t * 0.9)), color: C.colors.purple },
      { x: w * (0.5 + 0.15 * Math.sin(t * 0.6)), y: h * (0.8 + 0.1 * Math.cos(t * 1.3)), color: C.colors.pink },
    ]
    for (const p of positions) {
      const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, w * 0.35)
      g.addColorStop(0, rgba(p.color, 0.06))
      g.addColorStop(1, rgba(p.color, 0))
      ctx.fillStyle = g
      ctx.fillRect(0, 0, w, h)
    }
  }

  /* ─── Grid overlay ─── */
  function drawGrid() {
    ctx.strokeStyle = `rgba(255,255,255,${C.grid.alpha})`
    ctx.lineWidth = 0.3
    for (let x = 0; x < w; x += C.grid.spacing) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke()
    }
    for (let y = 0; y < h; y += C.grid.spacing) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke()
    }
  }

  /* ─── Connection lines ─── */
  function drawConnections() {
    const ps = state.particles
    for (let i = 0; i < ps.length; i++) {
      for (let j = i + 1; j < ps.length; j++) {
        const dx = ps[i].x - ps[j].x, dy = ps[i].y - ps[j].y
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < C.particles.connectionDist) {
          const opacity = (1 - dist / C.particles.connectionDist) * 0.12
          ctx.beginPath()
          ctx.moveTo(ps[i].x, ps[i].y); ctx.lineTo(ps[j].x, ps[j].y)
          ctx.strokeStyle = `rgba(${ps[i].color.r},${ps[i].color.g},${ps[i].color.b},${opacity})`
          ctx.lineWidth = 0.4
          ctx.stroke()
        }
      }
    }
  }

  /* ─── Mouse trail emission ─── */
  let sparkTimer = 0
  function emitSparks(dt) {
    sparkTimer += dt
    if (sparkTimer > 40 && state.mouseX > 0) {
      sparkTimer = 0
      if (state.sparks.length < 60) {
        state.sparks.push(new Spark(state.mouseX, state.mouseY, pick([C.colors.blue, C.colors.purple, C.colors.cyan])))
      }
    }
  }

  /* ─── Animation loop ─── */
  function frame(time) {
    if (!state.running) return
    const dt = Math.min(time - state.lastTime, 50)
    state.lastTime = time

    drawBg(time)
    drawGrid()

    for (const n of state.nebulae) { n.update(w, h, dt); n.draw(ctx) }
    for (const o of state.orbs) { o.update(w, h, time); o.draw(ctx) }
    for (const s of state.stars) { s.update(); s.draw(ctx) }
    for (const h of state.hexagons) { h.update(dt); h.draw(ctx) }

    drawConnections()

    for (const p of state.particles) { p.update(w, h, state.mouseX, state.mouseY); p.draw(ctx) }
    for (const m of state.meteors) { m.update(dt); m.draw(ctx) }

    emitSparks(dt)
    state.sparks = state.sparks.filter(s => { s.draw(ctx); return s.update(dt) })
    state.ripples = state.ripples.filter(r => { r.draw(ctx); return r.update(dt) })

    requestAnimationFrame(frame)
  }

  state.lastTime = performance.now()
  requestAnimationFrame(frame)

  /* ─── Event handlers ─── */
  const onMove = (e) => {
    const rect = canvas.getBoundingClientRect()
    state.mouseX = e.clientX - rect.left
    state.mouseY = e.clientY - rect.top
  }
  const onLeave = () => { state.mouseX = -9999; state.mouseY = -9999 }
  const onClick = (e) => {
    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left, y = e.clientY - rect.top
    if (state.ripples.length < C.mouse.rippleMax) {
      state.ripples.push(new Ripple(x, y, pick([C.colors.blue, C.colors.purple, C.colors.pink, C.colors.cyan])))
    }
    for (let i = 0; i < 12; i++) {
      state.sparks.push(new Spark(x, y, pick([C.colors.blue, C.colors.purple, C.colors.cyan, C.colors.pink])))
    }
  }
  const onResize = () => {
    resize()
    state.stars = Array.from({ length: C.stars.count }, () => new Star(w, h))
  }

  canvas.addEventListener('mousemove', onMove)
  canvas.addEventListener('mouseleave', onLeave)
  canvas.addEventListener('click', onClick)
  window.addEventListener('resize', onResize)

  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      if (!state.running) { state.running = true; state.lastTime = performance.now(); requestAnimationFrame(frame) }
    } else { state.running = false }
  })
  observer.observe(canvas)

  canvas._cleanup = () => {
    state.running = false
    canvas.removeEventListener('mousemove', onMove)
    canvas.removeEventListener('mouseleave', onLeave)
    canvas.removeEventListener('click', onClick)
    window.removeEventListener('resize', onResize)
    observer.disconnect()
  }
})

onUnmounted(() => { canvasRef.value?._cleanup?.() })
</script>

<style scoped>
.particle-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  cursor: crosshair;
}
</style>
