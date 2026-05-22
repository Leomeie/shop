<template>
  <Teleport to="body">
    <Transition name="wechat-fade">
      <div v-if="visible" class="wechat-pay-overlay" @click.self="$emit('close')">
        <Transition name="wechat-slide" appear>
          <div v-if="visible" class="wechat-pay-modal">
            <div class="wechat-pay-header">
              <div class="wechat-pay-header__left">
                <svg class="wechat-pay-logo" viewBox="0 0 24 24" width="22" height="22" fill="none">
                  <path d="M8.5 3C4.91 3 2 5.46 2 8.5c0 1.68.89 3.18 2.28 4.16L3.5 15l2.56-1.28c.7.26 1.46.42 2.24.47-.15-.5-.24-1.03-.24-1.58C8.06 9.47 10.72 7 14 7c.34 0 .67.03 1 .08C14.33 4.72 11.66 3 8.5 3zm-3 4.5a.75.75 0 110-1.5.75.75 0 010 1.5zm5 0a.75.75 0 110-1.5.75.75 0 010 1.5zM22 12.5c0-2.76-2.69-5-6-5s-6 2.24-6 5 2.69 5 6 5c.72 0 1.41-.12 2.04-.34L21 19l-.62-2.48C21.28 15.62 22 14.14 22 12.5zm-8-1a.75.75 0 110-1.5.75.75 0 010 1.5zm4 0a.75.75 0 110-1.5.75.75 0 010 1.5z" fill="currentColor"/>
                </svg>
                <span class="wechat-pay-title">微信支付</span>
              </div>
              <button class="wechat-pay-close" type="button" @click="$emit('close')">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </div>

            <div class="wechat-pay-body">
              <div class="wechat-pay-amount">
                <span class="wechat-pay-amount__label">支付金额</span>
                <span class="wechat-pay-amount__value">¥{{ amount }}</span>
              </div>

              <div class="wechat-pay-qr">
                <div class="wechat-pay-qr__frame">
                  <img :src="'/images/money.jpg'" alt="微信收款码" class="wechat-pay-qr__img" />
                </div>
                <p class="wechat-pay-qr__tip">请使用微信扫一扫完成支付</p>
              </div>

              <div class="wechat-pay-countdown" v-if="countdown > 0">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                支付剩余时间 {{ formatTime(countdown) }}
              </div>

              <button
                class="wechat-pay-confirm"
                type="button"
                :disabled="confirming"
                @click="handleConfirm"
              >
                <span v-if="confirming" class="wechat-pay-confirm__spinner" />
                <span v-else>我已支付</span>
              </button>

              <p class="wechat-pay-footer-tip">支付完成后请点击上方按钮确认</p>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  amount: { type: [String, Number], default: '0.00' },
})

const emit = defineEmits(['close', 'confirmed'])

const confirming = ref(false)
const countdown = ref(300)
let timer = null

function formatTime(seconds) {
  const m = Math.floor(seconds / 60)
  const s = seconds % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
}

function handleConfirm() {
  confirming.value = true
  emit('confirmed')
}

onMounted(() => {
  timer = setInterval(() => {
    if (countdown.value > 0) {
      countdown.value--
    } else {
      clearInterval(timer)
    }
  }, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
.wechat-pay-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(6px);
}

.wechat-pay-modal {
  width: 380px;
  max-width: calc(100vw - 32px);
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.wechat-pay-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: #07C160;
  color: #fff;
}

.wechat-pay-header__left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.wechat-pay-logo {
  flex-shrink: 0;
}

.wechat-pay-title {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
}

.wechat-pay-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}

.wechat-pay-close:hover {
  background: rgba(255, 255, 255, 0.35);
}

.wechat-pay-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 28px 24px 24px;
}

.wechat-pay-amount {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  margin-bottom: 24px;
}

.wechat-pay-amount__label {
  color: #999;
  font-size: 13px;
}

.wechat-pay-amount__value {
  color: #333;
  font-family: var(--font-display);
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.wechat-pay-qr {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.wechat-pay-qr__frame {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  border: 1px solid #e8e8e8;
  overflow: hidden;
  background: #fafafa;
}

.wechat-pay-qr__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.wechat-pay-qr__tip {
  color: #999;
  font-size: 13px;
}

.wechat-pay-countdown {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 20px;
  padding: 8px 16px;
  border-radius: 20px;
  background: #f6f6f6;
  color: #666;
  font-size: 13px;
}

.wechat-pay-confirm {
  width: 100%;
  height: 48px;
  margin-top: 24px;
  border: none;
  border-radius: 12px;
  background: #07C160;
  color: #fff;
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s;
  position: relative;
}

.wechat-pay-confirm:hover:not(:disabled) {
  background: #06ad56;
}

.wechat-pay-confirm:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.wechat-pay-confirm__spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: wechat-spin 0.6s linear infinite;
}

.wechat-pay-footer-tip {
  margin-top: 16px;
  color: #bbb;
  font-size: 12px;
}

@keyframes wechat-spin {
  to { transform: rotate(360deg); }
}

/* Transitions */
.wechat-fade-enter-active,
.wechat-fade-leave-active {
  transition: opacity 0.25s ease;
}
.wechat-fade-enter-from,
.wechat-fade-leave-to {
  opacity: 0;
}

.wechat-slide-enter-active {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
}
.wechat-slide-leave-active {
  transition: transform 0.2s ease, opacity 0.15s ease;
}
.wechat-slide-enter-from {
  transform: scale(0.95) translateY(12px);
  opacity: 0;
}
.wechat-slide-leave-to {
  transform: scale(0.97) translateY(8px);
  opacity: 0;
}
</style>
