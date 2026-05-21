<template>
  <div class="auth-shell">
    <section class="auth-shell__aside">
      <router-link to="/" class="auth-brand">
        <span class="auth-brand__mark">S</span>
        <span class="auth-brand__text">ShopEase</span>
      </router-link>

      <div class="auth-shell__copy">
        <span class="auth-shell__eyebrow">Premium Commerce</span>
        <h1>回到你的数字资产工作台</h1>
        <p>登录后继续查看订单、下载内容和收藏资源，保持创作流程不断档。</p>

        <div class="benefit-list">
          <div v-for="feature in visualFeatures" :key="feature.text" class="benefit-item">
            <AnimatedIcons :name="feature.icon" :size="18" />
            <span>{{ feature.text }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="auth-shell__form-area">
      <div class="auth-card">
        <div class="auth-card__header">
          <span class="auth-shell__eyebrow">Login</span>
          <h2>登录</h2>
          <p>输入账户信息，继续访问你的资源与交易记录。</p>
        </div>

        <div class="helper-panel">
          <div class="helper-panel__label">提示</div>
          <p>管理员请直接使用用户名登录，例如：`admin`，不要使用昵称或邮箱代替用户名。</p>
        </div>

        <div v-if="summaryLines.length" class="form-alert">
          <div class="form-alert__title">登录失败，请检查以下问题：</div>
          <ul>
            <li v-for="line in summaryLines" :key="line">{{ line }}</li>
          </ul>
        </div>

        <form class="auth-form" @submit.prevent="handleLogin">
          <div class="field">
            <label>用户名</label>
            <input v-model="form.username" type="text" placeholder="输入用户名" @blur="validateField('username')" />
            <p v-if="fieldErrors.username" class="field-error">{{ fieldErrors.username }}</p>
            <p v-else class="field-hint">普通用户和管理员都使用用户名登录。</p>
          </div>

          <div class="field">
            <label>密码</label>
            <input v-model="form.password" type="password" placeholder="输入密码" @blur="validateField('password')" />
            <p v-if="fieldErrors.password" class="field-error">{{ fieldErrors.password }}</p>
            <p v-else class="field-hint">密码长度至少 6 位，注意检查是否有多余空格。</p>
          </div>

          <button class="submit-btn" type="submit" :disabled="loading">
            <AnimatedIcons v-if="loading" name="spinner" :size="18" speed="fast" />
            <span v-else class="submit-btn__content">
              登录
              <AnimatedIcons name="arrow-right" :size="18" />
            </span>
          </button>
        </form>

        <p class="auth-switch">还没有账户？<router-link to="/register">立即注册</router-link></p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import { useUserStore } from '../../stores/user'
import { parseAuthApiError, validateLoginForm } from '../../utils/authFeedback'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const loading = ref(false)
const form = reactive({ username: '', password: '' })
const fieldErrors = reactive({ username: '', password: '' })
const summaryLines = ref([])

const visualFeatures = [
  { icon: 'download', text: '统一查看下载与交付记录' },
  { icon: 'package', text: '快速回到订单与支付进度' },
  { icon: 'shield', text: '账户与交易状态持续同步' },
]

function applyValidation(result) {
  fieldErrors.username = result.fieldErrors.username || ''
  fieldErrors.password = result.fieldErrors.password || ''
  summaryLines.value = result.summaryLines || []
  return result.valid
}

function validateField(name) {
  const result = validateLoginForm(form)
  if (name === 'username') {
    fieldErrors.username = result.fieldErrors.username || ''
  }
  if (name === 'password') {
    fieldErrors.password = result.fieldErrors.password || ''
  }
}

async function handleLogin() {
  if (!applyValidation(validateLoginForm(form))) return

  loading.value = true
  summaryLines.value = []
  try {
    await userStore.login({ username: form.username.trim(), password: form.password })
    ElMessage.success('登录成功')
    router.push(route.query.redirect || '/')
  } catch (error) {
    const parsed = parseAuthApiError(error, 'login')
    fieldErrors.username = parsed.fieldErrors.username || ''
    fieldErrors.password = parsed.fieldErrors.password || ''
    summaryLines.value = parsed.summaryLines
    ElMessage.error(parsed.summaryLines[0] || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-shell {
  display: grid;
  grid-template-columns: minmax(360px, 44vw) minmax(0, 1fr);
  min-height: 100vh;
  background: var(--gradient-tech);
}

.auth-shell__aside {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: var(--sp-8);
  background:
    radial-gradient(circle at top left, rgba(59, 130, 246, 0.18), transparent 40%),
    var(--surface-1);
  border-right: 1px solid var(--glass-border);
}

.auth-brand {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-3);
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
}

.auth-brand__mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 14px;
  background: var(--gradient-blue);
  color: var(--white);
}

.auth-shell__copy {
  max-width: 440px;
}

.auth-shell__eyebrow {
  display: inline-flex;
  margin-bottom: var(--sp-3);
  color: var(--accent);
  font-family: var(--font-display);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.auth-shell__copy h1 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: clamp(2.2rem, 4vw, 3.6rem);
  font-weight: 800;
  line-height: 1.05;
  letter-spacing: -0.05em;
}

.auth-shell__copy p {
  margin-top: var(--sp-5);
  color: var(--text-secondary);
  font-size: var(--text-lg);
  line-height: 1.8;
}

.benefit-list {
  display: grid;
  gap: var(--sp-3);
  margin-top: var(--sp-8);
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: var(--sp-3);
  padding: var(--sp-4);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  background: var(--glass-bg);
  color: var(--text-secondary);
  font-size: var(--text-sm);
}

.auth-shell__form-area {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--sp-8);
}

.auth-card {
  width: 100%;
  max-width: 460px;
  padding: var(--sp-8);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  background: var(--glass-bg);
  box-shadow: var(--glass-shadow);
}

.auth-card__header h2 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: 800;
  letter-spacing: -0.04em;
}

