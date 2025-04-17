<template>
  <div>
    <h2>Profile</h2>
    <p>Username: {{ user.username }}</p>
    <p>Points: {{ user.points }}</p>
    <p>Role: {{ user.role }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return { user: {} }
  },
  async created() {
    const token = localStorage.getItem('token')
    if (!token) {
      this.$router.push('/login')
      return
    }
    try {
      const { data } = await axios.get(`${import.meta.env.VITE_API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      this.user = data
    } catch (error) {
      console.error(error)
      this.$router.push('/login')
    }
  },
}
</script>

<style scoped>
p {
  margin: 0.5rem 0;
}
</style>