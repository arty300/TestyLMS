<template>
  <div class="home-container bg-gray-50 min-h-screen flex flex-col justify-center items-center px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl text-center">
      <h2 class="text-4xl md:text-5xl font-extrabold text-gray-900 animate-slide-up">Добро пожаловать в LMS</h2>
      <p class="text-lg md:text-xl text-gray-600 mt-4 animate-slide-up delay-300">Учитесь и развивайтесь с нашими курсами!</p>
      <div class="mt-8 flex justify-center animate-slide-up delay-500">
        <router-link
          to="/courses"
          class="px-6 py-3 bg-green-600 text-white font-medium rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition duration-200"
        >
          Посмотреть курсы
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.delay-300 {
  animation-delay: 0.3s;
}
.delay-500 {
  animation-delay: 0.5s;
}
.animate-slide-up {
  opacity: 0;
  transform: translateY(50px);
  animation: slideUp 1s ease-out forwards;
}

@keyframes slideUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>