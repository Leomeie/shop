# 产品需求文档 (PRD)

# ShopEase — AI 数字精品店

---

## 1. 产品概述

### 1.1 产品定位

ShopEase 是一个聚焦 AI 领域的数字精品店，销售高质量的 Prompt 模板、AI 工作流、LoRA 模型、设计素材等数字商品。前端采用 Apple Store/Gumroad 级别的极简设计，后端具备完整的电商能力。

**核心价值：帮 AI 创作者高效变现，帮 AI 用户找到靠谱的数字工具。**

### 1.2 目标用户

| 角色 | 描述 |
|------|------|
| **买家** | AI 从业者、设计师、开发者、内容创作者，需要高质量 prompt/工作流/模型 |
| **卖家/管理员** | AI 创作者、店铺运营者，需要上传商品、管理订单、查看数据 |

### 1.3 核心价值主张

- **买家**: 浏览 → 预览 → 购买 → 下载，4步完成，零摩擦
- **卖家**: 上传文件即可上架，自动处理支付和分发

### 1.4 品类规划

| 品类 | 示例 | SKU 结构 |
|------|------|---------|
| Prompt 模板 | 营销文案 prompt、代码生成 prompt、设计 prompt | 个人版/商用版 |
| AI 工作流 | ComfyUI 节点包、n8n 自动化模板、Dify 应用 | 基础版/专业版 |
| AI 模型 | LoRA 模型、风格预设、embedding | 个人版/商用版 |
| 设计素材 | 配色方案、字体组合、UI Kit | 个人版/团队版 |
| 教程/课程 | AI 工具使用指南、实战案例包 | 单独售卖 |

---

## 2. 功能需求

### 2.1 用户模块

#### 2.1.1 注册/登录

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 邮箱注册 | 邮箱 + 密码注册 | P0 |
| 密码登录 | 邮箱 + 密码 | P0 |
| JWT 认证 | Access Token (30min) + Refresh Token (7d) | P0 |
| 游客浏览 | 未登录可浏览商品，购买时引导登录 | P0 |

#### 2.1.2 用户中心

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 个人信息 | 修改昵称、头像 | P0 |
| 我的订单 | 订单列表、订单详情 | P0 |
| 我的下载 | 已购商品列表 + 下载按钮 + 版本更新提示 | P0 |
| 我的优惠券 | 已领取/已使用/已过期 分类查看 | P1 |
| 我的评价 | 待评价/已评价 | P1 |

#### 2.1.3 权限模型

| 角色 | 权限 |
|------|------|
| 游客 | 浏览商品、搜索 |
| 买家 | 游客权限 + 购买、下载、评价 |
| 管理员 | 全部权限 + 后台管理 |

---

### 2.2 商品模块

#### 2.2.1 分类管理

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 二级分类 | 支持最多2级分类树（如：Prompt → 营销文案） | P0 |
| 分类图标 | 每个分类可设置图标 | P0 |
| 分类排序 | 管理员可调整排序 | P1 |

#### 2.2.2 商品管理

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 商品 CRUD | 创建、编辑、删除商品 | P0 |
| 商品状态 | 草稿→上架→下架 三态流转 | P0 |
| 预览图管理 | 主图 + 最多10张预览图，支持拖拽排序 | P0 |
| 富文本详情 | 商品描述支持富文本（图片+文字混排） | P0 |
| 文件上传 | 上传商品文件（zip/pdf/ckpt/safetensors等） | P0 |
| Demo 文件 | 可选的免费演示文件，供买家试用 | P1 |
| 版本管理 | 更新版本号 + 更新日志，买家可收到更新通知 | P1 |
| 商品标签 | 热卖、新品、推荐 等标签 | P1 |
| 批量上架 | 勾选多个商品一键上架/下架 | P0 |
| 下载统计 | 自动累计下载次数 | P0 |
| 浏览量统计 | 自动累计浏览量 | P1 |

#### 2.2.3 SKU 管理

数字商品的 SKU 从矩阵结构简化为版本/授权层级：

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 版本定义 | 定义售卖版本（如：基础版/专业版/终身版） | P0 |
| 独立定价 | 每个版本独立设置价格、原价 | P0 |
| 授权说明 | 每个版本的授权范围说明 | P0 |

