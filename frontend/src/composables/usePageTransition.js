import { gsap, ScrollToPlugin, ScrollTrigger } from './useGsap.js'

export function usePageTransition() {
  function onLeave(el, done) {
    gsap.to(el, {
      opacity: 0,
      y: -8,
      duration: 0.18,
      ease: 'power2.in',
      onComplete: done,
    })
  }

  function onEnter(el, done) {
    gsap.fromTo(el,
      { opacity: 0, y: 16 },
      {
        opacity: 1,
        y: 0,
        duration: 0.35,
        ease: 'power3.out',
        onComplete() {
          ScrollTrigger.refresh()
          done()
        },
      }
    )
  }

  function scrollToTop() {
    gsap.to(window, {
      scrollTo: { y: 0 },
      duration: 0.4,
      ease: 'power2.out',
    })
  }

  return { onLeave, onEnter, scrollToTop }
}
