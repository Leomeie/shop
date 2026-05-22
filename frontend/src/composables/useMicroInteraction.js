import { gsap } from './useGsap.js'

export function useMicroInteraction() {
  function pulseButton(el) {
    if (!el) return
    gsap.fromTo(el,
      { scale: 1 },
      { scale: 0.95, duration: 0.1, ease: 'power2.in', yoyo: true, repeat: 1 }
    )
  }

  function bounceBadge(el) {
    if (!el) return
    gsap.fromTo(el,
      { scale: 0.5, rotation: -10 },
      { scale: 1, rotation: 0, duration: 0.4, ease: 'back.out(2)' }
    )
  }

  function slideInItem(el, onComplete) {
    if (!el) return
    gsap.fromTo(el,
      { opacity: 0, x: -20, height: 0 },
      {
        opacity: 1, x: 0, height: 'auto',
        duration: 0.35, ease: 'power3.out',
        onComplete,
      }
    )
  }

  function slideOutItem(el, onComplete) {
    if (!el) return
    gsap.to(el, {
      opacity: 0, x: 20, height: 0, paddingTop: 0, paddingBottom: 0, marginBottom: 0,
      duration: 0.3, ease: 'power2.in',
      onComplete,
    })
  }

  function numberTick(el, from, to, duration = 0.6) {
    if (!el) return
    const obj = { val: from }
    gsap.to(obj, {
      val: to,
      duration,
      ease: 'power2.out',
      onUpdate() {
        el.textContent = Math.round(obj.val)
      },
    })
  }

  return { pulseButton, bounceBadge, slideInItem, slideOutItem, numberTick }
}