**SKU 示例**:
```
Prompt 模板包:
  基础版   ¥29   — 个人使用，限 100 次/月
  专业版   ¥99   — 商用授权，不限次数
  终身版   ¥199  — 商用授权 + 终身更新

ComfyUI 工作流:
  免费版   ¥0    — 基础功能
  Pro 版   ¥49   — 完整功能 + 优先支持
```

---

### 2.3 搜索与筛选

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 关键词搜索 | 商品名称、描述模糊匹配 | P0 |
| 分类筛选 | 按分类层级筛选 | P0 |
| 价格区间 | 滑块选择价格范围 | P0 |
| 排序 | 综合/价格升序/价格降序/销量/最新/评分 | P0 |
| 搜索建议 | 输入时下拉提示 | P1 |

---

### 2.4 购物车模块

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 加入购物车 | 选择版本加入 | P0 |
| 修改版本 | 切换不同版本 | P0 |
| 选择/取消选择 | 勾选要结算的商品 | P0 |
| 全选/取消全选 | 一键全选 | P0 |
| 删除商品 | 单个删除、批量删除已选 | P0 |
| 价格计算 | 实时计算选中商品总价（含优惠预览） | P0 |
| 持久化 | 登录用户购物车存 Redis，7天过期 | P0 |

---

### 2.5 订单模块

#### 2.5.1 下单流程

```
购物车 → 确认订单（选优惠券）→ 提交订单 → 支付 → 自动完成 → 下载
```

| 步骤 | 描述 | 优先级 |
|------|------|--------|
| 确认订单页 | 展示选中商品、优惠券、应付金额 | P0 |
| 选择优惠券 | 展示可用优惠券列表，选择后实时更新金额 | P1 |
| 提交订单 | 生成订单号，30分钟内未支付自动取消 | P0 |
| 支付 | 跳转支付（模拟/Stripe） | P0 |
| 支付回调 | 支付成功后自动完成订单，生成下载链接 | P0 |

#### 2.5.2 订单状态流转

```
待支付 → 已支付 → 已完成（自动，付款即完成）
   ↓
 已取消（超时/手动取消）
```

| 状态 | 触发条件 | 可执行操作 |
|------|----------|-----------|
| 待支付 | 订单创建 | 支付、取消 |
| 已支付 | 支付成功 | 自动流转到已完成 |
| 已完成 | 付款即完成 | 下载、评价 |
| 已取消 | 超时/手动取消 | 无 |

#### 2.5.3 订单详情

| 字段 | 描述 |
|------|------|
| 订单号 | 格式：yyyyMMddHHmmss + 6位随机数 |
| 商品快照 | 下单时的商品名、版本、价格 |
| 优惠信息 | 使用的优惠券、折扣金额 |
| 支付信息 | 支付方式、支付时间、支付流水号 |

#### 2.5.4 下载系统

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 下载按钮 | 订单完成后显示下载按钮 | P0 |
| 下载链接 | 带时效的签名URL，24小时有效 | P0 |
| 下载次数限制 | 同一订单最多下载 50 次 | P0 |
| 版本更新通知 | 商品更新版本时通知已购用户 | P1 |
| 下载日志 | 记录每次下载的 IP、时间 | P1 |

---

### 2.6 支付模块

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 支付抽象层 | 统一支付接口，可插拔支付后端 | P0 |
| 模拟支付 | 开发环境使用，直接标记支付成功 | P0 |
| Stripe（预留） | 预留接口，后期可接入 | P1 |
| 支付超时 | 30分钟未支付自动取消 | P0 |

---

### 2.7 营销模块

#### 2.7.1 优惠券

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 创建优惠券 | 名称、类型、面值、最低消费、有效期、总量 | P0 |
| 优惠券类型 | 满减券、折扣券、固定金额券 | P0 |
| 领取限制 | 每人限领1张 | P0 |
| 使用规则 | 订单金额 >= 最低消费才可用 | P0 |
| 自动过期 | 超过有效期自动失效 | P0 |

---

