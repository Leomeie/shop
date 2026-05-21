const assert = require('node:assert/strict')
const { chromium } = require('playwright')

const sampleProducts = {
  count: 2,
  results: [
    {
      id: 1,
      name: 'Prompt Bundle Pro',
      category_name: 'Prompt',
      min_price_yuan: 99,
      download_count: 321,
      main_image: 'https://example.com/cover-1.jpg',
      description: '精选高转化提示词集合',
      status: 'active',
      created_at: '2026-05-15 10:00',
    },
    {
      id: 2,
      name: 'ComfyUI Workflow Kit',
      category_name: 'Workflow',
      min_price_yuan: 129,
      download_count: 112,
      main_image: 'https://example.com/cover-2.jpg',
      description: '用于复杂出图工作流的资源包',
      status: 'active',
      created_at: '2026-05-15 11:00',
    },
  ],
}

const sampleCart = {
  items: [
    {
      sku_id: 101,
      selected: true,
      image: 'https://example.com/cart-1.jpg',
      product_name: 'Prompt Bundle Pro',
      sku_name: '商业授权',
      price_yuan: 99,
      quantity: 1,
      subtotal_yuan: 99,
    },
  ],
}

const sampleDownloads = {
  count: 1,
  results: [
    {
      id: 8,
      order_no: 'SO20260515001',
      created_at: '2026-05-15 12:00',
      items: [{ id: 1, product_name: 'Prompt Bundle Pro', sku_name: '商业授权' }],
    },
  ],
}

const sampleAdminUser = {
  id: 1,
  username: 'admin',
  nickname: '',
  phone: '13800000000',
  email: 'admin@example.com',
  date_joined: '2026-05-08 22:12:38',
  is_staff: true,
  is_superuser: true,
  is_active: true,
}

const sampleAdminUsers = {
  count: 2,
  results: [
    sampleAdminUser,
    {
      id: 2,
      username: 'creator_user',
      nickname: '创作者 A',
      phone: '13900000000',
      email: 'creator@example.com',
      date_joined: '2026-05-10 08:30:00',
      is_staff: false,
      is_superuser: false,
      is_active: true,
    },
  ],
}

const sampleAdminOrderList = {
  count: 1,
  results: [
    {
      id: 1,
      order_no: 'SO20260515001',
      status: 'completed',
      status_display: '已完成',
      pay_amount_yuan: 99,
      total_amount_yuan: 99,
      discount_amount_yuan: 0,
      remark: '测试订单',
      created_at: '2026-05-15 10:00',
      items: [{ id: 1, product_name: 'Prompt Bundle Pro', sku_name: '商业授权', price_yuan: 99 }],
      user: { id: 2, username: 'creator_user', nickname: '创作者 A' },
    },
  ],
}

const sampleAdminOrderDetail = {
  ...sampleAdminOrderList.results[0],
  pay_time: '2026-05-15 10:05',
  complete_time: '2026-05-15 10:06',
}

const sampleAdminProductDetail = {
  id: 1,
  name: 'Prompt Bundle Pro',
  category: 1,
  category_name: 'Prompt',
  description: '用于营销文案、角色设定与图像生成的精选模板合集。',
  main_image: 'https://example.com/cover-1.jpg',
  file: 'https://example.com/file.zip',
  demo_file: 'https://example.com/demo.pdf',
  version: '1.2.0',
  changelog: '新增商业授权模板',
  status: 'active',
  is_featured: true,
  download_count: 321,
  images: [{ id: 11, image: 'https://example.com/detail-1.jpg', sort_order: 1 }],
  skus_data: [
    {
      id: 201,
      name: '商业授权',
      price_yuan: 99,
      original_price_yuan: 129,
      license_description: '适合商业项目使用',
      sort_order: 0,
      is_active: true,
    },
  ],
}

