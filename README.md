# ShopEase — AI 数字精品店

全栈数字商品电商平台，基于 Django REST Framework + Vue 3 构建，支持商品管理、购物车、订单、微信支付（模拟）、优惠券、评价、下载中心等功能。

---

## 目录

- [技术栈](#技术栈)
- [项目结构](#项目结构)
- [系统架构](#系统架构)
- [数据模型](#数据模型)
- [API 路由总览](#api-路由总览)
- [认证系统](#认证系统)
- [前后端交互](#前后端交互)
- [核心业务流程](#核心业务流程)
- [部署方案](#部署方案)

---

## 技术栈

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10+ | 运行时 |
| Django | 4.2+ | Web 框架 |
| Django REST Framework | 3.14+ | REST API |
| SimpleJWT | 5.3+ | JWT 认证 |
| django-filter | 24.1+ | 查询过滤 |
| django-cors-headers | 4.3+ | 跨域处理 |
| psycopg2-binary | 2.9+ | PostgreSQL 驱动 |
| dj-database-url | 2.1+ | 数据库 URL 解析 |
| Pillow | 10.2+ | 图片处理 |
| gunicorn | 22.0+ | 生产 WSGI 服务器 |
| WhiteNoise | 6.6+ | 静态文件服务 |

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue | 3.5 | UI 框架（Composition API + `<script setup>`） |
| Vite | 8.0 | 构建工具（Rolldown） |
| Pinia | 3.x | 状态管理 |
| Vue Router | 4.x | 路由 |
| Axios | - | HTTP 客户端 |
| Element Plus | - | UI 组件库（按需引入） |
| GSAP | 3.15 | 动画引擎（ScrollTrigger） |

### 部署

| 服务 | 用途 |
|------|------|
| Vercel | 前端静态托管 |
| Render | 后端 API 托管（免费版） |
| Neon | PostgreSQL 数据库（免费版） |

---

## 项目结构

```
shop/
├── frontend/                          # Vue 3 前端
│   ├── public/
│   │   ├── icons/                     # SVG 图标
│   │   └── images/                    # 静态图片（logo、收款码）
│   ├── src/
│   │   ├── api/                       # API 接口模块
│   │   │   ├── user.js                # 认证（登录/注册/用户信息）
│   │   │   ├── product.js             # 商品列表/详情/分类
│   │   │   ├── cart.js                # 购物车 CRUD
│   │   │   ├── order.js               # 订单创建/列表/取消/下载
│   │   │   ├── payment.js             # 支付创建/回调/查询
│   │   │   ├── adminProduct.js        # 管理后台-商品管理
│   │   │   └── adminPanel.js          # 管理后台-仪表盘/订单/用户
│   │   ├── assets/                    # 静态资源
│   │   ├── components/                # 公共组件
│   │   │   ├── AnimatedIcons.vue      # SVG 动画图标
│   │   │   ├── ProductCard.vue        # 商品卡片（3D 倾斜效果）
│   │   │   ├── WechatPayModal.vue     # 微信支付弹窗
│   │   │   ├── StorePageHeader.vue    # 页面标题栏
│   │   │   └── StatusBadge.vue        # 状态标签
│   │   ├── composables/               # 组合式函数
│   │   │   ├── useGsap.js             # GSAP 插件注册
│   │   │   ├── usePageTransition.js   # 页面过渡动画
│   │   │   ├── useScrollReveal.js     # 滚动显现动画
│   │   │   └── useStaggerGrid.js      # 网格交错动画
│   │   ├── router/                    # 路由配置
│   │   │   └── index.js               # 路由定义 + 导航守卫
│   │   ├── stores/                    # Pinia 状态仓库
│   │   │   ├── user.js                # 用户状态（token、userInfo）
│   │   │   └── cart.js                # 购物车状态
│   │   ├── styles/                    # 全局样式
│   │   │   └── global.css             # CSS 变量、通用样式、管理后台暗色主题
│   │   ├── utils/                     # 工具函数
│   │   │   ├── request.js             # Axios 实例（拦截器、token 注入）
│   │   │   └── authFeedback.js        # 注册/登录表单校验
│   │   ├── views/                     # 页面视图
│   │   │   ├── storefront/            # 前台页面
│   │   │   │   ├── MainLayout.vue     # 前台布局壳（导航栏、页脚）
│   │   │   │   ├── Home.vue           # 首页
│   │   │   │   ├── ProductList.vue    # 商品列表
│   │   │   │   ├── ProductDetail.vue  # 商品详情
│   │   │   │   ├── Cart.vue           # 购物车
│   │   │   │   ├── Checkout.vue       # 结算页
│   │   │   │   ├── Orders.vue         # 订单列表
│   │   │   │   ├── OrderDetail.vue    # 订单详情（含支付）
│   │   │   │   ├── Downloads.vue      # 下载中心
│   │   │   │   ├── Login.vue          # 登录
│   │   │   │   └── Register.vue       # 注册
│   │   │   └── admin/                 # 后台管理页面
│   │   │       ├── AdminLayout.vue    # 后台布局壳（侧边栏、顶栏）
│   │   │       ├── Dashboard.vue      # 数据仪表盘
│   │   │       ├── ProductManage.vue  # 商品管理
│   │   │       ├── ProductEditor.vue  # 商品编辑器
│   │   │       ├── OrderManage.vue    # 订单管理
│   │   │       ├── CouponManage.vue   # 优惠券管理
│   │   │       └── UserManage.vue     # 用户管理
│   │   ├── main.js                    # 应用入口
│   │   └── App.vue                    # 根组件
│   ├── vercel.json                    # Vercel 部署配置
│   └── vite.config.js                 # Vite 构建配置
│
├── shop_api/                          # Django 后端
│   ├── apps/
│   │   ├── users/                     # 用户认证
│   │   │   ├── models.py              # User、DownloadLog
│   │   │   ├── serializers.py         # 注册/登录/用户序列化器
│   │   │   ├── views.py               # 注册/登录/用户信息视图
│   │   │   └── urls.py                # 认证路由
│   │   ├── products/                  # 商品管理
│   │   │   ├── models.py              # Category、Product、ProductImage、SKU
│   │   │   ├── serializers.py         # 商品/分类/SKU 序列化器
│   │   │   ├── views.py               # 前台查询 + 后台管理视图
│   │   │   ├── filters.py             # 商品过滤器
│   │   │   └── urls.py                # 商品路由
│   │   ├── cart/                      # 购物车
│   │   │   ├── models.py              # CartItem
│   │   │   ├── services.py            # CartService（数据库购物车逻辑）
│   │   │   ├── serializers.py         # 购物车序列化器
│   │   │   ├── views.py               # 购物车视图
│   │   │   └── urls.py                # 购物车路由
│   │   ├── orders/                    # 订单
│   │   │   ├── models.py              # Order、OrderItem
│   │   │   ├── serializers.py         # 订单创建/列表/详情序列化器
│   │   │   ├── views.py               # 订单视图
│   │   │   └── urls.py                # 订单路由
│   │   ├── payment/                   # 支付
│   │   │   ├── models.py              # Payment
│   │   │   ├── backends/              # 支付后端抽象
│   │   │   │   ├── base.py            # 支付后端接口
│   │   │   │   └── mock.py            # 模拟支付（自动成功）
│   │   │   ├── serializers.py         # 支付序列化器
│   │   │   ├── views.py               # 支付创建/回调/查询视图
│   │   │   └── urls.py                # 支付路由
│   │   ├── marketing/                 # 营销（优惠券）
│   │   │   ├── models.py              # Coupon、UserCoupon
│   │   │   ├── serializers.py         # 优惠券序列化器
│   │   │   ├── views.py               # 优惠券视图
│   │   │   └── urls.py                # 优惠券路由
│   │   ├── reviews/                   # 评价
│   │   │   ├── models.py              # Review
│   │   │   ├── serializers.py         # 评价序列化器
│   │   │   ├── views.py               # 评价视图
│   │   │   └── urls.py                # 评价路由
│   │   └── admin_panel/               # 管理后台仪表盘
│   │       ├── views.py               # 仪表盘统计、用户/订单查询
│   │       └── urls.py                # 后台路由
│   ├── common/                        # 公共模块
│   │   ├── response.py                # 统一响应格式 {code, message, data}
│   │   ├── permissions.py             # IsAdminUser、IsOwnerOrAdmin
│   │   ├── pagination.py              # 标准分页（每页 20 条）
│   │   ├── utils.py                   # 订单号/支付号生成
│   │   └── exceptions.py              # 自定义异常处理
│   ├── config/                        # Django 配置
│   │   ├── settings/
│   │   │   ├── base.py                # 基础配置
│   │   │   ├── development.py         # 本地开发（MySQL）
│   │   │   └── production.py          # 生产环境（PostgreSQL）
│   │   ├── urls.py                    # 根路由
│   │   ├── wsgi.py                    # WSGI 入口
│   │   └── asgi.py                    # ASGI 入口
│   ├── manage.py                      # Django 管理脚本
│   ├── requirements.txt               # Python 依赖
│   └── .env.example                   # 环境变量模板
│
├── render.yaml                        # Render 部署蓝图
└── .gitignore
```

---

## 系统架构

```
┌─────────────────────────────────────────────────────┐
│                    用户浏览器                         │
│              https://xxx.vercel.app                  │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS
                       ▼
┌─────────────────────────────────────────────────────┐
│                  Vercel（前端）                       │
│           Vue 3 SPA + Vite 构建产物                   │
│     /api/v1/* 请求 → 转发到 Render 后端               │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS (CORS)
                       ▼
┌─────────────────────────────────────────────────────┐
│                Render（后端 API）                     │
│         Django + Gunicorn + WhiteNoise               │
│                                                      │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│   │  users  │  │products │  │  cart   │            │
│   ├─────────┤  ├─────────┤  ├─────────┤            │
│   │ orders  │  │ payment │  │marketing│            │
│   ├─────────┤  ├─────────┤  ├─────────┤            │
│   │ reviews │  │admin_pnl│  │ common  │            │
│   └─────────┘  └─────────┘  └─────────┘            │
└──────────────────────┬──────────────────────────────┘
                       │ SSL
                       ▼
┌─────────────────────────────────────────────────────┐
│              Neon（PostgreSQL 数据库）                 │
│         用户、商品、订单、支付、评价等表                  │
└─────────────────────────────────────────────────────┘
```

**请求流程：**
1. 用户访问 Vercel 域名，下载 Vue SPA
2. SPA 发起 API 请求（如 `/api/v1/auth/login/`）
3. 请求到达 Render 后端，经过 JWT 中间件认证
4. 后端处理业务逻辑，查询 PostgreSQL
5. 返回统一 JSON 格式 `{code, message, data}`

---

## 数据模型

### ER 关系图

```
User ─────┬────── cart_items ────── SKU ──────── Product ────── Category
          │                                              │
          ├────── orders ──── order_items ──── SKU       ├── images
          │         │                                    └── file
          │         └───── payments
          │
          ├────── reviews
          │
          ├────── user_coupons ──── coupons
          │
          └────── download_logs ──── order_items
```

### 用户模块（users）

#### User（用户）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigAutoField | 主键 |
| username | CharField(150) | 用户名（继承 AbstractUser，唯一） |
| password | CharField(128) | 密码（继承，PBKDF2 哈希） |
| email | EmailField | 邮箱 |
| phone | CharField(11) | 手机号（唯一，可空） |
| nickname | CharField(50) | 昵称 |
| avatar | ImageField | 头像（上传到 avatars/） |
| is_active | BooleanField | 是否启用 |
| is_staff | BooleanField | 是否管理员（控制后台访问） |
| is_superuser | BooleanField | 是否超级管理员 |
| date_joined | DateTimeField | 注册时间 |

**表名：** `users`

#### DownloadLog（下载记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| user | FK → User | 下载用户 |
| order_item | FK → OrderItem | 下载的订单项 |
| ip | GenericIPAddressField | 下载 IP |
| user_agent | CharField(500) | 浏览器 UA |
| downloaded_at | DateTimeField | 下载时间（自动） |

**表名：** `download_logs`

---

### 商品模块（products）

#### Category（分类）

| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField(50) | 分类名称 |
| parent | FK → self | 父分类（可空，支持两级） |
| level | PositiveSmallIntegerField | 层级（1 或 2） |
| icon | CharField(50) | 图标标识 |
| sort_order | IntegerField | 排序权重 |
| is_active | BooleanField | 是否显示 |

**表名：** `categories`
**排序：** sort_order ASC, id ASC

#### Product（商品）

| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField(200) | 商品名称 |
| category | FK → Category | 所属分类（SET_NULL） |
| description | TextField | 商品描述（Markdown） |
| main_image | ImageField | 主图 |
| file | FileField | 商品文件（下载用） |
| demo_file | FileField | 试用文件（可空） |
| version | CharField(20) | 版本号（默认 1.0.0） |
| changelog | TextField | 更新日志 |
| status | CharField(10) | 状态：draft / active / inactive |
| is_deleted | BooleanField | 软删除标记 |
| is_featured | BooleanField | 是否推荐 |
| download_count | IntegerField | 累计下载次数 |
| view_count | IntegerField | 累计浏览次数 |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

**表名：** `products`
**排序：** created_at DESC
**属性：** `min_price` — 所有启用 SKU 中的最低价

#### ProductImage（商品图片）

| 字段 | 类型 | 说明 |
|------|------|------|
| product | FK → Product | 所属商品（CASCADE） |
| image | ImageField | 图片文件 |
| sort_order | IntegerField | 排序权重 |

**表名：** `product_images`

#### SKU（库存量单位）

| 字段 | 类型 | 说明 |
|------|------|------|
| product | FK → Product | 所属商品（CASCADE） |
| name | CharField(50) | 版本名称（如「个人版」「企业版」） |
| price | IntegerField | 价格（单位：分） |
| original_price | IntegerField | 原价（单位：分） |
| license_description | CharField(200) | 授权说明 |
| sort_order | IntegerField | 排序权重 |
| is_active | BooleanField | 是否启用 |

**表名：** `skus`

---

### 购物车模块（cart）

#### CartItem（购物车条目）

| 字段 | 类型 | 说明 |
|------|------|------|
| user | FK → User | 用户 |
| sku | FK → SKU | 商品 SKU |
| quantity | PositiveIntegerField | 数量（默认 1） |
| selected | BooleanField | 是否选中结算（默认 true） |
| created_at | DateTimeField | 添加时间 |
| updated_at | DateTimeField | 更新时间 |

**表名：** 由 Django 自动生成
**约束：** `unique_together = ("user", "sku")` — 每个用户每个 SKU 只有一条

---

### 订单模块（orders）

#### Order（订单）

| 字段 | 类型 | 说明 |
|------|------|------|
| order_no | CharField(30) | 订单号（唯一，时间戳+随机 hex） |
| user | FK → User | 下单用户 |
| total_amount | IntegerField | 商品总金额（分） |
| discount_amount | IntegerField | 优惠减免（分，默认 0） |
| pay_amount | IntegerField | 应付金额（分） |
| status | CharField(10) | 状态：pending / paid / completed / cancelled |
| coupon | FK → Coupon | 使用的优惠券（可空，预留） |
| pay_time | DateTimeField | 支付时间 |
| complete_time | DateTimeField | 完成时间 |
| remark | CharField(200) | 备注 |
| is_deleted | BooleanField | 软删除 |
| created_at | DateTimeField | 创建时间 |
| updated_at | DateTimeField | 更新时间 |

**表名：** `orders`

#### OrderItem（订单项）

| 字段 | 类型 | 说明 |
|------|------|------|
| order | FK → Order | 所属订单（CASCADE） |
| sku | FK → SKU | SKU（SET_NULL，删除商品后保留记录） |
| product_name | CharField(200) | 商品名（下单时快照） |
| sku_name | CharField(50) | 版本名（下单时快照） |
| price | IntegerField | 单价（分，下单时快照） |
| download_count | IntegerField | 已下载次数 |
| download_token | CharField(64) | 下载令牌（唯一，用于文件下载鉴权） |

**表名：** `order_items`

---

### 支付模块（payment）

#### Payment（支付记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| order | FK → Order | 关联订单（CASCADE） |
| payment_no | CharField(40) | 支付流水号（唯一，PAY+时间戳+随机 hex） |
| amount | IntegerField | 金额（分） |
| method | CharField(10) | 支付方式：mock / stripe |
| status | CharField(10) | 状态：pending / success / failed |
| paid_at | DateTimeField | 支付完成时间 |

**表名：** `payments`

---

### 营销模块（marketing）

#### Coupon（优惠券模板）

| 字段 | 类型 | 说明 |
|------|------|------|
| name | CharField(100) | 优惠券名称 |
| code | CharField(30) | 优惠码（唯一） |
| type | CharField(10) | 类型：minus（满减） / discount（折扣） / fixed（固定金额） |
| value | IntegerField | 面值/折扣（分或百分比） |
| min_amount | IntegerField | 最低消费（分，默认 0） |
| start_time | DateTimeField | 生效时间 |
| end_time | DateTimeField | 失效时间 |
| total | IntegerField | 发行总量 |
| used | IntegerField | 已领取数量 |
| is_active | BooleanField | 是否启用 |
| created_at | DateTimeField | 创建时间 |

**表名：** `coupons`

#### UserCoupon（用户优惠券）

| 字段 | 类型 | 说明 |
|------|------|------|
| user | FK → User | 领取用户 |
| coupon | FK → Coupon | 优惠券模板 |
| is_used | BooleanField | 是否已使用 |
| used_at | DateTimeField | 使用时间 |
| created_at | DateTimeField | 领取时间（自动） |

**表名：** `user_coupons`
**约束：** `unique_together = ["user", "coupon"]`

---

### 评价模块（reviews）

#### Review（评价）

| 字段 | 类型 | 说明 |
|------|------|------|
| user | FK → User | 评价用户 |
| product | FK → Product | 评价商品 |
| order | FK → Order | 关联订单（可空） |
| rating | PositiveSmallIntegerField | 评分（1-5） |
| content | TextField | 评价内容 |
| is_anonymous | BooleanField | 是否匿名 |
| created_at | DateTimeField | 创建时间 |

**表名：** `reviews`
**约束：** `unique_together = ["user", "product", "order"]` — 同一订单对同一商品只能评价一次

---

## API 路由总览

所有接口以 `/api/v1/` 为前缀。

### 认证（/api/v1/auth/）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/auth/register/` | 注册 | 公开 |
| POST | `/auth/login/` | 登录 | 公开 |
| POST | `/auth/token/refresh/` | 刷新 Token | 公开 |
| GET | `/auth/me/` | 获取当前用户信息 | 需登录 |
| PUT/PATCH | `/auth/me/` | 更新用户信息 | 需登录 |

### 商品（/api/v1/products/）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/products/` | 商品列表（分页、搜索、过滤） | 公开 |
| GET | `/products/<pk>/` | 商品详情（含图片和 SKU） | 公开 |
| GET | `/products/categories/` | 分类树（嵌套） | 公开 |
| GET | `/products/categories/flat/` | 分类扁平列表 | 公开 |
| GET/POST | `/products/admin/categories/` | 分类管理 | 管理员 |
| GET/PUT/PATCH/DELETE | `/products/admin/categories/<pk>/` | 分类详情 | 管理员 |
| GET/POST | `/products/admin/` | 商品管理 | 管理员 |
| GET/PUT/PATCH/DELETE | `/products/admin/<pk>/` | 商品详情（含软删除） | 管理员 |
| POST | `/products/admin/batch/` | 批量操作 | 管理员 |
| GET/POST | `/products/admin/<id>/images/` | 商品图片管理 | 管理员 |
| DELETE | `/products/admin/<id>/images/<pk>/` | 删除图片 | 管理员 |
| GET/POST | `/products/admin/<id>/skus/` | SKU 管理 | 管理员 |
| GET/PUT/PATCH/DELETE | `/products/admin/<id>/skus/<pk>/` | SKU 详情 | 管理员 |

### 购物车（/api/v1/cart/）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/cart/` | 获取购物车 | 需登录 |
| DELETE | `/cart/` | 清空购物车 | 需登录 |
| POST | `/cart/items/` | 添加商品 | 需登录 |
| PUT | `/cart/items/<sku_id>/` | 更新数量/选中状态 | 需登录 |
| DELETE | `/cart/items/<sku_id>/` | 删除单个 | 需登录 |
| POST | `/cart/select-all/` | 全选/取消全选 | 需登录 |
| POST | `/cart/remove-selected/` | 删除已选 | 需登录 |

### 订单（/api/v1/orders/）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/orders/create/` | 创建订单（从购物车选中项） | 需登录 |
| GET | `/orders/` | 订单列表 | 需登录 |
| GET | `/orders/<pk>/` | 订单详情 | 需登录 |
| POST | `/orders/<pk>/cancel/` | 取消订单 | 需登录 |
| GET | `/orders/downloads/` | 下载中心列表 | 需登录 |
| GET | `/orders/<oid>/items/<iid>/download/` | 获取下载链接 | 需登录 |

### 支付（/api/v1/payment/）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/payment/create/` | 创建支付 | 需登录 |
| POST | `/payment/callback/` | 支付回调（模拟） | 公开 |
| GET | `/payment/<payment_no>/` | 查询支付状态 | 需登录 |

### 优惠券（/api/v1/marketing/）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/marketing/coupons/` | 可领优惠券列表 | 公开 |
| POST | `/marketing/coupons/claim/` | 领取优惠券 | 需登录 |
| GET | `/marketing/my-coupons/` | 我的优惠券 | 需登录 |
| GET/POST | `/marketing/admin/coupons/` | 优惠券管理 | 管理员 |
| GET/PUT/PATCH/DELETE | `/marketing/admin/coupons/<pk>/` | 优惠券详情 | 管理员 |

### 评价（/api/v1/reviews/）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/reviews/` | 发表评价 | 需登录 |
| GET | `/reviews/product/<id>/` | 商品评价列表 | 公开 |
| GET | `/reviews/product/<id>/stats/` | 评价统计 | 公开 |

### 管理后台（/api/v1/admin/）

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/admin/dashboard/` | 仪表盘数据 | 管理员 |
| GET | `/admin/users/` | 用户列表 | 管理员 |
| GET | `/admin/users/<pk>/` | 用户详情 | 管理员 |
| GET | `/admin/orders/` | 全部订单 | 管理员 |
| GET | `/admin/orders/<pk>/` | 订单详情 | 管理员 |

---

## 认证系统

### JWT 认证流程

```
┌──────────┐     POST /auth/login/     ┌──────────┐
│  前端    │  ──── {username, pass} ──→ │  后端    │
│          │                            │          │
│          │  ←── {access, refresh, ── │          │
│          │       user}               │          │
└────┬─────┘                            └──────────┘
     │
     │  后续请求携带 Header:
     │  Authorization: Bearer <access_token>
     │
     ▼
┌──────────┐     Token 过期 (401)      ┌──────────┐
│  前端    │  ──── POST /token/refresh │  后端    │
│          │  ──── {refresh_token} ──→ │          │
│          │  ←── {new access_token} ─ │          │
└──────────┘                            └──────────┘
```

### Token 配置

| 参数 | 值 |
|------|-----|
| Access Token 有效期 | 30 分钟 |
| Refresh Token 有效期 | 7 天 |
| Token 轮换 | 启用（每次刷新生成新的 refresh token） |
| 黑名单 | 启用（旧 refresh token 刷新后失效） |
| Header 格式 | `Authorization: Bearer <token>` |

### 注册校验规则

- **用户名**：3-20 位字符，仅限字母、数字、下划线，不能是纯数字，唯一
- **密码**：6-20 位，必须包含至少一个字母和一个数字
- **确认密码**：必须与密码一致

### 登录流程

1. 前端发送 `{username, password}` 到 `POST /api/v1/auth/login/`
2. 后端调用 `django.contrib.auth.authenticate()` 验证
3. 验证通过 → 生成 JWT access + refresh token
4. 返回 `{user: {id, username, is_staff, ...}, access, refresh}`
5. 前端将 token 存入 localStorage 和 Pinia store
6. 后续所有请求自动携带 `Authorization: Bearer <token>`

### 权限控制

| 权限类 | 检查逻辑 | 使用场景 |
|--------|---------|---------|
| AllowAny | 无限制 | 商品列表、分类、登录注册 |
| IsAuthenticated | 检查 JWT token 有效性 | 购物车、订单、支付 |
| IsAdminUser | 检查 `is_staff = True` | 管理后台所有接口 |
| IsOwnerOrAdmin | 对象级别：staff 或所有者 | 用户信息修改 |

---

## 前后端交互

### 统一响应格式

所有 API 返回统一的 JSON 格式：

```json
// 成功
{
  "code": 200,
  "message": "success",
  "data": { ... }
}

// 失败
{
  "code": 400,
  "message": "错误描述",
  "data": null,
  "errors": { "field": ["错误信息"] }
}
```

### Axios 拦截器

**请求拦截器：**
- 自动从 Pinia store 读取 JWT token
- 自动添加 `Authorization: Bearer <token>` 请求头

**响应拦截器：**
- 统一解包响应体为 `{code, message, data}` 格式
- 收到 401 → 自动调用 `logout()` → 跳转登录页

### 开发环境代理

Vite 开发服务器自动代理以下路径到 Django 后端（`http://127.0.0.1:8000`）：

| 前端路径 | 后端地址 |
|---------|---------|
| `/api/*` | `http://127.0.0.1:8000/api/*` |
| `/media/*` | `http://127.0.0.1:8000/media/*` |

### 价格处理

后端所有价格以**分（整数）**存储。序列化器自动添加 `*_yuan` 计算字段：

```python
# 后端模型
price = models.IntegerField("价格（分）")

# 序列化器
price_yuan = serializers.SerializerMethodField()
def get_price_yuan(self, obj):
    return f"{obj.price / 100:.2f}"
```

前端直接使用 `price_yuan` 字段显示。

---

## 核心业务流程

### 1. 购物车 → 订单 → 支付

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ 添加商品 │ →  │ 购物车  │ →  │ 结算页  │ →  │ 订单详情│
│ 到购物车 │    │ 选中/改 │    │ 确认提交│    │ 微信支付│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
                                    │              │
                                    ▼              ▼
                              POST /orders/   POST /payment/create/
                              create/              │
                                                   ▼
                                            扫码 → 点「我已支付」
                                                   │
                                                   ▼
                                            POST /payment/callback/
                                                   │
                                                   ▼
                                            订单状态: pending → paid → completed
                                            自动生成下载令牌
```

**详细步骤：**

1. **添加购物车**：`POST /api/v1/cart/items/` → `{sku_id, quantity}` → CartService.add() → CartItem（如已存在则累加数量）

2. **创建订单**：`POST /api/v1/orders/create/` → `{remark}`
   - 读取购物车中 `selected=True` 的条目
   - 校验 SKU 状态（`is_active`）
   - 生成唯一订单号（时间戳 + 6位随机hex）
   - 创建 Order，设置 total_amount = sum(SKU.price × quantity)
   - 为每个数量单位创建一条 OrderItem（快照商品名、版本名、单价）
   - 为每个 OrderItem 生成唯一 download_token
   - 清除购物车中已选中的条目

3. **发起支付**：`POST /api/v1/payment/create/` → `{order_id, method: 'mock'}`
   - 创建 Payment 记录，生成 payment_no（PAY + 时间戳 + 8位随机hex）
   - 返回 payment_no 给前端

4. **显示支付弹窗**：前端展示 WechatPayModal，显示收款码图片 + 5分钟倒计时

5. **确认支付**：用户扫码后点击「我已支付」→ `POST /api/v1/payment/callback/` → `{payment_no}`
   - Mock 后端直接返回 success
   - 更新 Payment 状态为 success
   - 更新 Order 状态为 paid → completed（数字商品自动完成）
   - 每个 OrderItem 生成 download_token

6. **下载商品**：`GET /api/v1/orders/<oid>/items/<iid>/download/`
   - 校验 download_token
   - 限制最多下载 50 次
   - 记录 DownloadLog

### 2. 注册 → 登录 → 购买

```
注册页                 登录页                 商品页
  │                     │                     │
  │ POST /auth/register │ POST /auth/login/   │ GET /products/
  │ → JWT tokens        │ → JWT tokens        │ → 商品列表
  │ → 自动登录          │ → 跳转首页           │
  │                     │                     │ 点击商品
  │                     │                     │ → 商品详情
  │                     │                     │ → 选择 SKU
  │                     │                     │ → 加入购物车
  │                     │                     │ → 去结算
```

### 3. 管理员操作

```
登录（is_staff=True）
  │
  ▼
/admin（AdminLayout）
  ├─ Dashboard     → GET /admin/dashboard/  → 今日订单/销售额/趋势
  ├─ 商品管理       → CRUD /products/admin/
  ├─ 订单管理       → GET /admin/orders/
  ├─ 优惠券管理     → CRUD /marketing/admin/coupons/
  └─ 用户管理       → GET /admin/users/
```

### 4. 路由守卫流程

```
用户访问 /cart
  │
  ├─ meta.auth = true?
  │   ├─ 是 → isLoggedIn = true?
  │   │       ├─ 是 → userInfo = null?
  │   │       │       ├─ 是 → fetchUserInfo() → 成功? → 放行
  │   │       │       │                 → 失败? → logout → /login
  │   │       │       └─ 否 → 放行
  │   │       └─ 否 → /login?redirect=/cart
  │   └─ 否 → 放行
  │
  ├─ meta.admin = true?
  │   └─ 是 → isAdmin = true?
  │           ├─ 是 → 放行
  │           └─ 否 → /
```

---

## 前端路由映射

### 前台页面（MainLayout 包裹）

| 路径 | 组件 | 说明 | 需登录 |
|------|------|------|--------|
| `/` | Home | 首页（英雄区 + 推荐商品） | 否 |
| `/products` | ProductList | 商品列表（搜索/分类/排序） | 否 |
| `/products/:id` | ProductDetail | 商品详情 | 否 |
| `/showcase` | Showcase | 展示页 | 否 |
| `/categories` | CategoryBrowse | 分类浏览 | 否 |
| `/cart` | Cart | 购物车 | 是 |
| `/checkout` | Checkout | 结算确认 | 是 |
| `/orders` | Orders | 订单列表 | 是 |
| `/orders/:id` | OrderDetail | 订单详情 | 是 |
| `/downloads` | Downloads | 下载中心 | 是 |
| `/wishlist` | Wishlist | 收藏夹 | 是 |
| `/profile` | Profile | 个人中心 | 是 |
| `/help` | Help | 帮助中心 | 否 |

### 登录/注册（独立页面，无布局包裹）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/login` | Login | 登录页 |
| `/register` | Register | 注册页 |

### 后台管理（AdminLayout 包裹，需管理员权限）

| 路径 | 组件 | 说明 |
|------|------|------|
| `/admin` | Dashboard | 数据仪表盘 |
| `/admin/products` | ProductManage | 商品管理 |
| `/admin/products/new` | ProductEditor | 新建商品 |
| `/admin/products/:id/edit` | ProductEditor | 编辑商品 |
| `/admin/orders` | OrderManage | 订单管理 |
| `/admin/coupons` | CouponManage | 优惠券管理 |
| `/admin/users` | UserManage | 用户管理 |

---

## 部署方案

### 架构

| 服务 | 地址 | 用途 |
|------|------|------|
| Vercel | `https://shop-xxx.vercel.app` | 前端静态站点 |
| Render | `https://shop-api-xxx.onrender.com` | 后端 API |
| Neon | `postgres://xxx.neon.tech` | PostgreSQL 数据库 |

### 环境变量

**Vercel（前端）：**
| 变量 | 值 |
|------|-----|
| `VITE_API_BASE` | `https://shop-api-xxx.onrender.com/api/v1` |

**Render（后端）：**
| 变量 | 值 |
|------|-----|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `DJANGO_SECRET_KEY` | 随机生成 |
| `ALLOWED_HOSTS` | `shop-api-xxx.onrender.com` |
| `DATABASE_URL` | Neon PostgreSQL 连接 URL |
| `CORS_ALLOWED_ORIGINS` | `https://shop-xxx.vercel.app` |

### 构建流程

**Render Build Command：**
```bash
pip install -r shop_api/requirements.txt && \
cd shop_api && \
python manage.py migrate --noinput && \
python manage.py createcachetable && \
python manage.py collectstatic --noinput
```

**Render Start Command：**
```bash
cd shop_api && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 注意事项

- Render 免费版 15 分钟无请求后休眠，首次访问需等待冷启动（约 30-50 秒）
- Neon 免费版数据库 90 天不活跃会暂停
- 所有价格以分（整数）存储，前端显示时除以 100
- 订单创建后 30 分钟未支付自动取消（配置已定义，需定时任务实现）
- 支付使用模拟后端，用户扫描个人收款码后手动确认
