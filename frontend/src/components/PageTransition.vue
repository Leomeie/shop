<template>
  <Transition mode="out-in" :css="false" @leave="onLeave" @enter="onEnter">
    <slot />
  </Transition>
</template>

<script setup>
import { usePageTransition } from '../composables/usePageTransition'

const { onLeave, onEnter } = usePageTransition()
</script>
