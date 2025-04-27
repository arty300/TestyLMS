<template>
  <div class="container mx-auto px-6 py-8">
    <h2 class="text-3xl font-bold text-green-800 mb-6">Профиль пользователя</h2>
    <div v-if="!user" class="text-center py-10 text-gray-500">
      <p>Данные пользователя недоступны. Пожалуйста, войдите в систему.</p>
      <router-link to="/login" class="inline-block bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded transition duration-200 mt-4">Войти</router-link>
    </div>
    <div v-else class="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
      <div class="flex flex-col md:flex-row items-center md:items-start gap-6">
        <div class="w-32 h-32 bg-gray-200 rounded-full flex items-center justify-center text-gray-500">
          <span class="text-2xl">{{ user.username ? user.username.charAt(0).toUpperCase() : 'U' }}</span>
          <!-- Здесь можно добавить аватар пользователя, если он есть -->
        </div>
        <div class="flex-1">
          <h3 class="text-2xl font-semibold text-gray-800 mb-2">{{ user.username }}</h3>
          <p class="text-gray-600 mb-1"><span class="font-medium">Роль:</span> {{ user.role === 'admin' ? 'Администратор' : 'Пользователь' }}</p>
          <p class="text-gray-600 mb-4"><span class="font-medium">Баллы:</span> <span class="bg-green-100 text-green-900 px-2 py-1 rounded-full text-sm">{{ user.points }}</span></p>
        </div>
      </div>
      <div class="mt-8">
        <h4 class="text-xl font-semibold text-gray-800 mb-4">Прогресс по курсам</h4>
        <div v-if="courses.length === 0" class="text-gray-500 text-center py-4">
          <p>Вы пока не записаны на курсы.</p>
        </div>
        <div v-else class="space-y-4">
          <div v-for="course in coursesWithProgress" :key="course.id" class="border border-gray-200 rounded-lg p-4 flex flex-col md:flex-row justify-between items-center gap-4">
            <div>
              <h5 class="font-medium text-gray-800">{{ course.title }}</h5>
              <p class="text-sm text-gray-600">Преподаватель: {{ course.instructor }}</p>
            </div>
            <div class="w-full md:w-1/2">
              <div class="bg-gray-200 rounded-full h-2.5">
                <div class="bg-green-600 h-2.5 rounded-full" :style="{ width: course.progress + '%' }"></div>
              </div>
              <p class="text-sm text-gray-500 text-right mt-1">{{ course.progress }}% завершено ({{ course.unlockedSections }} из {{ course.totalSections }} разделов)</p>
            </div>
          </div>
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
      user: {},
      courses: [],
      apiBaseUrl: `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}`
    }
  },
  computed: {
    coursesWithProgress() {
      return this.courses.map(course => {
        const totalSections = course.hiddenSections ? course.hiddenSections.length : 0;
        const unlockedSections = this.user.unlockedSections && this.user.unlockedSections[course.id] ? this.user.unlockedSections[course.id].length : 0;
        const progress = totalSections > 0 ? Math.round((unlockedSections / totalSections) * 100) : 0;
        return {
          ...course,
          progress,
          unlockedSections,
          totalSections
        };
      });
    }
  },
  async created() {
    await this.fetchUser()
    await this.fetchUserCourses()
  },
  methods: {
    async fetchUser() {
      try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No authorization token found')
        const { data } = await axios.get(`${this.apiBaseUrl}/users/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.user = data
      } catch (error) {
        console.error('Failed to fetch user data:', error.response || error)
        this.user = null
        this.$router.push('/login')
      }
    },
    async fetchUserCourses() {
      try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No authorization token found')
        const { data } = await axios.get(`${this.apiBaseUrl}/courses`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.courses = data
      } catch (error) {
        console.error('Failed to fetch user courses:', error.response || error)
        this.courses = []
      }
    }
  }
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
.bg-white {
  background-color: #ffffff;
}
.rounded-lg {
  border-radius: 0.5rem;
}
.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.p-6 {
  padding: 1.5rem;
}
.max-w-2xl {
  max-width: 42rem;
}
.mx-auto {
  margin-left: auto;
  margin-right: auto;
}
.flex {
  display: flex;
}
.flex-col {
  flex-direction: column;
}
.md\:flex-row {
  @media (min-width: 768px) {
    flex-direction: row;
  }
}
.items-center {
  align-items: center;
}
.md\:items-start {
  @media (min-width: 768px) {
    align-items: flex-start;
  }
}
.gap-6 {
  gap: 1.5rem;
}
.w-32 {
  width: 8rem;
}
.h-32 {
  height: 8rem;
}
.bg-gray-200 {
  background-color: #e2e8f0;
}
.rounded-full {
  border-radius: 9999px;
}
.text-2xl {
  font-size: 1.5rem;
}
.flex-1 {
  flex: 1 1 0%;
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
.mb-1 {
  margin-bottom: 0.25rem;
}
.font-medium {
  font-weight: 500;
}
.mb-4 {
  margin-bottom: 1rem;
}
.bg-green-100 {
  background-color: #c6f6d5;
}
.text-green-900 {
  color: #22543d;
}
.px-2 {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
}
.py-1 {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}
.text-sm {
  font-size: 0.875rem;
}
.space-x-3 > * + * {
  margin-left: 0.75rem;
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
.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
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
.bg-gray-200 {
  background-color: #e2e8f0;
}
.hover\:bg-gray-300:hover {
  background-color: #cbd5e1;
}
.text-gray-800 {
  color: #2d3748;
}
.mt-8 {
  margin-top: 2rem;
}
.text-xl {
  font-size: 1.25rem;
}
.py-4 {
  padding-top: 1rem;
  padding-bottom: 1rem;
}
.space-y-4 > * + * {
  margin-top: 1rem;
}
.border {
  border-width: 1px;
}
.border-gray-200 {
  border-color: #e2e8f0;
}
.justify-between {
  justify-content: space-between;
}
.gap-4 {
  gap: 1rem;
}
.w-full {
  width: 100%;
}
.md\:w-1\/2 {
  @media (min-width: 768px) {
    width: 50%;
  }
}
.h-2\.5 {
  height: 0.625rem;
}
.mt-1 {
  margin-top: 0.25rem;
}
.text-right {
  text-align: right;
}
.inline-block {
  display: inline-block;
}
.mt-4 {
  margin-top: 1rem;
}
</style>