### 2.8 评价模块

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 发表评价 | 1-5星评分 + 文字 | P0 |
| 匿名评价 | 可选匿名，隐藏用户名 | P1 |
| 评价排序 | 按时间/评分/有用数排序 | P1 |
| 评价统计 | 好评率、各星级数量统计 | P0 |

---

### 2.9 后台管理模块

#### 2.9.1 数据看板

| 指标 | 描述 | 优先级 |
|------|------|--------|
| 今日数据 | 今日订单数、销售额 | P0 |
| 趋势图 | 近7天/30天 销售额和订单量趋势 | P0 |
| 热销排行 | Top 10 热销商品 | P1 |

#### 2.9.2 商品管理后台

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 商品列表 | 分页、搜索、按状态/分类筛选 | P0 |
| 创建商品 | 表单：基本信息 + 分类 + 图片 + 文件 + SKU | P0 |
| 编辑商品 | 同创建表单 | P0 |
| 上下架 | 单个/批量上下架 | P0 |
| 删除 | 软删除 | P0 |
| 文件管理 | 上传/更新商品文件，管理版本 | P0 |

#### 2.9.3 订单管理后台

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 订单列表 | 分页、搜索（订单号/用户名）、按状态筛选 | P0 |
| 订单详情 | 完整订单信息 | P0 |

#### 2.9.4 营销管理后台

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 优惠券管理 | 创建、编辑、停用、查看领取/使用情况 | P0 |

#### 2.9.5 用户管理后台

| 功能 | 描述 | 优先级 |
|------|------|--------|
| 用户列表 | 分页、搜索、按状态筛选 | P0 |
| 禁用/启用 | 禁用后用户无法登录 | P1 |

---

## 3. 非功能需求

### 3.1 性能要求

| 指标 | 目标值 |
|------|--------|
| 商品列表加载 | < 500ms |
| 商品详情加载 | < 300ms |
| 搜索响应 | < 500ms |
| 下单接口 | < 1s |

### 3.2 安全要求

| 项目 | 要求 |
|------|------|
| 认证 | JWT + Token 刷新 |
| 授权 | RBAC 角色权限控制 |
| 密码 | bcrypt 加密存储 |
| 文件下载 | 签名URL + 时效 + 下载次数限制 |
| SQL注入 | Django ORM 自动防护 |
| XSS | 前端输出转义 |
| CORS | 白名单配置 |

### 3.3 数据规范

| 项目 | 规范 |
|------|------|
| 金额 | 存储单位为分（Integer），避免浮点精度问题 |
| 时间 | 统一使用 UTC 存储，前端展示时转本地时区 |
| 软删除 | 商品、订单使用 `is_deleted` 标记，不物理删除 |
| ID | 自增 ID，订单号使用业务编号 |
| 图片 | 上传后生成缩略图（300x300, 600x600, 1200x1200） |
| 文件 | 单文件 <= 500MB，支持常见格式 |

---

## 4. 前端设计规范

### 4.1 设计原则

1. **极简克制** — 每个页面只做一件事，移除所有不必要的元素
2. **大留白** — 内容间距 >= 24px，区块间距 >= 48px
3. **大图优先** — 预览图占视觉主体，文字精简
4. **一致的节奏** — 8px 基础网格，所有间距为 8 的倍数
5. **微妙动效** — 过渡 200-300ms，缓动函数 ease-out
6. **移动优先** — 先设计移动端，再适配桌面端

### 4.2 色彩系统

```css
/* 主色 */
--color-primary:    #1a1a2e;    /* 深蓝黑，用于导航、标题 */
--color-accent:     #e94560;    /* 强调色，用于价格、按钮、提示 */

/* 中性色 */
--color-text-primary:   #1a1a1a;
--color-text-secondary: #666666;
--color-text-hint:      #999999;
--color-bg-primary:     #ffffff;
--color-bg-secondary:   #f5f5f7;  /* Apple 风格浅灰 */
--color-border:         #e8e8e8;

/* 功能色 */
--color-success:    #52c41a;
--color-warning:    #faad14;
--color-error:      #ff4d4f;
```

### 4.3 字体系统

