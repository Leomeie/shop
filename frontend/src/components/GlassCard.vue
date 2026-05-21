<template>
  <div
    :class="[
      'glass-card',
      {
        'glass-card--hover': hover,
        'glass-card--clickable': clickable,
      },
      customClass
    ]"
    @click="handleClick"
  >
    <slot />
  </div>
</template>

<script setup>
defineProps({
  hover: {
    type: Boolean,
    default: true,
  },
  clickable: {
    type: Boolean,
    default: false,
  },
  customClass: {
    type: String,
    default: '',
  },
});

const emit = defineEmits(['click']);

const handleClick = (e) => {
  emit('click', e);
};
</script>

<style scoped>
.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  box-shadow: var(--glass-shadow);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-card--hover:hover {
  border-color: var(--glass-border-active);
  transform: translateY(-2px);
  box-shadow: var(--glass-shadow-hover);
}

.glass-card--clickable {
  cursor: pointer;
}

.glass-card--clickable:active {
  transform: scale(0.98);
}
</style>