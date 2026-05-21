<template>
  <span :class="['status-badge', `status-badge--${normalized}`, `status-badge--${size}`, { 'has-dot': dot }]">
    <span v-if="dot" class="status-badge__dot" />
    <span>{{ label }}</span>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  status: { type: String, default: 'neutral' },
  size: { type: String, default: 'md' },
  dot: { type: Boolean, default: true },
})

const normalized = computed(() => {
  const map = {
    active: 'success',
    completed: 'success',
    success: 'success',
    paid: 'info',
    info: 'info',
    pending: 'warning',
    warning: 'warning',
    draft: 'warning',
    inactive: 'neutral',
    neutral: 'neutral',
    cancelled: 'danger',
    error: 'danger',
    danger: 'danger',
  }

  return map[props.status] || 'neutral'
})
</script>
