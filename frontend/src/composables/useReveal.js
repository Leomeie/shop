import { onMounted, onUnmounted } from 'vue'

/**
 * Scroll-triggered reveal animation via Intersection Observer.
 * Usage: useReveal(elRef, 'fade-up', { delay: 100 })
 */
export function useReveal(targetRef, animation = 'fade-up', options = {}) {
  let observer = null

  onMounted(() => {
    const el = targetRef.value
    if (!el) return

    el.style.opacity = '0'
    el.classList.add('reveal-ready')

    observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          const delay = options.delay || 0
          setTimeout(() => {
            el.style.opacity = ''
            el.classList.add('reveal', `reveal-${animation}`)
          }, delay)
          observer.unobserve(el)
        }
      },
      { threshold: options.threshold || 0.15, rootMargin: options.rootMargin || '0px 0px -40px 0px' }
    )
    observer.observe(el)
  })

  onUnmounted(() => observer?.disconnect())
}
