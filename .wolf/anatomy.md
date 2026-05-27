# anatomy.md

> Auto-maintained by OpenWolf. Last scanned: 2026-05-27T09:20:38.577Z
> Files: 270 tracked | Anatomy hits: 0 | Misses: 0

## ./

- `.dockerignore` (~36 tok)
- `.gitignore` — Git ignore rules (~121 tok)
- `.mcp.json` (~126 tok)
- `CLAUDE.md` — OpenWolf (~742 tok)
- `docker-compose.yml` — Docker Compose services (~264 tok)
- `prd.json` (~3105 tok)
- `PRD.md` — 产品需求文档 (PRD) (~4017 tok)
- `Procfile` (~27 tok)
- `progress.txt` — Ralph Progress Log (~8509 tok)
- `README.md` — Project documentation (~6921 tok)
- `render.yaml` (~213 tok)

## .claude/

- `settings.json` (~441 tok)
- `settings.local.json` (~858 tok)

## .claude/rules/

- `openwolf.md` (~313 tok)

## .github/workflows/

- `ci.yml` — CI: CI (~395 tok)

## cache/

- `__init__.py` (~142 tok)
- `api.py` — Message Cache REST API (~1590 tok)
- `config.py` — class: cache_key, system_cache_key, is_expired, fingerprint + 3 more (~1031 tok)
- `dashboard.py` — Message Cache Web Dashboard (~2506 tok)
- `glossary.py` — 中文停用词（高频无意义词） (~2123 tok)
- `service.py` — View: get, put (~2908 tok)
- `storage.py` — View: get, put, delete, get, put, delete, get, put, get, put, delete (~1022 tok)

## frontend/

- `.dockerignore` (~9 tok)
- `.env.example` — Frontend environment variables template (~220 tok)
- `.gitignore` — Git ignore rules (~68 tok)
- `Dockerfile` — Docker container definition (~38 tok)
- `index.html` — ShopEase — AI 数字精品店 (~167 tok)
- `package-lock.json` — npm lock file (~17546 tok)
- `package.json` — Node.js package manifest (~182 tok)
- `README.md` — Project documentation (~97 tok)
- `tsconfig.json` — TypeScript configuration (~134 tok)
- `vercel.json` (~51 tok)
- `vite.config.js` (~265 tok)

## frontend/scripts/

- `homepage-regression.cjs` — assert: main (~1399 tok)
- `secondary-redesign-regression.cjs` — ', async (route) => { (~4244 tok)

## frontend/src/

- `App.vue` — Vue component (~11 tok)
- `env.d.ts` — / <reference types="vite/client" /> (~54 tok)
- `main.js` — Declares app (~191 tok)

## frontend/src/api/

- `adminPanel.d.ts` — Exports AdminOrderListParams, AdminUserListParams, getAdminOrders, getAdminOrder + 2 more (~195 tok)
- `adminPanel.js` — API routes: GET (4 endpoints) (~101 tok)
- `adminProduct.d.ts` — Exports AdminProductListParams, AdminProductCreatePayload, AdminBatchPayload, AdminCategoryCreatePay (~633 tok)
- `adminProduct.js` — API routes: GET, POST, PATCH, DELETE (13 endpoints) (~380 tok)
- `cart.d.ts` — Exports CartItem, CartData, CartAddPayload, CartUpdatePayload + 9 more (~357 tok)
- `cart.js` — API routes: GET, POST, PUT, DELETE (7 endpoints) (~157 tok)
- `order.d.ts` — Exports OrderItem, OrderListItem, OrderDetail, OrderCreatePayload + 8 more (~478 tok)
- `order.js` — API routes: POST, GET (6 endpoints) (~150 tok)
- `payment.d.ts` — Exports PaymentData, PaymentCreatePayload, PaymentQueryResult, PaymentCallbackPayload + 3 more (~196 tok)
- `payment.js` — API routes: POST, GET (3 endpoints) (~81 tok)
- `product.d.ts` — Exports Category, CategoryFlat, ProductListItem, SKU + 7 more (~541 tok)
- `product.js` — API routes: GET (4 endpoints) (~96 tok)
- `types.ts` — Standard API response wrapper (~89 tok)
- `user.d.ts` — Exports UserData, LoginData, RegisterData, AuthTokens + 5 more (~275 tok)
- `user.js` — API routes: POST, GET, PATCH (5 endpoints) (~112 tok)

