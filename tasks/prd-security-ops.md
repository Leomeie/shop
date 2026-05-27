# PRD: 安全加固与运维基础设施

## Introduction

基于代码审查，ShopEase 缺少多项安全和运维基础设施：无 API 限流、无 API 文档、日志体系不完善、无健康检查。这些是上线前的必要加固。

## Goals

- API 限流防刷
- 自动生成 API 文档（Swagger/OpenAPI）
- 完善日志体系
- 添加健康检查端点

## User Stories

### US-001: API 限流（Throttling）
**Description:** 作为运维人员，我需要限制 API 请求频率，防止恶意刷接口。

**Acceptance Criteria:**
- [ ] 在 `REST_FRAMEWORK` 配置中添加 `DEFAULT_THROTTLE_CLASSES`
- [ ] 未认证用户：20 次/分钟
- [ ] 已认证用户：60 次/分钟
- [ ] 支付相关接口：10 次/分钟（更严格）
- [ ] 限流返回 429 状态码和友好提示
- [ ] 所有测试通过

### US-002: API 文档自动生成
**Description:** 作为前端开发者，我需要自动生成的 API 文档，方便对接。

**Acceptance Criteria:**
- [ ] 安装 `drf-spectacular`（OpenAPI 3.0）
- [ ] 配置 `DEFAULT_SCHEMA_CLASS` 为 `drf-spectacular.openapi.AutoSchema`
- [ ] API 文档页面可通过 `/api/docs/` 访问
- [ ] Schema JSON 可通过 `/api/schema/` 获取
- [ ] 所有序列化器有 `description` 和 `help_text`
- [ ] 所有 View 有 `summary` 和 `description`

### US-003: 结构化日志
**Description:** 作为运维人员，我需要结构化的日志输出，便于排查问题。

**Acceptance Criteria:**
- [ ] 创建 `shop_api/config/logging.py` 配置日志格式
- [ ] 日志格式包含：时间戳、级别、模块名、消息
- [ ] 生产环境输出 JSON 格式日志
- [ ] 开发环境输出彩色可读日志
- [ ] 所有 view 和 service 添加关键操作日志
- [ ] 支付回调必须记录完整请求/响应

### US-004: 健康检查端点
**Description:** 作为运维人员，我需要健康检查端点用于监控和负载均衡。

**Acceptance Criteria:**
- [ ] 创建 `/api/health/` 端点
- [ ] 检查数据库连接
- [ ] 检查缓存连接
- [ ] 返回状态：{ status: "ok"|"error", db: "ok"|"error", cache: "ok"|"error" }
- [ ] 健康时返回 200，异常时返回 503
- [ ] 不需要认证

### US-005: 登录失败锁定
**Description:** 作为安全人员，我需要限制登录失败次数，防止暴力破解。

**Acceptance Criteria:**
- [ ] 同一邮箱连续 5 次登录失败后锁定 15 分钟
- [ ] 锁定期间返回"账号已锁定，请稍后再试"
- [ ] 成功登录重置失败计数
- [ ] 锁定信息存储在缓存中（利用现有缓存系统）
- [ ] 所有测试通过

## Functional Requirements

- FR-1: Throttling 使用 DRF 内置的 AnonRateThrottle 和 UserRateThrottle
- FR-2: drf-spectacular 生成 OpenAPI 3.0 schema
- FR-3: 日志使用 Python 标准 logging 模块
- FR-4: 健康检查端点无需认证，返回简洁状态
- FR-5: 登录锁定基于缓存实现，重启后自动解锁

## Non-Goals

- 不实现 WAF（Web Application Firewall）
- 不实现 IP 黑名单
- 不实现 CAPTCHA 验证码
- 不实现审计日志（所有操作记录）

## Technical Considerations

- DRF throttling 可直接使用内置类，无需额外依赖
- drf-spectacular 比 drf-yasg 更轻量，支持 OpenAPI 3.0
- 日志配置放在单独的 `logging.py`，settings 中引用
- 健康检查端点放在 `config/urls.py` 中，不在任何 app 内

## Success Metrics

- API 限流生效：超过阈值返回 429
- `/api/docs/` 可访问并显示所有端点
- 生产日志为 JSON 格式，可用 ELK 解析
- 健康检查端点 < 100ms 响应

## Open Questions

- 是否需要为管理后台单独设置限流策略？
- 日志是否需要接入外部服务（如 Sentry）？
- API 文档是否需要认证保护？
- 是否需要实现 request ID 追踪？
