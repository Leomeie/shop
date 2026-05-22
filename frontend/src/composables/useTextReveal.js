import { onMounted, onUnmounted, nextTick } from 'vue'
import { gsap } from './useGsap.js'
import { SplitText } from 'gsap/SplitText'
import { useIsMobile } from './useGsap.js'

export function useTextReveal(elementRef, options = {}) {
  const {
    type = 'words',
    y = 30,
    stagger = 0.03,
    duration = 0.5,
    ease = 'power3.out',
    scrollTrigger = true,
    start = 'top 85%',
    once = true,
  } = options

  const isMobile = useIsMobile()
  let ctx = null
  let splitInstance = null

  function setup() {
    const el = elementRef?.value?.$el || elementRef?.value
    if (!el) return

    ctx = gsap.context(() => {
      const splitType = isMobile.value ? 'lines' : type
      splitInstance = new SplitText(el, { type: splitType })
      const targets = splitInstance[splitType] || splitInstance.words || splitInstance.chars

      gsap.set(targets, { opacity: 0, y })

      const stConfig = scrollTrigger
        ? { trigger: el, start, once }
        : false

      gsap.to(targets, {
        opacity: 1,
        y: 0,
        duration,
        ease,
        stagger: isMobile.value ? 0.02 : stagger,
        scrollTrigger: stConfig,
      })
    }, el)
  }

  function cleanup() {
    splitInstance?.revert()
    splitInstance = null
    ctx?.revert()
    ctx = null
  }

  onMounted(() => nextTick(setup))
  onUnmounted(cleanup)

  return { cleanup }
}
