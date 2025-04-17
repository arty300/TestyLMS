<template>
  <div class="home-container" :key="$route.path">
    <h2 class="animate-slide-up">Welcome to LMS</h2>
    <p class="animate-slide-up">Learn and grow with our courses!</p>
  </div>
</template>

<style scoped>
.home-container {
  text-align: center;
  padding: 2rem;
}

h2 {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 1rem;
}
p {
  color: #666;
  font-size: 1.2rem;
}

.animate-slide-up {
  opacity: 0;
  transform: translateY(50px);
  animation: slideUp 1s ease-out forwards;
}

.animate-slide-up:nth-child(2) {
  animation-delay: 0.3s;
}

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>