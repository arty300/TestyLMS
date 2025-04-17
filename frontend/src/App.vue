<template>
  <div>
    <header>
      <nav>
        <router-link to="/">Home</router-link> |
        <router-link to="/courses">Courses</router-link> |
        <router-link to="/profile">Profile</router-link> |
        <template v-if="isLoggedIn">
          <a href="#" @click.prevent="logout">Logout</a>
        </template>
        <template v-else>
          <router-link to="/login">Login</router-link> |
        </template>
      </nav>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token')
    },
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
      alert('Logged out successfully!')
    },
  },
}
</script>

<style scoped>
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  background-color: #f8f9fa;
  border-bottom: 1px solid #e7e7e7;
  padding: 1rem;
  z-index: 1000;
}

nav {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 1rem;
}

nav a {
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
}

nav a.router-link-exact-active {
  color: #42b983;
}

nav a:hover {
  color: #42b983;
}

main {
  margin-top: 60px;
  padding: 1rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}
</style>