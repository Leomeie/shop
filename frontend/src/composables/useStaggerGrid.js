import { onMounted, onUnmounted, nextTick, watch } from 'vue'
import { gsap } from './useGsap.js'
import { useIsMobile } from './useGsap.js'

export function useStaggerGrid(gridRef, options = {}) {
  const {
    itemSelector = ':scope > *',
    stagger = 0.06,
    y = 24,
    duration = 0.5,
    ease = 'power3.out',
  } = options

  const isMobile = useIsMobile()
  let ctx = null

  function animate() {
    cleanup()
    const grid = gridRef?.value?.$el || gridRef?.value
    if (!grid) return

    ctx = gsap.context(() => {
      const items = grid.querySelectorAll(itemSelector)
      if (!items.length) return

      gsap.from(items, {
        opacity: 0,
        y,
        duration,
        ease,
        stagger: isMobile.value ? 0.03 : stagger,
        clearProps: 'all',
      })
    }, grid)
  }

  function cleanup() {
    ctx?.revert()
    ctx = null
  }

  function refresh() {
    cleanup()
    nextTick(animate)
  }

  onMounted(() => nextTick(animate))
  onUnmounted(cleanup)

  return { refresh, cleanup }
}