## frontend/src/components/

- `AnimatedIcons.vue` — Vue: setup (~2483 tok)
- `GradientText.vue` — Vue: setup (~282 tok)
- `PageTransition.vue` — Vue: setup (~73 tok)
- `ProductCard.vue` — Vue: setup (~1727 tok)
- `StatusBadge.vue` — Vue: setup (~236 tok)
- `StoreAccountNav.vue` — Vue: setup (~258 tok)
- `StorePageHeader.vue` — Vue: setup (~389 tok)
- `WechatPayModal.vue` — Vue: setup, emits (~1894 tok)

## frontend/src/composables/

- `useGsap.js` — Exports defaults, useReducedMotion, useIsMobile, useGsapDefaults (~493 tok)
- `useMicroInteraction.js` — Exports useMicroInteraction (~405 tok)
- `usePageTransition.js` — Exports usePageTransition (~262 tok)
- `useScrollReveal.js` — Exports useScrollReveal (~336 tok)
- `useStaggerGrid.js` — Exports useStaggerGrid (~294 tok)
- `useTextReveal.js` — Exports useTextReveal (~394 tok)

## frontend/src/router/

- `index.js` — Declares routes (~1038 tok)

## frontend/src/stores/

- `app.js` — Exports useAppStore (~38 tok)
- `cart.js` — Exports useCartStore (~417 tok)
- `types.ts` — Exports UserState, CartState, AppState (~90 tok)
- `user.js` — Exports useUserStore (~437 tok)

## frontend/src/styles/

- `global.css` — Styles: 51 rules, 81 vars, 1 media queries, 7 animations (~9490 tok)

## frontend/src/utils/

- `authFeedback.js` — Exports validateLoginForm, validateRegisterForm, parseAuthApiError (~1092 tok)
- `request.js` — Declares request (~388 tok)

## frontend/src/views/admin/

- `AdminLayout.vue` — Vue: setup (~2089 tok)
- `CouponManage.vue` — Vue: setup (~1799 tok)
- `Dashboard.vue` — Vue: setup (~1571 tok)
- `OrderManage.vue` — Vue: setup (~2228 tok)
- `ProductEditor.vue` — Vue: setup (~5803 tok)
- `ProductManage.vue` — Vue: setup (~3372 tok)
- `UserManage.vue` — Vue: setup (~1819 tok)

## frontend/src/views/storefront/

- `Cart.vue` — Vue: setup (~2521 tok)
- `CategoryBrowse.vue` — Vue: setup (~1280 tok)
- `Checkout.vue` — Vue: setup (~1760 tok)
- `Downloads.vue` — Vue: setup (~1101 tok)
- `Help.vue` — Vue: setup (~1401 tok)
- `Home.vue` — Vue: setup (~4466 tok)
- `Login.vue` — Vue: setup (~3026 tok)
- `MainLayout.vue` — Vue: setup (~4565 tok)
- `OrderDetail.vue` — Vue: setup (~2212 tok)
- `Orders.vue` — Vue: setup (~2064 tok)
- `ProductDetail.vue` — Vue: setup (~3640 tok)
- `ProductList.vue` — Vue: setup (~3223 tok)
- `Profile.vue` — Vue: setup (~1204 tok)
- `Register.vue` — Vue: setup (~2907 tok)
- `Showcase.vue` — Vue: setup (~727 tok)
- `Wishlist.vue` — Vue: setup (~782 tok)

## graphify-out/

