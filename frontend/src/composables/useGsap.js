import { ref, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import { ScrollToPlugin } from 'gsap/ScrollToPlugin'

gsap.registerPlugin(ScrollTrigger, ScrollToPlugin)

export { gsap, ScrollTrigger, ScrollToPlugin }

export const defaults = {
  ease: 'power3.out',
  duration: 0.6,
  stagger: 0.08,
  mobileStagger: 0.04,
  mobileDuration: 0.4,
  mobileY: 20,
}

const _isMobile = ref(false)
const _reducedMotion = ref(false)

export function useReducedMotion() {
  onMounted(() => {
    const mq = window.matchMedia('(prefers-reduced-motion: reduce)')
    _reducedMotion.value = mq.matches
    const handler = (e) => { _reducedMotion.value = e.matches }
    mq.addEventListener('change', handler)
    onUnmounted(() => mq.removeEventListener('change', handler))
  })
  return _reducedMotion
}

export function useIsMobile() {
  onMounted(() => {
    const mq = window.matchMedia('(max-width: 768px)')
    _isMobile.value = mq.matches
    const handler = (e) => { _isMobile.value = e.matches }
    mq.addEventListener('change', handler)
    onUnmounted(() => mq.removeEventListener('change', handler))
  })
  return _isMobile
}

export function useGsapDefaults() {
  const isMobile = useIsMobile()
  const reducedMotion = useReducedMotion()
  return {
    get ease() { return reducedMotion.value ? 'none' : defaults.ease },
    get duration() { return reducedMotion.value ? 0 : (isMobile.value ? defaults.mobileDuration : defaults.duration) },
    get stagger() { return reducedMotion.value ? 0 : (isMobile.value ? defaults.mobileStagger : defaults.stagger) },
    get y() { return reducedMotion.value ? 0 : (isMobile.value ? defaults.mobileY : 40) },
  }
}
