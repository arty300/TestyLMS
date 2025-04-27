<template>
  <div class="container mx-auto px-6 py-8">
    <h2 class="text-3xl font-bold text-green-800 mb-6">Доступные курсы</h2>
    <div v-if="isAdmin" class="mb-6">
      <router-link
        to="/admin/panel"
        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition duration-200"
      >
        Управление курсами
      </router-link>
    </div>
    <div v-if="courses.length === 0" class="text-center py-10 text-gray-500">
      <p>Курсы пока недоступны. Пожалуйста, зайдите позже.</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="course in courses" :key="course.id" class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
        <div class="h-48 bg-gray-200 flex items-center justify-center">
          <span class="text-gray-500 text-lg">Изображение курса</span>
          <!-- Здесь можно добавить обложку курса, если она есть в данных -->
        </div>
        <div class="p-4">
          <h3 class="text-xl font-semibold text-gray-800 mb-2">{{ course.title }}</h3>
          <p class="text-gray-600 mb-2 line-clamp-2">{{ course.description }}</p>
          <p class="text-sm text-gray-500 mb-4">Группы: {{ course.allowedGroups.join(', ') || 'Все' }}</p>
          <router-link :to="`/courses/${course.id}`" class="block w-full text-center bg-green-600 hover:bg-green-700 text-white py-2 rounded transition duration-200">
            Перейти к курсу
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      courses: [],
      isAdmin: false,
    }
  },
  async created() {
    await this.fetchCourses()
    const token = localStorage.getItem('token')
    if (token) {
      try {
        const { data } = await axios.get(`${import.meta.env.VITE_API_URL}/users/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.isAdmin = data.role === 'admin'
      } catch (error) {
        console.error('Failed to fetch user:', error)
        localStorage.removeItem('token')
      }
    }
  },
  methods: {
    async fetchCourses() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/courses`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        })
        this.courses = response.data
        console.log('Courses fetched in CoursesView:', this.courses)
      } catch (error) {
        console.error('Failed to fetch courses:', error.response || error)
        this.courses = []
      }
    },
  },
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}
.text-3xl {
  font-size: 1.875rem;
}
.font-bold {
  font-weight: 700;
}
.text-green-800 {
  color: #276749;
}
.mb-6 {
  margin-bottom: 1.5rem;
}
.text-center {
  text-align: center;
}
.py-10 {
  padding-top: 2.5rem;
  padding-bottom: 2.5rem;
}
.text-gray-500 {
  color: #718096;
}
.grid {
  display: grid;
}
.grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}
.md\:grid-cols-2 {
  @media (min-width: 768px) {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
.lg\:grid-cols-3 {
  @media (min-width: 1024px) {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
.gap-6 {
  gap: 1.5rem;
}
.bg-white {
  background-color: #ffffff;
}
.rounded-lg {
  border-radius: 0.5rem;
}
.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.overflow-hidden {
  overflow: hidden;
}
.hover\:shadow-lg:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
.transition-shadow {
  transition-property: box-shadow;
}
.duration-300 {
  transition-duration: 300ms;
}
.h-48 {
  height: 12rem;
}
.bg-gray-200 {
  background-color: #e2e8f0;
}
.flex {
  display: flex;
}
.items-center {
  align-items: center;
}
.justify-center {
  justify-content: center;
}
.text-lg {
  font-size: 1.125rem;
}
.p-4 {
  padding: 1rem;
}
.text-xl {
  font-size: 1.25rem;
}
.font-semibold {
  font-weight: 600;
}
.text-gray-800 {
  color: #2d3748;
}
.mb-2 {
  margin-bottom: 0.5rem;
}
.text-gray-600 {
  color: #4a5568;
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.text-sm {
  font-size: 0.875rem;
}
.mb-4 {
  margin-bottom: 1rem;
}
.block {
  display: block;
}
.w-full {
  width: 100%;
}
.text-center {
  text-align: center;
}
.bg-green-600 {
  background-color: #38a169;
}
.hover\:bg-green-700:hover {
  background-color: #2f855a;
}
.text-white {
  color: #ffffff;
}
.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}
.rounded {
  border-radius: 0.25rem;
}
.transition {
  transition-property: all;
}
.duration-200 {
  transition-duration: 200ms;
}
</style>
