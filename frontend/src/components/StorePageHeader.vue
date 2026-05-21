<template>
  <section :class="['store-view-header', `store-view-header--${tone}`, { 'store-view-header--compact': compact }]">
    <div class="container store-view-header__inner" :class="[`is-${align}`]">
      <div class="store-view-header__copy">
        <div v-if="eyebrow || icon" class="store-view-header__eyebrow">
          <AnimatedIcons v-if="icon" :name="icon" :size="14" />
          <span v-if="eyebrow">{{ eyebrow }}</span>
        </div>

        <div class="store-view-header__title-row">
          <h1 class="store-view-header__title">{{ title }}</h1>
          <span v-if="badge" class="store-view-header__badge">{{ badge }}</span>
        </div>

        <p v-if="subtitle" class="store-view-header__subtitle">{{ subtitle }}</p>

        <div v-if="$slots.meta" class="store-view-header__meta">
          <slot name="meta" />
        </div>
      </div>

      <div v-if="$slots.actions" class="store-view-header__actions">
        <slot name="actions" />
      </div>
    </div>
  </section>
</template>

<script setup>
import AnimatedIcons from './AnimatedIcons.vue'

defineProps({
  eyebrow: { type: String, default: '' },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  badge: { type: String, default: '' },
  icon: { type: String, default: '' },
  tone: { type: String, default: 'light' },
  compact: { type: Boolean, default: false },
  align: { type: String, default: 'left' },
})
</script>
