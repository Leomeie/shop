import { onMounted, onUnmounted, watch, nextTick } from 'vue'
import { gsap, ScrollTrigger } from './useGsap.js'

export function useScrollReveal(containerRef, options = {}) {
  const {
    targets = '.reveal',
    stagger = 0.08,
    y = 40,
    duration = 0.6,
    ease = 'power3.out',
    start = 'top 85%',
    once = true,
    disabled = false,
  } = options

  let ctx = null

  function setup() {
    if (disabled) return
    const container = containerRef?.value?.$el || containerRef?.value
    if (!container) return

    ctx = gsap.context(() => {
      const els = container.querySelectorAll(targets)
      if (!els.length) return

      gsap.set(els, { opacity: 0, y })

      ScrollTrigger.batch(els, {
        start,
        once,
        onEnter(batch) {
          gsap.to(batch, {
            opacity: 1,
            y: 0,
            duration,
            ease,
            stagger,
            overwrite: true,
          })
        },
      })
    }, container)
  }

  function cleanup() {
    ctx?.revert()
    ctx = null
  }

  onMounted(() => nextTick(setup))
  onUnmounted(cleanup)

  return { refresh: () => { cleanup(); nextTick(setup) }, cleanup }
}