```css
--font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
               'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;

/* 字号 */
--font-size-xs:   12px;   /* 辅助文字 */
--font-size-sm:   14px;   /* 次要文字 */
--font-size-base: 16px;   /* 正文 */
--font-size-lg:   20px;   /* 小标题 */
--font-size-xl:   24px;   /* 标题 */
--font-size-xxl:  32px;   /* 大标题 */
--font-size-hero: 48px;   /* 首页大标题 */
```

### 4.4 间距系统

```css
--space-xs:   4px;
--space-sm:   8px;
--space-md:   16px;
--space-lg:   24px;
--space-xl:   32px;
--space-xxl:  48px;
--space-xxxl: 64px;
```

### 4.5 圆角系统

```css
--radius-sm:   4px;    /* 按钮、输入框 */
--radius-md:   8px;    /* 卡片 */
--radius-lg:   12px;   /* 弹窗 */
--radius-full: 9999px; /* 胶囊按钮 */
```

### 4.6 阴影系统

```css
--shadow-sm:   0 1px 2px rgba(0,0,0,0.06);
--shadow-md:   0 4px 12px rgba(0,0,0,0.08);
--shadow-lg:   0 8px 24px rgba(0,0,0,0.12);
```

### 4.7 页面布局规范

#### 商城前台

```
┌─────────────────────────────────────┐
│  顶部导航 (固定, 64px高)              │
│  Logo    搜索栏    登录/购物车       │
├─────────────────────────────────────┤
│                                     │
│  内容区域 (max-width: 1200px, 居中)  │
│                                     │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ 商品 │ │ 商品 │ │ 商品 │ │ 商品 │  │
│  │ 卡片 │ │ 卡片 │ │ 卡片 │ │ 卡片 │  │
│  └─────┘ └─────┘ └─────┘ └─────┘  │
│                                     │
├─────────────────────────────────────┤
│  底部信息 (简洁)                     │
└─────────────────────────────────────┘
```

#### 后台管理

```
┌──────┬──────────────────────────────┐
│ 侧边栏│  顶部栏 (面包屑 + 用户信息)  │
│ (240px)├──────────────────────────────┤
│      │                              │
│ 导航  │  内容区域                     │
│ 菜单  │  (padding: 24px)             │
│      │                              │
│      │  ┌──────────────────────┐    │
│      │  │ 筛选/搜索栏           │    │
│      │  ├──────────────────────┤    │
│      │  │ 表格/表单             │    │
│      │  └──────────────────────┘    │
└──────┴──────────────────────────────┘
```

---

## 5. API 规范

### 5.1 统一响应格式

```json
// 成功
{
    "code": 200,
    "message": "success",
    "data": { ... }
}

// 分页
{
    "code": 200,
    "message": "success",
    "data": {
        "count": 100,
        "next": "http://...",
        "previous": null,
        "results": [ ... ]
    }
}

// 错误
{
    "code": 400,
    "message": "参数错误",
    "errors": {
        "field_name": ["错误描述"]
    }
}
```

### 5.2 HTTP 状态码使用

| 状态码 | 使用场景 |
|--------|---------|
| 200 | 成功 |
| 201 | 创建成功 |
| 204 | 删除成功（无返回体） |
| 400 | 参数校验失败 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

### 5.3 分页规范

| 参数 | 默认值 | 说明 |
|------|--------|------|
| page | 1 | 页码 |
| page_size | 20 | 每页数量，最大100 |

### 5.4 排序规范

```
GET /api/v1/products/?ordering=price        # 价格升序
GET /api/v1/products/?ordering=-price       # 价格降序
GET /api/v1/products/?ordering=-download_count # 按下载量降序
```

---

## 6. 技术栈与约束

### 6.1 技术栈

| 层 | 技术 |
|---|------|
| 后端框架 | Django 5 + Django REST Framework |
| 数据库 | MySQL 8.0 |
| 缓存 | Redis（购物车、session、热门商品缓存） |
| 前端框架 | Vue 3 + Vite |
| UI 组件 | Element Plus（后台）+ 自定义设计系统（前台） |
| 状态管理 | Pinia |
| 路由 | Vue Router |
| HTTP 客户端 | Axios |
| 支付 | 模拟支付 + 预留 Stripe 接口 |
| 文件存储 | 本地存储（前期）→ OSS（后期） |