async function mockApi(page) {
  await page.route('**/api/v1/**', async (route) => {
    const url = route.request().url()
    const method = route.request().method()

    const json = (body) =>
      route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(body),
      })

    if (url.includes('/api/v1/products/') && !url.includes('/admin/') && !url.includes('/categories/') && method === 'GET') {
      return json({ code: 0, message: 'ok', data: sampleProducts })
    }

    if (url.endsWith('/api/v1/products/categories/') && method === 'GET') {
      return json({
        code: 0,
        message: 'ok',
        data: [{ id: 1, name: 'Prompt', product_count: 12, description: 'Prompt 分类' }],
      })
    }

    if (url.endsWith('/api/v1/cart/') && method === 'GET') {
      return json({ code: 0, message: 'ok', data: sampleCart })
    }

    if (url.endsWith('/api/v1/orders/downloads/') && method === 'GET') {
      return json({ code: 0, message: 'ok', data: sampleDownloads })
    }

    if (url.endsWith('/api/v1/auth/me/') && method === 'GET') {
      return json({ code: 0, message: 'ok', data: sampleAdminUser })
    }

    if (/\/api\/v1\/admin\/users\/\d+\/$/.test(url) && method === 'GET') {
      const id = Number(url.match(/\/admin\/users\/(\d+)\//)?.[1] || 1)
      const user = sampleAdminUsers.results.find((item) => item.id === id) || sampleAdminUsers.results[0]
      return json({ code: 0, message: 'ok', data: user })
    }

    if (/\/api\/v1\/admin\/orders\/\d+\/$/.test(url) && method === 'GET') {
      return json({ code: 0, message: 'ok', data: sampleAdminOrderDetail })
    }

    if (url.includes('/api/v1/admin/users/') && method === 'GET') {
      return json({ code: 0, message: 'ok', data: sampleAdminUsers })
    }

    if (url.includes('/api/v1/admin/orders/') && method === 'GET') {
      return json({ code: 0, message: 'ok', data: sampleAdminOrderList })
    }

    if (url.endsWith('/api/v1/auth/login/') && method === 'POST') {
      const body = route.request().postDataJSON()
      if (body.username === 'admin' && body.password === 'admin123') {
        return json({
          code: 0,
          message: 'ok',
          data: {
            user: sampleAdminUser,
            access: 'mock-access',
            refresh: 'mock-refresh',
          },
        })
      }

      return route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({
          code: 400,
          message: '用户名或密码错误，请检查后重试',
          errors: { non_field_errors: ['用户名或密码错误，请检查后重试'] },
        }),
      })
    }

    if (url.endsWith('/api/v1/auth/register/') && method === 'POST') {
      const body = route.request().postDataJSON()
      if (body.username === 'existing_user') {
        return route.fulfill({
          status: 400,
          contentType: 'application/json',
          body: JSON.stringify({
            code: 400,
            message: '该用户名已存在，请更换一个新的用户名',
            errors: { username: ['该用户名已存在，请更换一个新的用户名'] },
          }),
        })
      }

      return json({
        code: 201,
        message: 'ok',
        data: {
          user: { ...sampleAdminUser, username: body.username, is_staff: false, is_superuser: false },
          access: 'mock-access',
          refresh: 'mock-refresh',
        },
      })
    }

    if (url.includes('/api/v1/products/admin/') && method === 'GET') {
      if (/\/api\/v1\/products\/admin\/\d+\/$/.test(url)) {
        return json({ code: 0, message: 'ok', data: sampleAdminProductDetail })
      }
      return json({
        code: 0,
        message: 'ok',
        data: {
          count: 1,
          results: [
            {
              id: 1,
              name: 'Prompt Bundle Pro',
              category_name: 'Prompt',
              status: 'active',
              download_count: 321,
              created_at: '2026-05-15 10:00',
            },
          ],
        },
      })
    }

    if (url.endsWith('/api/v1/products/admin/categories/') && method === 'GET') {
      return json({
        code: 0,
        message: 'ok',
        data: [{ id: 1, name: 'Prompt', parent: null, level: 1, icon: '' }],
      })
    }

    if (url.includes('/api/v1/orders/') && method === 'GET') {
      return json({
        code: 0,
        message: 'ok',
        data: {
          count: 1,
          results: [
            {
              id: 1,
              order_no: 'SO20260515001',
              status: 'completed',
              status_display: '已完成',
              pay_amount_yuan: 99,
              created_at: '2026-05-15 10:00',
              items: [{ id: 1, product_name: 'Prompt Bundle Pro', sku_name: '商业授权' }],
            },
          ],
        },
      })
    }

    return json({ code: 0, message: 'ok', data: {} })
  })
}

