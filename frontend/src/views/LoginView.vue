<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label>Username:</label>
        <input v-model="form.username" type="text" placeholder="Enter username" required />
      </div>
      <div>
        <label>Password:</label>
        <input v-model="form.password" type="password" placeholder="Enter password" required />
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
    }
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/users/login`, this.form)
        localStorage.setItem('token', response.data.access_token)
        this.$router.push('/courses')
        alert('Login successful!')
      } catch (error) {
        console.error(error)
        alert('Invalid username or password.')
      }
    },
  },
}
</script>

<style scoped>
div {
  margin: 1rem 0;
}
label {
  display: inline-block;
  width: 100px;
}
input {
  padding: 0.5rem;
  width: 200px;
}
button {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #3aa876;
}
</style>