.auth-card__header p {
  margin-top: var(--sp-3);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.8;
}

.helper-panel,
.form-alert {
  margin-top: var(--sp-5);
  padding: var(--sp-4);
  border-radius: 16px;
}

.helper-panel {
  border: 1px solid rgba(59, 130, 246, 0.24);
  background: rgba(59, 130, 246, 0.08);
}

.helper-panel__label,
.form-alert__title {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 700;
}

.helper-panel p {
  margin-top: var(--sp-2);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  line-height: 1.8;
}

.form-alert {
  border: 1px solid rgba(214, 69, 69, 0.24);
  background: rgba(214, 69, 69, 0.08);
}

.form-alert ul {
  margin-top: var(--sp-2);
  padding-left: 18px;
  color: #f87171;
  font-size: var(--text-sm);
  line-height: 1.8;
}

.auth-form {
  display: grid;
  gap: var(--sp-5);
  margin-top: var(--sp-7);
}

.field {
  display: grid;
  gap: var(--sp-2);
}

.field label {
  color: var(--text-secondary);
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: 600;
}

.field input {
  width: 100%;
  height: 48px;
  border: 1px solid var(--glass-border);
  border-radius: 14px;
  background: var(--glass-bg);
  padding: 0 var(--sp-4);
  color: var(--text-primary);
}

.field input:focus {
  outline: none;
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.12);
}

.field-error {
  color: var(--error);
  font-size: var(--text-xs);
}

.field-hint {
  color: var(--text-muted);
  font-size: var(--text-xs);
}

.submit-btn {
  width: 100%;
  height: 50px;
  border: none;
  border-radius: 14px;
  background: var(--gradient-blue);
  color: var(--white);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.submit-btn__content {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
}

.auth-switch {
  margin-top: var(--sp-6);
  color: var(--text-secondary);
  font-size: var(--text-sm);
  text-align: center;
}

.auth-switch a {
  color: var(--accent);
  font-weight: 700;
}

@media (max-width: 960px) {
  .auth-shell {
    grid-template-columns: 1fr;
  }

  .auth-shell__aside {
    display: none;
    opacity: 0;
    transform: translateY(-20px);
    transition: opacity 0.3s ease, transform 0.3s ease;
  }
}
</style>