### 6.2 技术约束

| 约束 | 说明 |
|------|------|
| Python 版本 | >= 3.11 |
| Django 版本 | >= 5.0 |
| DRF 版本 | >= 3.15 |
| Vue 版本 | Vue 3.4+ |
| Node 版本 | >= 18 |
| MySQL 版本 | >= 8.0 |
| Redis 版本 | >= 7.0 |
| 金额存储 | 分（Integer），前端展示时 / 100 |
| 文件上传 | 单文件 <= 500MB |
| 图片上传 | 单文件 <= 5MB，仅允许 jpg/png/webp |
| 日志 | Django logging，按日期轮转 |
| 代码风格 | Python: PEP8 + Black; JS: ESLint + Prettier |

---

## 7. 项目结构

### 7.1 Django 后端

```
shop_api/
├── config/                    # 项目配置
│   ├── settings/
│   │   ├── base.py           # 基础配置
│   │   ├── development.py    # 开发环境
│   │   └── production.py     # 生产环境
│   ├── urls.py               # 总路由
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/                # 用户模块
│   │   ├── models.py         # User, DownloadLog
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── products/             # 商品模块（核心）
│   │   ├── models.py         # Category, Product, SKU, ProductImage
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── filters.py        # 商品筛选
│   │   └── urls.py
│   ├── cart/                 # 购物车（Redis）
│   │   ├── views.py
│   │   └── urls.py
│   ├── orders/               # 订单模块
│   │   ├── models.py         # Order, OrderItem
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── payment/              # 支付模块
│   │   ├── models.py         # Payment
│   │   ├── backends/         # 支付后端
│   │   │   ├── base.py       # 抽象基类
│   │   │   └── mock.py       # 模拟支付
│   │   ├── views.py
│   │   └── urls.py
│   ├── marketing/            # 营销模块
│   │   ├── models.py         # Coupon, UserCoupon
│   │   ├── views.py
│   │   └── urls.py
│   ├── reviews/              # 评价模块
│   │   ├── models.py         # Review
│   │   ├── views.py
│   │   └── urls.py
│   └── admin_panel/          # 后台管理API
│       ├── views.py
│       └── urls.py
├── common/                   # 公共模块
│   ├── permissions.py
│   ├── pagination.py
│   ├── exceptions.py
│   └── utils.py
├── media/                    # 上传文件
│   ├── products/             # 商品文件
│   ├── images/               # 商品图片
│   └── avatars/              # 用户头像
├── manage.py
└── requirements.txt
```

### 7.2 Vue 前端

```
frontend/
├── src/
│   ├── api/                  # API 请求封装
│   ├── views/
│   │   ├── storefront/       # 商城前台
│   │   │   ├── Home.vue          # 首页（精选推荐 + 分类导航）
│   │   │   ├── ProductList.vue   # 商品列表（筛选+搜索）
│   │   │   ├── ProductDetail.vue # 商品详情（预览图 + 版本选择 + 评价）
│   │   │   ├── Cart.vue          # 购物车
│   │   │   ├── Checkout.vue      # 结算
│   │   │   ├── OrderList.vue     # 我的订单
│   │   │   ├── Downloads.vue     # 我的下载
│   │   │   └── Profile.vue       # 个人中心
│   │   └── admin/            # 后台管理
│   │       ├── Dashboard.vue     # 数据看板
│   │       ├── ProductManage.vue # 商品管理
│   │       ├── OrderManage.vue   # 订单管理
│   │       ├── CouponManage.vue  # 优惠券管理
│   │       └── UserManage.vue    # 用户管理
│   ├── components/           # 通用组件
│   │   ├── ProductCard.vue   # 商品卡片
│   │   ├── SearchBar.vue     # 搜索栏
│   │   ├── ImageGallery.vue  # 图片画廊
│   │   ├── PriceTag.vue      # 价格标签
│   │   └── EmptyState.vue    # 空状态
│   ├── stores/               # Pinia 状态管理
│   ├── router/               # 路由配置
│   ├── styles/               # 全局样式
│   └── utils/                # 工具函数
├── vite.config.js
└── package.json
```

