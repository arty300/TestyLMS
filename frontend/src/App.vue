<template>
  <div id="app">
    <nav class="bg-green-700 text-white shadow-lg">
      <div class="container mx-auto px-6 py-3 flex justify-between items-center">
        <div class="flex items-center">
          <router-link to="/" class="text-2xl font-bold text-green-100 mr-8">LMS</router-link>
          <div class="hidden md:flex space-x-6">
            <router-link to="/courses" class="hover:text-green-100 transition duration-200">Курсы</router-link>
            <router-link v-if="isAdmin" to="/admin/panel" class="hover:text-green-100 transition duration-200">Админ-панель</router-link>
            <router-link v-if="isLoggedIn" to="/profile" class="hover:text-green-100 transition duration-200">Профиль</router-link>
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <span v-if="user" class="bg-green-100 text-green-900 text-sm font-semibold px-3 py-1 rounded-full">Баллы: {{ user.points }}</span>
          <router-link v-if="!isLoggedIn" to="/login" class="text-sm bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded transition duration-200">Войти</router-link>
          <button v-if="isLoggedIn" @click="logout" class="text-sm bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded transition duration-200">Выйти</button>
        </div>
        <button class="md:hidden focus:outline-none" @click="toggleMobileMenu">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
          </svg>
        </button>
      </div>
      <!-- Мобильное меню -->
      <div v-if="mobileMenuOpen" class="md:hidden bg-green-600 px-6 py-3 space-y-2">
        <router-link to="/courses" class="block hover:text-green-100 transition duration-200" @click="toggleMobileMenu">Курсы</router-link>
        <router-link v-if="isAdmin" to="/admin/panel" class="block hover:text-green-100 transition duration-200" @click="toggleMobileMenu">Админ-панель</router-link>
        <router-link v-if="isLoggedIn" to="/profile" class="block hover:text-green-100 transition duration-200" @click="toggleMobileMenu">Профиль</router-link>
        <router-link v-if="!isLoggedIn" to="/login" class="block hover:text-green-100 transition duration-200" @click="toggleMobileMenu">Войти</router-link>
        <button v-if="isLoggedIn" @click="logout" class="block text-left hover:text-green-100 transition duration-200 w-full">Выйти</button>
      </div>
    </nav>
    <router-view @user-updated="updateUser"></router-view>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
      user: null,
      apiBaseUrl: `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}`,
      mobileMenuOpen: false
    }
  },
  created() {
    this.checkLoginStatus()
    if (this.isLoggedIn) {
      this.fetchUser()
    }
  },
  methods: {
    checkLoginStatus() {
      const token = localStorage.getItem('token')
      this.isLoggedIn = !!token
      if (token) {
        // Проверяем роль пользователя из localStorage или делаем запрос
        const storedUser = localStorage.getItem('user')
        if (storedUser) {
          const user = JSON.parse(storedUser)
          this.isAdmin = user.role === 'admin'
          this.user = user
        }
      }
    },
    async fetchUser() {
      try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No authorization token found')
        const { data } = await axios.get(`${this.apiBaseUrl}/users/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.user = data
        this.isAdmin = data.role === 'admin'
        localStorage.setItem('user', JSON.stringify(data)) // Сохраняем данные пользователя
      } catch (error) {
        console.error('Failed to fetch user data:', error.response || error)
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        this.isLoggedIn = false
        this.user = null
        this.isAdmin = false
        this.$router.push('/login')
      }
    },
    logout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.isLoggedIn = false
      this.user = null
      this.isAdmin = false
      this.$router.push('/login')
    },
    updateUser(updatedUser) {
      this.user = updatedUser
      localStorage.setItem('user', JSON.stringify(updatedUser))
    },
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
}
nav {
  background-color: #2f855a;
}
.container {
  max-width: 1200px;
}
.text-2xl {
  font-size: 1.5rem;
}
.font-bold {
  font-weight: 700;
}
.mr-8 {
  margin-right: 2rem;
}
.space-x-6 > * + * {
  margin-left: 1.5rem;
}
.px-6 {
  padding-left: 1.5rem;
  padding-right: 1.5rem;
}
.py-3 {
  padding-top: 0.75rem;
  padding-bottom: 0.75rem;
}
.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
.text-green-100 {
  color: #f0fff4;
}
.hover\:text-green-100:hover {
  color: #f0fff4;
}
.bg-green-100 {
  background-color: #c6f6d5;
}
.text-green-900 {
  color: #22543d;
}
.text-sm {
  font-size: 0.875rem;
}
.font-semibold {
  font-weight: 600;
}
.px-3 {
  padding-left: 0.75rem;
  padding-right: 0.75rem;
}
.py-1 {
  padding-top: 0.25rem;
  padding-bottom: 0.25rem;
}
.rounded-full {
  border-radius: 9999px;
}
.bg-green-500 {
  background-color: #48bb78;
}
.hover\:bg-green-600:hover {
  background-color: #38a169;
}
.bg-red-500 {
  background-color: #f56565;
}
.hover\:bg-red-600:hover {
  background-color: #e53e3e;
}
.text-white {
  color: #ffffff;
}
.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
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
.flex {
  display: flex;
}
.items-center {
  align-items: center;
}
.justify-between {
  justify-content: space-between;
}
.space-x-4 > * + * {
  margin-left: 1rem;
}
.hidden {
  display: none;
}
.md\:hidden {
  @media (min-width: 768px) {
    display: none;
  }
}
.md\:flex {
  @media (min-width: 768px) {
    display: flex;
  }
}
.block {
  display: block;
}
.text-left {
  text-align: left;
}
.w-full {
  width: 100%;
}
.space-y-2 > * + * {
  margin-top: 0.5rem;
}
.bg-green-600 {
  background-color: #38a169;
}
.bg-green-700 {
  background-color: #2f855a;
}
</style>