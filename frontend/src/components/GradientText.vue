<template>
  <span
    :class="[
      'gradient-text',
      `gradient-text--${variant}`,
      customClass
    ]"
  >
    <slot />
  </span>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'blue',
    validator: (value) => ['blue', 'purple', 'pink'].includes(value),
  },
  customClass: {
    type: String,
    default: '',
  },
});
</script>

<style scoped>
.gradient-text {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-purple) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  display: inline-block;
}

.gradient-text--blue {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.gradient-text--purple {
  background: linear-gradient(135deg, var(--accent-purple) 0%, var(--accent-pink) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>