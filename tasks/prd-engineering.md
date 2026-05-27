# PRD: 工程化升级

## Introduction

ShopEase 当前缺乏工程化基础设施：没有 TypeScript、没有 CI/CD、没有容器化、环境变量管理松散。本 PRD 建立现代化工程化体系，提升代码质量、开发效率和部署可靠性。

## Goals

- 前端渐进式迁移 TypeScript
- 建立 GitHub Actions CI/CD 管道
- Docker 化开发和部署环境
- 规范化环境变量管理

## User Stories

### US-001: 前端 TypeScript 渐进迁移 - API 层
**Description:** 作为前端开发者，我希望 API 层有类型定义，减少调用错误。

**Acceptance Criteria:**
- [ ] 安装 TypeScript、@types/node
- [ ] 创建 `tsconfig.json`，allowJs: true 渐进迁移
- [ ] 为 `src/api/*.js` 中每个模块创建对应的 `.d.ts` 类型定义
- [ ] 为 `src/stores/*.js` 中每个 store 创建类型定义
- [ ] `vue-tsc --noEmit` 无类型错误
- [ ] 现有 JavaScript 文件不受影响

### US-002: 前端 TypeScript 渐进迁移 - Store 层
**Description:** 作为前端开发者，我希望 Pinia store 有完整的类型支持。

**Acceptance Criteria:**
- [ ] `cartStore` 定义状态类型（CartItem[]、totalAmount、selectedIds）
- [ ] `userStore` 定义状态类型（token、userInfo、isAuthenticated）
- [ ] Actions 有参数和返回值类型
- [ ] Getters 有返回值类型
- [ ] `vue-tsc --noEmit` 无类型错误

### US-003: GitHub Actions CI 管道
**Description:** 作为开发者，我希望每次 push 和 PR 自动运行测试和 lint。

**Acceptance Criteria:**
- [ ] 创建 `.github/workflows/ci.yml`
- [ ] 后端 jobs：安装依赖 → pytest → 覆盖率报告
- [ ] 前端 jobs：npm ci → npm run test → npm run build
- [ ] 在 PR 上自动运行，结果回显到 PR
- [ ] 覆盖率低于阈值时 fail（阈值可配置）

### US-004: Docker 开发环境
**Description:** 作为开发者，我希望用 `docker-compose up` 一键启动完整开发环境。

**Acceptance Criteria:**
- [ ] 创建 `Dockerfile` (后端 Django)
- [ ] 创建 `frontend/Dockerfile` (前端 Vite dev server)
- [ ] 创建 `docker-compose.yml` 编排：db (MySQL) + backend + frontend
- [ ] `docker-compose up` 后后端在 :8000，前端在 :5173
- [ ] 数据库数据持久化（volume）
- [ ] 热重载正常工作

### US-005: 环境变量规范化
**Description:** 作为开发者，我需要清晰的环境变量文档和模板。

**Acceptance Criteria:**
- [ ] 创建 `.env.example` 列出所有需要的环境变量及说明
- [ ] `.env` 已在 `.gitignore` 中
- [ ] Django settings 统一从环境变量读取敏感配置
- [ ] README 中有环境配置说明

### US-006: Docker 生产部署
**Description:** 作为运维人员，我需要 Docker 用于生产部署。

**Acceptance Criteria:**
- [ ] 生产 Dockerfile 使用多阶段构建（builder + runtime）
- [ ] 使用 gunicorn 作为 WSGI 服务器
- [ ] 静态文件通过 Django collectstatic 收集并挂载
- [ ] `docker-compose.prod.yml` 不含 dev 工具（如 vite dev server）
- [ ] 生产镜像大小 < 500MB

## Functional Requirements

- FR-1: TypeScript 配置 allowJs: true，允许 JS/TS 共存
- FR-2: CI 管道并行运行后端和前端测试
- FR-3: Docker 使用 MySQL 8.0 作为数据库
- FR-4: Docker 网络隔离，只有 backend 暴露 8000 端口
- FR-5: 环境变量通过 `.env` 文件加载，Docker 通过 `env_file` 注入

## Non-Goals

- 不全面重写为 TypeScript（只迁移 API 层和 Store 层）
- 不使用 Kubernetes 或复杂编排
- 不实现自动部署（只实现构建，部署手动触发）
- 不迁移数据库（继续使用 MySQL）

## Technical Considerations

- TypeScript 迁移使用 allowJs 渐进模式，不破坏现有代码
- Docker 使用 `python:3.11-slim` 减小镜像体积
- CI 使用 GitHub Actions 免费额度
- 前端 Docker 使用 `node:20-alpine`

## Success Metrics

- `vue-tsc --noEmit` 无错误
- `docker-compose up` 30 秒内启动完成
- CI 管道 5 分钟内完成
- `.env.example` 覆盖所有必需环境变量

## Open Questions

- 是否需要 Redis 作为缓存后端？（目前用 Django 内存缓存）
- 是否需要 Nginx 反向代理？
- CI 是否需要 lint（ESLint）检查？
- 生产部署用什么云平台？（影响 Dockerfile 细节）
