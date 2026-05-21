const assert = require('node:assert/strict')
const { chromium } = require('playwright')

async function main() {
  const browser = await chromium.launch({ headless: true })
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } })

  try {
    await page.goto('http://127.0.0.1:5173/', { waitUntil: 'domcontentloaded' })
    await page.waitForSelector('.video-auth .auth-btn, .slide-video-bg, .hero-video-bg', { timeout: 15000 })

    const metrics = await page.evaluate(() => ({
      hasVideo: Boolean(document.querySelector('.slide-video-bg, .hero-video-bg')),
      authButtonCount: document.querySelectorAll('.video-auth .auth-btn').length,
      scrollHeight: document.documentElement.scrollHeight,
      viewportHeight: window.innerHeight,
      initialScrollY: window.scrollY,
      navVisible:
        (() => {
          const header = document.querySelector('header.nav')
          if (!header) return false
          const style = window.getComputedStyle(header)
          return style.opacity !== '0' && style.visibility !== 'hidden' && style.pointerEvents !== 'none'
        })(),
      firstSectionBottom: document.querySelector('.home > section')?.getBoundingClientRect().bottom ?? 0,
      rootScrollSnapType: getComputedStyle(document.documentElement).scrollSnapType,
      screenSnapStop: getComputedStyle(document.querySelector('.screen')).scrollSnapStop,
    }))

    assert.equal(metrics.hasVideo, true, 'The first screen should keep a full-screen hero video.')
    assert.equal(metrics.authButtonCount, 2, 'The first screen should keep the CTA button group.')
    assert.ok(
      metrics.scrollHeight > metrics.viewportHeight * 3.6,
      `Homepage should contain four full-screen sections. Expected scrollHeight > ${metrics.viewportHeight * 3.6}, received ${metrics.scrollHeight}.`,
    )
    assert.equal(metrics.navVisible, false, 'The first screen should hide the global navigation.')
    assert.ok(
      metrics.firstSectionBottom >= metrics.viewportHeight - 1,
      `The first screen should fully cover the viewport without exposing the next section. Received bottom=${metrics.firstSectionBottom}.`,
    )
    assert.notEqual(
      metrics.rootScrollSnapType,
      'y mandatory',
      `Homepage should avoid mandatory scroll snapping because it feels choppy. Received "${metrics.rootScrollSnapType}".`,
    )
    assert.equal(
      metrics.screenSnapStop,
      'normal',
      `Homepage screens should not force snap-stop on every wheel gesture. Received "${metrics.screenSnapStop}".`,
    )

    await page.mouse.wheel(0, 1200)
    await page.waitForTimeout(900)

    const afterFirstScroll = await page.evaluate(() => ({
      scrollY: window.scrollY,
      brandHeading: Array.from(document.querySelectorAll('h1, h2, h3')).find((el) =>
        /发现最好的AI工具与模板/.test((el.textContent || '').replace(/\s+/g, '')),
      )?.textContent?.replace(/\s+/g, '') ?? null,
      navVisible:
        (() => {
          const header = document.querySelector('header.nav')
          if (!header) return false
          const style = window.getComputedStyle(header)
          return style.opacity !== '0' && style.visibility !== 'hidden' && style.pointerEvents !== 'none'
        })(),
    }))

    assert.ok(
      afterFirstScroll.scrollY > metrics.viewportHeight * 0.45,
      `Scrolling down from the first screen should move the document toward the second screen. Received scrollY=${afterFirstScroll.scrollY}.`,
    )
    assert.equal(afterFirstScroll.navVisible, true, 'The navigation should appear from the second screen onward.')
    assert.ok(afterFirstScroll.brandHeading, 'After the first scroll, the second screen brand hero should be active.')

    await page.mouse.wheel(0, 1200)
    await page.waitForTimeout(900)

    const afterSecondScroll = await page.evaluate(() => ({
      scrollY: window.scrollY,
      sectionHeading:
        Array.from(document.querySelectorAll('h1, h2, h3')).find((el) =>
          /为创作者设计的交付系统/.test((el.textContent || '').replace(/\s+/g, '')),
        )?.textContent?.replace(/\s+/g, '') ?? null,
    }))

    assert.ok(
      afterSecondScroll.scrollY > metrics.viewportHeight * 1.2,
      `After the second scroll, the page should enter the third screen. Received scrollY=${afterSecondScroll.scrollY}.`,
    )
    assert.ok(afterSecondScroll.sectionHeading, 'The third screen should be the creator-system section.')

    await page.mouse.wheel(0, 1200)
    await page.waitForTimeout(900)

    const afterThirdScroll = await page.evaluate(() => ({
      scrollY: window.scrollY,
      sectionHeading:
        Array.from(document.querySelectorAll('h1, h2, h3')).find((el) =>
          /直接进入高价值资源/.test((el.textContent || '').replace(/\s+/g, '')),
        )?.textContent?.replace(/\s+/g, '') ?? null,
    }))

    assert.ok(
      afterThirdScroll.scrollY > metrics.viewportHeight * 2.1,
      `After the third scroll, the page should enter the fourth screen. Received scrollY=${afterThirdScroll.scrollY}.`,
    )
    assert.ok(afterThirdScroll.sectionHeading, 'The fourth screen should be the curated-collections section.')
  } finally {
    await browser.close()
  }
}

main().catch((error) => {
  console.error(error.stack || error)
  process.exit(1)
})
