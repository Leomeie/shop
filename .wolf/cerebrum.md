# Cerebrum

> OpenWolf's learning memory. Updated automatically as the AI learns from interactions.
> Do not edit manually unless correcting an error.
> Last updated: 2026-05-22

## User Preferences

<!-- How the user likes things done. Code style, tools, patterns, communication. -->

## Key Learnings

- **Project:** shop
- **Description:** 全栈数字商品电商平台，基于 Django REST Framework + Vue 3 构建，支持商品管理、购物车、订单、微信支付（模拟）、优惠券、评价、下载中心等功能。

- **Test fixtures with api_client need explicit `db`** — the `api_client` fixture alone doesn't grant DB access. When test methods call `_coupon()` or similar helpers that do `Model.objects.create()`, add `db` to the method signature. Alternatively, wrap with a fixture that includes both.
- **CouponClaimView wraps response in `success()`** — coupon data is at `resp.data["data"]`, not `resp.data` directly. Same pattern applies to all views using common.response.success().
- **Coupon with total=0 is "fully claimed"** — `used >= total` evaluates to `0 >= 0 = True`, so claiming fails. This is correct behavior for coupons that are no longer distributed.

## Do-Not-Repeat

<!-- Mistakes made and corrected. Each entry prevents the same mistake recurring. -->
<!-- Format: [YYYY-MM-DD] Description of what went wrong and what to do instead. -->

## Decision Log

<!-- Significant technical decisions with rationale. Why X was chosen over Y. -->
