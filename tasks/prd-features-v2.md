# PRD: 功能补全 v2

## Introduction

基于 Graphify 知识图谱分析和 PRD 对照，ShopEase 有多个已规划但未实现的功能。本 PRD 补全核心缺失功能：微信支付后端、商品搜索、评价系统增强、浏览量统计。

## Goals

- 实现微信支付后端，保持与支付宝一致的策略模式
- 实现商品搜索功能（至少基础全文搜索）
- 增强评价系统（评分、图片评价）
- 实现商品浏览量统计

## User Stories

### US-001: 微信支付后端
**Description:** 作为用户，我希望可以使用微信支付完成购买，这样覆盖更多支付场景。

**Acceptance Criteria:**
- [ ] 创建 `WechatPaymentBackend`，继承 `PaymentBackend` ABC
- [ ] 实现 `create_payment()` 返回微信支付链接/二维码
- [ ] 实现 `verify_notification()` 验证微信支付回调签名
- [ ] 使用策略模式，与 `AlipayPaymentBackend` 保持一致的接口
- [ ] 支持沙箱/测试模式
- [ ] 在 `PaymentBackend` 注册表中添加微信支付选项
- [ ] 所有测试通过

### US-002: 商品搜索 - 后端
**Description:** 作为用户，我希望能通过关键词搜索找到想要的商品。

**Acceptance Criteria:**
- [ ] 创建 `SearchView`，支持 GET `/api/v1/products/search/?q=keyword`
- [ ] 搜索范围：商品名称、描述、分类名称
- [ ] 支持分页（使用 StandardPagination）
- [ ] 搜索结果按相关性排序
- [ ] 空关键词返回空结果（非报错）
- [ ] 性能：1000 商品数据下搜索响应 < 200ms
- [ ] 所有测试通过

### US-003: 商品搜索 - 前端
**Description:** 作为用户，我希望在商品列表页顶部有搜索框，输入关键词即可搜索。

**Acceptance Criteria:**
- [ ] 商品列表页顶部添加搜索输入框
- [ ] 输入防抖（300ms），避免频繁请求
- [ ] 搜索结果高亮关键词
- [ ] 无结果时显示友好提示
- [ ] 搜索状态通过 URL params 保持（刷新不丢失）
- [ ] Verify in browser using dev-browser skill

### US-004: 评价系统增强
**Description:** 作为买家，我希望能对已购买的商品进行带评分和图片的评价。

**Acceptance Criteria:**
- [ ] Review 模型添加 `rating` 字段（1-5 星，默认 5）
- [ ] Review 模型添加 `images` 字段（JSONField，存储图片 URL 列表，最多 5 张）
- [ ] 创建 `ReviewCreateSerializer` 支持 rating 和 images 参数
- [ ] 商品详情页显示平均评分和评分分布
- [ ] 评价列表支持按评分筛选
- [ ] 只能评价已购买且已支付的商品
- [ ] 同一订单项只能评价一次
- [ ] 所有测试通过

### US-005: 商品浏览量统计
**Description:** 作为管理员，我希望能看到每个商品的浏览量，以便了解商品热度。

**Acceptance Criteria:**
- [ ] Product 模型添加 `view_count` 字段（PositiveIntegerField，默认 0）
- [ ] 商品详情 API 返回 `view_count`
- [ ] 每次访问商品详情自动 +1（去重：同一用户/IP 24 小时内只计一次）
- [ ] Admin Dashboard 显示浏览量排行
- [ ] 所有测试通过

## Functional Requirements

- FR-1: 微信支付后端实现 `PaymentBackend` 接口，支持 create_payment 和 verify_notification
- FR-2: 搜索 API 支持关键词搜索商品名称、描述、分类
- FR-3: 搜索结果分页，使用现有 StandardPagination
- FR-4: 评价支持 1-5 星评分和最多 5 张图片
- FR-5: 商品详情返回平均评分
- FR-6: 浏览量自动统计，24 小时去重
- FR-7: 所有新功能需要管理员权限的接口加 IsAdminUser 权限

## Non-Goals

- 不实现微信支付的实际对接（只实现接口和沙箱模式）
- 不实现 Elasticsearch（先用 Django ORM 的 contains/iexact 做基础搜索）
- 不实现评价回复/卖家回复功能
- 不实现实时浏览量 WebSocket 推送

## Technical Considerations

- 微信支付参考 `AlipayPaymentBackend` 的实现模式，使用 `requests` 库
- 搜索使用 Django ORM 的 `Q` 对象组合查询，后续可升级到 Elasticsearch
- 浏览量去重使用 Django cache（已有 MessageCacheService 可复用或使用简单缓存）
- 评价图片上传可以复用现有的文件上传机制（如有）或使用 ImageField

## Success Metrics

- 微信支付后端可通过 Mock 测试
- 搜索功能可在商品列表页使用
- 商品详情页显示评分
- 商品详情页显示浏览量

## Open Questions

- 微信支付需要申请商户号和 API 密钥吗？还是先只做 Mock？
- 搜索是否需要支持拼音搜索？（如搜 "shouji" 能找到 "手机"）
- 评价图片存储在哪里？本地还是 OSS？
- 浏览量统计用 Django cache 还是数据库？（cache 性能好但重启丢失）
