# PRD: 测试覆盖体系建设

## Introduction

ShopEase 当前零测试覆盖。所有 `tests.py` 文件为空（仅有 migration 文件），前端无任何测试配置。作为电商项目，缺少测试意味着每次修改都有回归风险。本 PRD 建立后端 pytest + 前端 Vitest 的完整测试体系，覆盖核心业务流程。

## Goals

- 后端核心业务逻辑测试覆盖率达到 70%+
- 前端关键组件和 store 有基本测试覆盖
- 建立 CI 可运行的测试套件
- 购物车→下单→支付 完整流程有集成测试

## User Stories

### US-001: 后端测试基础设施搭建
**Description:** 作为开发者，我需要搭建 pytest + DRF 测试基础设施，以便后续编写测试用例。

**Acceptance Criteria:**
- [ ] 安装 pytest、pytest-django、pytest-factoryboy、pytest-cov
- [ ] 创建 `shop_api/pytest.ini` 或 `pyproject.toml` 配置 pytest
- [ ] 创建 `conftest.py` 提供通用 fixtures（authenticated client、test user、test product）
- [ ] `pytest` 命令可正常运行并输出覆盖率报告
- [ ] 至少有一个 smoke test 通过

### US-002: 用户模块测试
**Description:** 作为开发者，我需要测试注册、登录、JWT 认证流程。

**Acceptance Criteria:**
- [ ] 注册：成功注册、重复邮箱、密码过短、缺少必填字段
- [ ] 登录：成功登录、错误密码、不存在的用户
- [ ] JWT：access token 过期后用 refresh token 刷新、无效 token 拒绝
- [ ] 游客可以浏览商品，未登录不能下单
- [ ] 所有测试通过

### US-003: 商品模块测试
**Description:** 作为开发者，我需要测试商品 CRUD、分类、SKU 管理。

**Acceptance Criteria:**
- [ ] 商品列表分页、按分类筛选、搜索（如有）
- [ ] 商品详情返回正确数据结构
- [ ] 管理员可以创建/编辑/上下架商品
- [ ] 非管理员不能执行管理操作
- [ ] SKU 价格和库存正确
- [ ] 所有测试通过

### US-004: 购物车模块测试
**Description:** 作为开发者，我需要测试购物车的完整操作。

**Acceptance Criteria:**
- [ ] 添加商品到购物车（同 SKU 不重复添加，增加数量）
- [ ] 修改购物车商品数量
- [ ] 删除购物车商品
- [ ] 全选/取消全选
- [ ] 未登录不能操作购物车
- [ ] 库存不足时给出明确错误
- [ ] 所有测试通过

### US-005: 订单流程集成测试
**Description:** 作为开发者，我需要测试从购物车到下单到支付的完整流程。

**Acceptance Criteria:**
- [ ] 从购物车创建订单（正确扣减库存、生成订单号）
- [ ] 创建支付（Mock 模式）并完成支付
- [ ] 支付完成后订单状态正确变更
- [ ] 库存不足时下单失败并回滚
- [ ] 并发下单的库存一致性（race condition）
- [ ] 所有测试通过

### US-006: 优惠券模块测试
**Description:** 作为开发者，我需要测试优惠券领取、使用、过期逻辑。

**Acceptance Criteria:**
- [ ] 领取优惠券（未过期、未领完）
- [ ] 不能重复领取已领的优惠券
- [ ] 下单时使用优惠券（满减/折扣/固定金额）
- [ ] 过期优惠券不能使用
- [ ] 已使用的优惠券不能重复使用
- [ ] 所有测试通过

### US-007: 前端测试基础设施搭建
**Description:** 作为前端开发者，我需要搭建 Vitest + Vue Test Utils 测试环境。

**Acceptance Criteria:**
- [ ] 安装 vitest、@vue/test-utils、jsdom
- [ ] 配置 vite.config.js 支持 vitest
- [ ] 创建 `setupTests.js` 配置全局 mock
- [ ] `npm run test` 可正常运行
- [ ] 至少有一个组件 smoke test 通过

### US-008: 前端 Store 测试
**Description:** 作为前端开发者，我需要测试 Pinia store 的业务逻辑。

**Acceptance Criteria:**
- [ ] cartStore：addToCart、removeItem、updateQty、clearCart
- [ ] userStore：login、logout、getToken、isAuthenticated
- [ ] API 调用使用 mock，验证调用参数和状态变更
- [ ] 所有测试通过

### US-009: 前端组件快照测试
**Description:** 作为前端开发者，我需要对关键组件做快照测试，防止意外 UI 回归。

**Acceptance Criteria:**
- [ ] ProductCard 组件快照测试
- [ ] StatusBadge 组件快照测试
- [ ] StorePageHeader 组件快照测试
- [ ] 快照更新有明确 diff

## Functional Requirements

- FR-1: 后端使用 pytest 作为测试框架，pytest-django 管理 Django 上下文
- FR-2: 使用 pytest-factoryboy 生成测试数据（User、Product、SKU、Order 等 factories）
- FR-3: 测试数据库使用 SQLite 内存数据库，不依赖外部 MySQL
- FR-4: 前端使用 Vitest 作为测试框架，jsdom 模拟浏览器环境
- FR-5: API 测试使用 DRF 的 APIClient，模拟真实 HTTP 请求
- FR-6: 集成测试覆盖 购物车→下单→支付 完整链路
- FR-7: 测试覆盖率报告输出到 `htmlcov/` 目录

## Non-Goals

- 不做端到端测试（E2E，如 Cypress/Playwright）
- 不做性能测试/压力测试
- 不做视觉回归测试（如 Percy/Chromatic）
- 不要求 100% 覆盖率（目标 70%+ 核心逻辑）

## Technical Considerations

- 测试数据库使用 SQLite 而非 MySQL，避免依赖外部服务
- pytest-factoryboy 生成测试数据，减少 fixture 维护成本
- Mock 支付使用现有的 MockPaymentBackend
- 前端 API 调用使用 vi.mock() mock axios

## Success Metrics

- `pytest --cov` 核心模块覆盖率达到 70%
- `npm run test` 前端测试全部通过
- CI 中 pytest 和 vitest 均可运行
- 购物车→支付 完整流程有至少 1 个端到端集成测试

## Open Questions

- 是否需要为缓存模块（cache/）编写测试？
- 是否需要数据库 migration 的测试？
- 前端是否需要 router guard 的测试？
