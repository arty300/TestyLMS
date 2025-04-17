<template>
  <div class="container mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">Courses</h2>
    <div v-if="isAdmin" class="mb-4">
      <router-link
        to="/admin/panel"
        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
      >
        Manage Courses
      </router-link>
    </div>
    <ul class="list-none">
      <li v-for="course in courses" :key="course.id" class="mb-2">
        <router-link
          :to="`/courses/${course.id}`"
          class="text-blue-600 hover:underline"
        >
          {{ course.title }} (Groups: {{ course.allowedGroups.join(', ') || 'All' }})
        </router-link>
      </li>
      <li v-if="!courses.length" class="text-gray-500">No courses available.</li>
    </ul>
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
          headers: { Authorization: `Bearer ${token}` },
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
.mb-4 {
  margin-bottom: 1rem;
}
</style>