- `.graphify_chunk_00.json` (~5634 tok)
- `.graphify_chunk_01.json` (~3926 tok)
- `.graphify_chunk_02.json` (~8119 tok)
- `.graphify_chunk_03.json` — Declares restricting (~3441 tok)
- `.graphify_chunk_04.json` (~4010 tok)
- `.graphify_chunk_05.json` (~7163 tok)
- `.graphify_chunk_06.json` (~4785 tok)
- `.graphify_chunk_07.json` (~2821 tok)
- `.graphify_chunk_08.json` (~1132 tok)
- `.graphify_chunk_09.json` — Declares configuration (~3908 tok)
- `.graphify_chunk_10.json` (~5374 tok)
- `.graphify_chunk_11.json` (~664 tok)
- `.graphify_count_dirs.ps1` (~93 tok)
- `.graphify_merge_final.py` (~305 tok)
- `.graphify_merge_semantic.py` (~296 tok)
- `.graphify_split_chunks.py` (~617 tok)
- `.graphify_step_ast.py` — main (~259 tok)
- `.graphify_step_cache.py` (~222 tok)
- `.graphify_step1.ps1` — Declares Find (~457 tok)
- `.graphify_step2.py` (~42 tok)
- `.graphify_step4.py` (~481 tok)
- `.graphify_step5_label.py` (~654 tok)
- `.graphify_step6_html.py` (~260 tok)
- `.graphify_step8_benchmark.py` (~90 tok)
- `.graphify_step9_cleanup.py` — Save manifest for --update (~360 tok)
- `.graphify_transcribe.py` (~145 tok)

## shop_api/

- `conftest.py` — api_client, test_user, admin_user, auth_client (~272 tok)
- `docker-entrypoint.sh` (~43 tok)
- `Dockerfile` — Docker container definition (~134 tok)
- `manage.py` — Django's command-line utility for administrative tasks. (~219 tok)
- `pyproject.toml` (~122 tok)
- `requirements-dev.txt` (~27 tok)
- `requirements.txt` — Python dependencies (~74 tok)
- `runtime.txt` (~4 tok)
- `setup_spectacular.py` — patch_settings (~603 tok)

## shop_api/apps/

- `__init__.py` (~0 tok)

## shop_api/apps/admin_panel/

- `__init__.py` (~0 tok)
- `admin.py` — Register your models here. (~19 tok)
- `apps.py` — Declares AdminPanelConfig (~47 tok)
- `models.py` — Create your models here. (~18 tok)
- `tests.py` — Create your tests here. (~18 tok)
- `urls.py` (~176 tok)
- `views.py` — DashboardView: get, get_queryset, get_price_yuan, get_pay_amount_yuan + 5 more (~1964 tok)

## shop_api/apps/admin_panel/migrations/

- `__init__.py` (~0 tok)

## shop_api/apps/cart/

- `__init__.py` (~0 tok)
- `admin.py` — Register your models here. (~19 tok)
- `apps.py` — Declares CartConfig (~44 tok)
- `models.py` — Model: CartItem, 6 fields (~212 tok)
- `serializers.py` — Declares CartAddSerializer (~242 tok)
- `services.py` — CartService: get_items, add, update, remove + 3 more (~523 tok)
- `tests.py` — TestCartAuth: cart_user, cart_client, second_cart_user, second_cart_client + 30 more (~5726 tok)
- `urls.py` — URL patterns: 5 routes (~138 tok)
- `views.py` — View: get, delete, post, put, delete, post, post (~1116 tok)

## shop_api/apps/cart/migrations/

- `__init__.py` (~0 tok)
- `0001_initial.py` — Declares Migration (~526 tok)

## shop_api/apps/marketing/

- `__init__.py` (~0 tok)
- `admin.py` — Declares CouponAdmin (~167 tok)
- `apps.py` — Declares MarketingConfig (~46 tok)
- `models.py` — Model: Coupon, table: coupons, 16 fields (~499 tok)
- `serializers.py` — CouponSerializer: get_value_yuan, get_min_amount_yuan, validate_coupon_id, validate + 1 more (~667 tok)
- `tests.py` — TestCouponList: coupon_user, coupon_client, coupon_admin, admin_coupon_client + 31 more (~4552 tok)
- `urls.py` — URL patterns: 5 routes (~151 tok)
- `views.py` — View: post (~599 tok)

## shop_api/apps/marketing/migrations/

- `__init__.py` (~0 tok)
- `0001_initial.py` — Declares Migration (~1218 tok)

## shop_api/apps/orders/