async function main() {
  const browser = await chromium.launch({ headless: true })
  const page = await browser.newPage({ viewport: { width: 1440, height: 960 } })

  try {
    await mockApi(page)

    await page.goto('http://127.0.0.1:5173/products', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(1000)

    const catalogPage = await page.evaluate(() => ({
      hasCatalogShell: Boolean(document.querySelector('.catalog-shell')),
      hasFacetSidebar: Boolean(document.querySelector('.facet-sidebar')),
      hasResultsToolbar: Boolean(document.querySelector('.results-toolbar')),
      hasLegacyHero: Boolean(document.querySelector('.page-hero')),
      productCards: document.querySelectorAll('.product-grid .card, .product-grid .grid-item').length,
    }))

    assert.equal(catalogPage.hasCatalogShell, true, 'Product list should use the new catalog shell.')
    assert.equal(catalogPage.hasFacetSidebar, true, 'Product list should include a desktop facet sidebar.')
    assert.equal(catalogPage.hasResultsToolbar, true, 'Product list should expose a dedicated results toolbar.')
    assert.equal(catalogPage.hasLegacyHero, false, 'Product list should not reuse the legacy full hero banner.')
    assert.ok(catalogPage.productCards >= 2, 'Product list should render mocked product results.')

    await page.goto('http://127.0.0.1:5173/login', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(500)
    await page.getByRole('button', { name: '登录' }).click()
    await page.waitForTimeout(200)
    const loginValidation = await page.evaluate(() => ({
      usernameError: document.querySelector('.field-error')?.textContent?.trim() ?? '',
    }))
    assert.ok(loginValidation.usernameError.includes('请输入用户名'), 'Login page should expose field-level validation before submit.')

    await page.getByPlaceholder('输入用户名').fill('admin')
    await page.getByPlaceholder('输入密码').fill('wrong-password')
    await page.getByRole('button', { name: '登录' }).click()
    await page.waitForTimeout(400)
    const loginFailure = await page.evaluate(() => ({
      hasAlert: Boolean(document.querySelector('.form-alert')),
      alertText: document.querySelector('.form-alert')?.textContent ?? '',
    }))
    assert.equal(loginFailure.hasAlert, true, 'Login page should render a detailed error alert on API failure.')
    assert.ok(loginFailure.alertText.includes('用户名或密码错误'), 'Login error alert should contain backend failure details.')
    assert.ok(loginFailure.alertText.includes('管理员请使用用户名登录'), 'Login error alert should include administrator guidance.')

    await page.goto('http://127.0.0.1:5173/register', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(500)
    await page.getByPlaceholder('输入用户名').fill('bad user')
    await page.getByPlaceholder('至少 6 位密码').fill('123456')
    await page.getByPlaceholder('再次输入密码').fill('654321')
    await page.getByRole('button', { name: '创建账户' }).click()
    await page.waitForTimeout(300)
    const registerValidation = await page.evaluate(() => ({
      errors: Array.from(document.querySelectorAll('.field-error')).map((el) => el.textContent?.trim()),
      alertText: document.querySelector('.form-alert')?.textContent ?? '',
    }))
    assert.ok(registerValidation.errors.some((text) => text.includes('用户名只能包含字母、数字或下划线')), 'Register page should validate username format.')
    assert.ok(registerValidation.errors.some((text) => text.includes('两次输入的密码不一致')), 'Register page should validate password confirmation.')

    await page.evaluate(() => {
      localStorage.setItem('token', 'mock-token')
      localStorage.setItem('refresh_token', 'mock-refresh')
    })
    await page.goto('http://127.0.0.1:5173/cart', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(1000)

    const cartPage = await page.evaluate(() => ({
      hasTransactionShell: Boolean(document.querySelector('.transaction-shell')),
      hasSummaryRail: Boolean(document.querySelector('.summary-rail')),
      hasLegacyHero: Boolean(document.querySelector('.page-hero')),
    }))

    assert.equal(cartPage.hasTransactionShell, true, 'Cart should use the new transaction shell.')
    assert.equal(cartPage.hasSummaryRail, true, 'Cart should render the shared summary rail.')
    assert.equal(cartPage.hasLegacyHero, false, 'Cart should not use the legacy hero header.')

    await page.goto('http://127.0.0.1:5173/admin/products', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(1200)

    const adminPage = await page.evaluate(() => ({
      hasWorkbenchPage: Boolean(document.querySelector('.workbench-page')),
      hasWorkbenchFilters: Boolean(document.querySelector('.workbench-filters')),
      hasTablePanel: Boolean(document.querySelector('.table-panel')),
      hasAdminLayoutShell: Boolean(document.querySelector('.admin-shell')),
    }))

    assert.equal(adminPage.hasAdminLayoutShell, true, 'Admin should use the new admin shell.')
    assert.equal(adminPage.hasWorkbenchPage, true, 'Admin list pages should use the new workbench page scaffold.')
    assert.equal(adminPage.hasWorkbenchFilters, true, 'Admin list pages should include the shared filter console.')
    assert.equal(adminPage.hasTablePanel, true, 'Admin list pages should render inside the shared table panel.')

    await page.locator('.clickable-row').first().click()
    await page.waitForTimeout(500)
    const drawerState = await page.evaluate(() => ({
      hasDrawer: Boolean(document.querySelector('.drawer-content')),
      drawerTitle: document.querySelector('.drawer-top h3')?.textContent?.trim() ?? '',
    }))
    assert.equal(drawerState.hasDrawer, true, 'Admin product list should expose a detail drawer.')
    assert.equal(drawerState.drawerTitle, 'Prompt Bundle Pro', 'Detail drawer should render the selected product detail.')

    await page.getByRole('button', { name: '前往编辑' }).click()
    await page.waitForTimeout(600)
    const editorState = await page.evaluate(() => ({
      hasEditorPage: Boolean(document.querySelector('.editor-page')),
      hasEditorNav: Boolean(document.querySelector('.editor-nav')),
      title: document.querySelector('.editor-title')?.textContent?.trim() ?? '',
    }))
    assert.equal(editorState.hasEditorPage, true, 'Admin should navigate to the new product editor page.')
    assert.equal(editorState.hasEditorNav, true, 'Product editor should include left-side section navigation.')
    assert.equal(editorState.title, 'Prompt Bundle Pro', 'Product editor should load the selected product data.')

    await page.goto('http://127.0.0.1:5173/admin/orders', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(800)
    await page.locator('.clickable-row').first().click()
    await page.waitForTimeout(500)
    const orderDrawer = await page.evaluate(() => ({
      hasDrawer: Boolean(document.querySelector('.drawer-content')),
      title: document.querySelector('.drawer-top h3')?.textContent?.trim() ?? '',
    }))
    assert.equal(orderDrawer.hasDrawer, true, 'Admin order page should expose a detail drawer.')
    assert.equal(orderDrawer.title, 'SO20260515001', 'Order drawer should display the selected order number.')

    await page.goto('http://127.0.0.1:5173/admin/users', { waitUntil: 'domcontentloaded' })
    await page.waitForTimeout(800)
    await page.locator('.clickable-row').nth(1).click()
    await page.waitForTimeout(500)
    const userDrawer = await page.evaluate(() => ({
      hasDrawer: Boolean(document.querySelector('.drawer-content')),
      title: document.querySelector('.drawer-top h3')?.textContent?.trim() ?? '',
    }))
    assert.equal(userDrawer.hasDrawer, true, 'Admin user page should expose a detail drawer.')
    assert.equal(userDrawer.title, 'creator_user', 'User drawer should display the selected username.')
  } finally {
    await browser.close()
  }
}

main().catch((error) => {
  console.error(error.stack || error)
  process.exit(1)
})