---

## 8. API 路由设计

```
/api/v1/
├── auth/                    # 认证
│   ├── register/
│   ├── login/
│   └── token/refresh/
├── users/                   # 用户
│   ├── me/                  # 当前用户信息
│   ├── me/downloads/        # 我的下载
│   └── me/coupons/          # 我的优惠券
├── products/                # 商品
│   ├── /                    # 商品列表（支持筛选、排序、搜索）
│   ├── {id}/                # 商品详情
│   ├── categories/          # 分类树
│   └── search/suggest/      # 搜索建议
├── cart/                    # 购物车
│   ├── /                    # 获取/清空
│   ├── items/               # 添加/修改/删除
│   └── select/              # 全选/取消全选
├── orders/                  # 订单
│   ├── /                    # 订单列表
│   ├── create/              # 创建订单
│   ├── {id}/                # 订单详情
│   └── {id}/cancel/         # 取消订单
├── payment/                 # 支付
│   ├── create/              # 发起支付
│   └── callback/            # 支付回调
├── reviews/                 # 评价
│   └── product/{id}/        # 商品评价列表
└── admin/                   # 后台管理API
    ├── dashboard/           # 数据统计
    ├── products/            # 商品CRUD + 批量操作
    ├── orders/              # 订单管理
    ├── coupons/             # 优惠券管理
    └── users/               # 用户管理
```

---

## 9. 核心数据模型

### 9.1 用户模块 (users)

```
User:
  - id, username, email, password
  - avatar, nickname, is_active, is_staff
  - created_at, updated_at

DownloadLog:
  - id, user (FK), order_item (FK)
  - ip, user_agent, downloaded_at
```

### 9.2 商品模块 (products)

```
Category:
  - id, name, parent (self FK), level, icon, sort_order
  - is_active

Product:
  - id, name, category (FK)
  - description (富文本), main_image
  - file (商品文件), demo_file (免费demo, 可空)
  - version, changelog
  - is_active, is_deleted, is_featured
  - download_count, view_count
  - created_at, updated_at

ProductImage:
  - id, product (FK), image, sort_order

SKU:
  - id, product (FK)
  - name (如: "基础版"、"专业版")
  - price, original_price
  - license_description (授权说明)
  - sort_order, is_active
```

### 9.3 购物车 (cart - Redis)

```
Redis Key: cart:{user_id}
Hash Field: sku_id
Hash Value: JSON { quantity, selected, added_at }
TTL: 7 days
```

### 9.4 订单模块 (orders)

```
Order:
  - id, order_no, user (FK)
  - total_amount, discount_amount, pay_amount
  - status (待支付/已支付/已完成/已取消)
  - coupon (FK, nullable)
  - pay_time, complete_time
  - remark, is_deleted

OrderItem:
  - id, order (FK), sku (FK)
  - product_name, sku_name, price
  - download_count, download_token
```

### 9.5 支付模块 (payment)

```
Payment:
  - id, order (FK), payment_no
  - amount, method (mock/stripe)
  - status (pending/success/failed)
  - paid_at
```

### 9.6 营销模块 (marketing)

```
Coupon:
  - id, name, code
  - type (满减/折扣/固定金额)
  - value, min_amount
  - start_time, end_time, total, used
  - is_active

UserCoupon:
  - id, user (FK), coupon (FK)
  - is_used, used_at
```

### 9.7 评价模块 (reviews)

```
Review:
  - id, user (FK), product (FK), sku (FK), order (FK)
  - rating (1-5), content
  - is_anonymous
  - created_at
```

---

## 10. 里程碑

| 阶段 | 内容 | 预计时间 |
|------|------|---------|
| M1 | 项目搭建 + 用户模块 + 基础框架 | 已完成 |
| M2 | 商品模块（分类/商品/SKU/文件上传） | 3天 |
| M3 | 购物车 + 订单 + 下载系统 | 3天 |
| M4 | 支付 + 优惠券 | 2天 |
| M5 | 评价 + 搜索 + 数据看板 | 2天 |
| M6 | Vue 前端商城 + 后台管理 | 5天 |

**总计**: 约 15 个工作日