- `__init__.py` (~0 tok)
- `admin.py` — Declares OrderItemInline (~172 tok)
- `apps.py` — Declares OrdersConfig (~45 tok)
- `models.py` — Model: Order, table: orders, 20 fields (~635 tok)
- `serializers.py` — OrderItemSerializer: get_price_yuan, get_pay_amount_yuan, get_total_amount_yuan, get_discount_amount (~1096 tok)
- `tests.py` — TestOrderCreate: order_user, order_client, other_user, other_client + 24 more (~5519 tok)
- `urls.py` — URL patterns: 6 routes (~168 tok)
- `views.py` — View: create, post, get (~898 tok)

## shop_api/apps/orders/migrations/

- `__init__.py` (~0 tok)
- `0001_initial.py` — Declares Migration (~1681 tok)

## shop_api/apps/payment/

- `__init__.py` (~0 tok)
- `admin.py` — Declares PaymentAdmin (~104 tok)
- `apps.py` — Declares PaymentConfig (~45 tok)
- `models.py` — Model: Payment, 6 fields (~304 tok)
- `tests.py` — Create your tests here. (~18 tok)
- `urls.py` — URL patterns: 4 routes (~122 tok)
- `views.py` — PaymentCreateView: get_backend, post, post, post + 2 more (~1749 tok)

## shop_api/apps/payment/backends/

- `__init__.py` (~0 tok)
- `alipay.py` — AlipayPaymentBackend: create_payment, query_payment, refund, verify_callback (~1879 tok)
- `base.py` — PaymentBackend: create_payment, query_payment, refund (~118 tok)
- `mock.py` — MockPaymentBackend: create_payment, query_payment, refund (~211 tok)
- `wechat.py` — WechatPaymentBackend: create_payment, query_payment, refund, verify_notification (~1226 tok)

## shop_api/apps/payment/migrations/

- `__init__.py` (~0 tok)
- `0001_initial.py` — Declares Migration (~728 tok)

## shop_api/apps/products/

- `__init__.py` (~0 tok)
- `admin.py` — Declares ProductImageInline (~332 tok)
- `apps.py` — Declares ProductsConfig (~46 tok)
- `filters.py` — ProductFilter: filter_min_price, filter_max_price (~224 tok)
- `models.py` — Model: Category, table: categories, 31 fields (~1043 tok)
- `serializers.py` — CategorySerializer: get_children, get_price_yuan, get_original_price_yuan, get_min_price_yuan + 1 mo (~944 tok)
- `tests.py` — TestProductList: product_admin_user, product_admin_client, product_normal_user, product_normal_clien (~6046 tok)
- `urls.py` (~446 tok)
- `views.py` — CategoryTreeView: get_queryset, get_queryset, get_queryset, retrieve + 12 more (~1896 tok)

## shop_api/apps/products/management/

- `__init__.py` (~1 tok)

## shop_api/apps/products/management/commands/

- `__init__.py` (~1 tok)
- `seed_demo_products.py` — Command: handle (~4215 tok)

## shop_api/apps/products/migrations/

- `__init__.py` (~0 tok)
- `0001_initial.py` — Declares Migration (~2398 tok)
- `0002_seed_categories.py` — Migration: create_categories, remove_categories (~533 tok)

## shop_api/apps/reviews/

- `__init__.py` (~0 tok)
- `admin.py` — Declares ReviewAdmin (~109 tok)
- `apps.py` — Declares ReviewsConfig (~45 tok)
- `models.py` — Model: Review, 8 fields (~324 tok)
- `serializers.py` — ReviewSerializer: get_username, validate, save (~596 tok)
- `tests.py` — Create your tests here. (~18 tok)
- `urls.py` — URL patterns: 3 routes (~108 tok)
- `views.py` — View: create, get (~495 tok)

## shop_api/apps/reviews/migrations/

- `__init__.py` (~0 tok)
- `0001_initial.py` — Declares Migration (~816 tok)
- `0002_review_images.py` — Declares Migration (~102 tok)

## shop_api/apps/users/

- `__init__.py` (~0 tok)
- `admin.py` — Declares UserAdmin (~228 tok)
- `apps.py` — Declares UsersConfig (~42 tok)
- `models.py` — Model: DownloadLog, table: users, 9 fields (~383 tok)
- `serializers.py` — RegisterSerializer: validate_username, validate_password, validate, create + 1 more (~1066 tok)
- `tests.py` — TestUserModel, TestRegister, TestLogin, TestJWTAuth, TestGuestAccess: 24 tests total (~3200 tok)
- `urls.py` — URL patterns: 4 routes (~119 tok)
- `views.py` — RegisterView: create, post, get_object (~717 tok)

