# PRD: 前端体验升级

## Introduction

ShopEase 前端使用 Vue 3 + Element Plus + GSAP 动画，基础体验良好，但存在多个体验痛点：刷新丢失状态、动画散落未封装、API 错误处理不统一。本 PRD 聚焦前端体验提升。

## Goals

- Pinia 状态持久化（刷新不丢失）
- GSAP 动画统一封装
- API 错误处理统一
- 路由过渡动画

## User Stories

### US-001: Pinia Store 持久化
**Description:** 作为用户，我希望刷新页面后购物车和登录状态不丢失。

**Acceptance Criteria:**
- [ ] 安装 `pinia-plugin-persistedstate`
- [ ] `cartStore` 持久化到 localStorage（购物车数据）
- [ ] `userStore` 持久化到 localStorage（token + 用户信息）
- [ ] 刷新页面后购物车商品仍在
- [ ] 刷新页面后登录状态保持
- [ ] 登出时清除 userStore 持久化数据
- [ ] Verify in browser using dev-browser skill

### US-002: 路由过渡动画封装
**Description:** 作为用户，我希望页面切换时有平滑的过渡动画，提升使用体验。

**Acceptance Criteria:**
- [ ] 创建 `<PageTransition>` 包裹组件
- [ ] 使用 Vue 的 `<Transition>` + GSAP 实现页面切换动画
- [ ] 支持淡入淡出 + 轻微位移效果
- [ ] `router-view` 被 `<PageTransition>` 包裹
- [ ] 在 `MainLayout.vue` 和 `AdminLayout.vue` 中使用
- [ ] 用户偏好 reduced-motion 时禁用动画
- [ ] Verify in browser using dev-browser skill

### US-003: API 错误处理统一
**Description:** 作为用户，我希望 API 错误时看到友好的中文提示，而不是原始错误信息。

**Acceptance Criteria:**
- [ ] `request.js` 的拦截器统一处理错误响应
- [ ] 401 错误自动跳转登录页
- [ ] 403 错误显示"无权限"
- [ ] 404 错误显示"资源不存在"
- [ ] 500 错误显示"服务器繁忙"
- [ ] 网络错误显示"网络连接失败"
- [ ] 使用 Element Plus 的 ElMessage 显示错误
- [ ] 所有 API 调用不需要单独处理通用错误
- [ ] Verify in browser using dev-browser skill

### US-004: 购物车数量脉冲动画
**Description:** 作为用户，添加商品到购物车时应有视觉反馈。

**Acceptance Criteria:**
- [ ] 添加商品时购物车图标有脉冲/弹跳动画
- [ ] 购物车数量 badge 变化时有数字滚动效果
- [ ] 动画持续时间 < 300ms，不打断用户操作
- [ ] 使用已有的 `useMicroInteraction` composable
- [ ] Verify in browser using dev-browser skill

### US-005: 商品卡片骨架屏
**Description:** 作为用户，在商品列表加载时应看到骨架屏而非空白。

**Acceptance Criteria:**
- [ ] 商品列表加载时显示骨架屏（灰色占位块）
- [ ] 骨架屏动画为微光效果（shimmer）
- [ ] 数据加载完成后平滑过渡到真实内容
- [ ] 使用 Element Plus 的 `el-skeleton` 组件
- [ ] Verify in browser using dev-browser skill

### US-006: 暗色模式基础支持
**Description:** 作为用户，我希望支持暗色模式，减少夜间使用时的眼睛疲劳。

**Acceptance Criteria:**
- [ ] 使用 CSS 变量（已定义 81 个 vars）支持主题切换
- [ ] 添加暗色模式 CSS 变量集
- [ ] 在 Header 或用户菜单中添加主题切换按钮
- [ ] 主题偏好持久化到 localStorage
- [ ] 跟随系统偏好（`prefers-color-scheme`）
- [ ] 所有页面在暗色模式下可读
- [ ] Verify in browser using dev-browser skill

## Functional Requirements

- FR-1: pinia-plugin-persistedstate 配置 storage 为 localStorage
- FR-2: PageTransition 组件支持 props 控制动画类型（fade/slide）
- FR-3: 错误拦截器统一处理 HTTP 状态码，业务错误从 response.data 读取
- FR-4: 骨架屏仅在首次加载时显示，切换分页时不显示
- FR-5: 暗色模式通过 CSS 类名 `dark` 切换，挂载在 `<html>` 元素上

## Non-Goals

- 不实现完整的主题系统（只做亮/暗两套）
- 不实现动画编排系统（只做页面过渡）
- 不做国际化（i18n）
- 不做响应式布局优化（移动端适配已有）

## Technical Considerations

- CSS 变量已在 `global.css` 中定义 81 个，暗色模式只需覆盖这些变量
- GSAP 已安装（^3.15.0），动画封装不需要额外依赖
- Element Plus 内置暗色模式支持，可参考其文档
- pinia-plugin-persistedstate 对 Pinia 3.x 的兼容性需确认

## Success Metrics

- 刷新页面后购物车和登录状态保持
- 页面切换动画流畅（< 300ms）
- API 错误时用户看到中文友好提示
- 暗色模式切换无闪烁

## Open Questions

- 暗色模式的颜色方案是否需要设计师参与？
- 是否需要为管理后台单独做暗色模式？
- 骨架屏是否需要为不同页面定制样式？
