<template>
  <div ref="containerRef" class="particle-bg">
    <div
      v-for="(particle, i) in particles"
      :key="i"
      class="particle"
      :style="{
        left: `${particle.x}%`,
        top: `${particle.y}%`,
        width: `${particle.size}px`,
        height: `${particle.size}px`,
        animationDelay: `${particle.delay}s`,
        animationDuration: `${particle.duration}s`,
        background: particle.color,
      }"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const containerRef = ref(null);
const particles = ref([]);

const particleCount = 50;

const generateParticles = () => {
  const newParticles = [];
  const colors = [
    'rgba(59, 130, 246, 0.6)',
    'rgba(139, 92, 246, 0.6)',
    'rgba(236, 72, 153, 0.6)',
  ];

  for (let i = 0; i < particleCount; i++) {
    newParticles.push({
      x: Math.random() * 100,
      y: Math.random() * 100,
      size: Math.random() * 4 + 2,
      delay: Math.random() * 5,
      duration: Math.random() * 3 + 4,
      color: colors[Math.floor(Math.random() * colors.length)],
    });
  }

  particles.value = newParticles;
};

onMounted(() => {
  generateParticles();
});
</script>

<style scoped>
.particle-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.particle {
  position: absolute;
  border-radius: 50%;
  animation: floatParticle 6s ease-in-out infinite;
  opacity: 0.6;
}

@keyframes floatParticle {
  0%, 100% {
    transform: translate(0, 0) scale(1);
    opacity: 0.6;
  }
  33% {
    transform: translate(30px, -30px) scale(1.2);
    opacity: 0.8;
  }
  66% {
    transform: translate(-15px, 15px) scale(0.8);
    opacity: 0.4;
  }
}
</style>