## shop_api/apps/users/migrations/

- `__init__.py` (~0 tok)
- `0001_initial.py` — Declares Migration (~2060 tok)
- `0002_downloadlog_delete_address.py` — Declares Migration (~657 tok)
- `0003_create_superuser.py` — Migration: create_superuser, reverse (~192 tok)

## shop_api/common/

- `__init__.py` (~0 tok)
- `exceptions.py` — BadRequest: custom_exception_handler (~392 tok)
- `pagination.py` — Declares StandardPagination (~55 tok)
- `permissions.py` — IsAdminUser: has_permission, has_object_permission (~110 tok)
- `response.py` — success, error (~92 tok)
- `throttles.py` — PaymentRateThrottle: get_cache_key (~128 tok)
- `utils.py` — generate_order_no, generate_payment_no, get_file_extension (~110 tok)

## shop_api/config/

- `__init__.py` (~0 tok)
- `asgi.py` (~51 tok)
- `logging.py` — JsonFormatter: format, format (~811 tok)
- `urls.py` (~343 tok)
- `views.py` — HealthCheckView: get (~307 tok)
- `wsgi.py` (~51 tok)

## shop_api/config/settings/

- `__init__.py` (~0 tok)
- `base.py` (~1390 tok)
- `development.py` — Development settings. (~200 tok)
- `production.py` — Production settings. (~198 tok)
- `test.py` — Test settings — uses SQLite for fast, dependency-free tests. (~104 tok)

## shop_api/logs/

- `django.log` (~9996 tok)

## shop_api/media/products/demo/

- `seed-1-demo.txt` (~34 tok)
- `seed-2-demo.txt` (~35 tok)
- `seed-3-demo.txt` (~33 tok)
- `seed-4-demo.txt` (~37 tok)
- `seed-5-demo.txt` (~35 tok)

## shop_api/tests/

- `__init__.py` (~0 tok)
- `test_health.py` — TestHealthCheck: test_health_returns_200, test_health_returns_ok_status, test_health_no_auth_require (~442 tok)
- `test_login_lockout.py` — TestLoginLockout: test_success_login_not_locked, test_lockout_after_5_failures, test_locked_returns_ (~750 tok)
- `test_product_search.py` — TestSearchBasic: category, product, product2, inactive_product + 14 more (~1254 tok)
- `test_review_images.py` — TestReviewImages: category, product, test_create_review_with_images, test_create_review_without_imag (~1137 tok)
- `test_spectacular.py` — TestSchemaEndpoint: test_schema_json_accessible, test_schema_contains_openapi_version, test_schema_c (~428 tok)
- `test_throttling.py` — TestAnonThrottle: test_first_request_succeeds, test_throttled_after_limit, test_throttle_response_ha (~1279 tok)
- `test_view_count.py` — TestViewCountDetail: category, product, vc_admin_user, vc_admin_client + 11 more (~1188 tok)
- `test_wechat_payment.py` — TestWechatSandbox: backend, mock_order, test_create_payment_returns_pending, test_create_payment_pay (~1561 tok)

## skills/message-cache/

- `SKILL.md` — Message Cache Skill — 企业级版 (~1675 tok)

## tasks/

- `prd-engineering.md` — PRD: 工程化升级 (~702 tok)
- `prd-features-v2.md` — PRD: 功能补全 v2 (~666 tok)
- `prd-frontend-experience.md` — PRD: 前端体验升级 (~712 tok)
- `prd-security-ops.md` — PRD: 安全加固与运维基础设施 (~574 tok)
- `prd-testing.md` — PRD: 测试覆盖体系建设 (~840 tok)
- `test_persistence_final.py` — Declares app (~385 tok)
- `test_persistence.py` (~617 tok)
- `test_persistence2.py` (~729 tok)
- `test_persistence3.py` — Declares app (~406 tok)
- `test_persistence4.py` — Declares app (~658 tok)
- `test_persistence5.py` — Declares app (~984 tok)
