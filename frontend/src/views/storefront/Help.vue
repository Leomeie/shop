<template>
  <div class="store-page">
    <StorePageHeader eyebrow="Help Center" icon="shield" title="帮助中心" subtitle="关于购买、下载、授权和账户使用的常见问题。" compact />

    <div class="store-page-body">
      <div class="container">
        <div class="account-shell">
          <StoreAccountNav />

          <div class="account-content">
            <section class="store-surface store-surface--soft faq-panel">
              <div class="store-panel-header">
                <div>
                  <div class="store-panel-title">常见问题</div>
                  <div class="store-panel-subtitle">点击问题可展开查看详细说明</div>
                </div>
              </div>

              <div class="faq-list">
                <div v-for="(faq, index) in faqs" :key="index" class="faq-item" :class="{ open: openFaq === index }">
                  <button class="faq-question" type="button" @click="openFaq = openFaq === index ? null : index">
                    <span>{{ faq.q }}</span>
                    <AnimatedIcons :name="openFaq === index ? 'close' : 'plus'" :size="18" />
                  </button>
                  <Transition name="faq-expand">
                    <div v-if="openFaq === index" class="faq-answer">
                      <p>{{ faq.a }}</p>
                    </div>
                  </Transition>
                </div>
              </div>
            </section>

            <section class="store-surface store-surface--soft support-panel">
              <div class="store-panel-header">
                <div>
                  <div class="store-panel-title">联系支持</div>
                  <div class="store-panel-subtitle">仍有问题时，可通过以下方式获取帮助</div>
                </div>
              </div>

              <div class="support-list">
                <div class="support-item">
                  <AnimatedIcons name="mail" :size="16" />
                  <span>support@shopease.com</span>
                </div>
                <div class="support-item">
                  <AnimatedIcons name="globe" :size="16" />
                  <span>工作日 9:00 - 18:00</span>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StoreAccountNav from '../../components/StoreAccountNav.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'

const openFaq = ref(null)

const faqs = [
  { q: '购买后如何下载商品？', a: '支付完成后，在“我的下载”页即可看到已购买的商品，点击下载按钮即可获取。' },
  { q: '支持哪些支付方式？', a: '当前提供系统默认支付流程，后续可按业务需要接入更多支付方式。' },
  { q: '购买后可以退款吗？', a: '数字商品一经购买通常不支持无理由退款，如遇异常情况请联系支持处理。' },
  { q: '商品可以商用吗？', a: '不同资源的授权范围不同，请以商品详情页的授权说明为准。' },
  { q: '如何查看订单状态？', a: '在“我的订单”页可以查看待支付、已支付、已完成和已取消等状态。' },
  { q: '账户安全如何保障？', a: '系统使用标准鉴权与安全传输机制，敏感信息不会以明文形式存储。' },
]
</script>

<style scoped>
.faq-panel,
.support-panel {
  overflow: hidden;
}

.faq-list {
  display: grid;
  gap: var(--sp-3);
  padding: 0 var(--sp-6) var(--sp-6);
}

.faq-item {
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  background: var(--glass-bg);
  overflow: hidden;
}

.faq-question {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--sp-4);
  padding: var(--sp-4) var(--sp-5);
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 600;
  text-align: left;
}

.faq-answer {
  padding: 0 var(--sp-5) var(--sp-5);
}

.faq-answer p {
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.8;
}

.faq-expand-enter-active,
.faq-expand-leave-active {
  transition: all 0.24s ease;
}

.faq-expand-enter-from,
.faq-expand-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.support-list {
  display: grid;
  gap: var(--sp-3);
  padding: 0 var(--sp-6) var(--sp-6);
}

.support-item {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-4) var(--sp-5);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  background: var(--glass-bg);
  color: var(--text-secondary);
  font-size: var(--text-sm);
}
</style>
