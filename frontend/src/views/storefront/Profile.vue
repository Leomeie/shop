<template>
  <div class="store-page">
    <StorePageHeader eyebrow="Account" icon="user" title="个人资料" subtitle="管理你的账户信息、显示名称与基础联系方式。" compact />

    <div class="store-page-body">
      <div class="container">
        <div class="account-shell">
          <StoreAccountNav />

          <div class="account-content">
            <section class="store-surface store-surface--soft profile-panel">
              <div class="profile-header">
                <div class="avatar-large">
                  <span>{{ (form.nickname || form.username || 'U').charAt(0).toUpperCase() }}</span>
                </div>
                <div class="profile-intro">
                  <h2>{{ form.nickname || form.username }}</h2>
                  <p>@{{ form.username }}</p>
                </div>
              </div>

              <form class="profile-form" @submit.prevent="handleSave">
                <div class="field">
                  <label>用户名</label>
                  <input :value="form.username" disabled />
                </div>
                <div class="field">
                  <label>昵称</label>
                  <input v-model="form.nickname" type="text" placeholder="设置一个更适合展示的名称" />
                </div>
                <div class="field">
                  <label>手机号</label>
                  <input v-model="form.phone" type="text" placeholder="输入你的手机号" />
                </div>
                <button class="save-btn" type="submit" :disabled="loading">
                  <AnimatedIcons v-if="loading" name="spinner" :size="18" speed="fast" />
                  <span v-else class="save-btn__content">
                    保存修改
                    <AnimatedIcons name="check" :size="18" />
                  </span>
                </button>
              </form>
            </section>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import AnimatedIcons from '../../components/AnimatedIcons.vue'
import StoreAccountNav from '../../components/StoreAccountNav.vue'
import StorePageHeader from '../../components/StorePageHeader.vue'
import { useUserStore } from '../../stores/user'

const userStore = useUserStore()
const loading = ref(false)
const form = ref({ username: '', nickname: '', phone: '' })

onMounted(async () => {
  if (!userStore.userInfo) await userStore.fetchUserInfo()
  form.value = { ...userStore.userInfo }
})

async function handleSave() {
  loading.value = true
  try {
    await userStore.fetchUserInfo()
    ElMessage.success('资料已同步')
  } catch {} finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-panel {
  padding: var(--sp-6);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: var(--sp-5);
  padding-bottom: var(--sp-6);
  border-bottom: 1px solid var(--glass-border);
  margin-bottom: var(--sp-6);
}

.avatar-large {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 84px;
  height: 84px;
  border-radius: 999px;
  background: linear-gradient(135deg, var(--accent), var(--accent-purple));
  color: var(--white);
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 800;
}

.profile-intro h2 {
  color: var(--text-primary);
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
}

.profile-intro p {
  margin-top: var(--sp-1);
  color: var(--text-muted);
  font-size: var(--text-sm);
}

.profile-form {
  display: grid;
  gap: var(--sp-5);
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
  font-size: var(--text-sm);
}

.field input:focus {
  outline: none;
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.12);
}

.field input:disabled {
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-muted);
}

.save-btn {
  width: 100%;
  height: 48px;
  border: none;
  border-radius: 14px;
  background: var(--gradient-blue);
  color: var(--white);
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: 700;
}

.save-btn__content {
  display: inline-flex;
  align-items: center;
  gap: var(--sp-2);
}
</style>
