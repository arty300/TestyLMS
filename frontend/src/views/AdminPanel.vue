<template>
  <div class="container mx-auto p-6 bg-gray-50 min-h-screen">
    <h2 class="text-3xl font-bold text-gray-800 mb-6">Admin Panel</h2>
    <div class="tabs flex border-b border-gray-200 mb-8">
      <button
        :class="{ 'border-b-2 border-green-600 text-green-600': activeTab === 'courses' }"
        class="tab px-4 py-2 text-lg font-medium"
        @click="activeTab = 'courses'"
      >
        Courses
      </button>
      <button
        :class="{ 'border-b-2 border-green-600 text-green-600': activeTab === 'users' }"
        class="tab px-4 py-2 text-lg font-medium"
        @click="activeTab = 'users'"
      >
        Users
      </button>
      <button
        :class="{ 'border-b-2 border-green-600 text-green-600': activeTab === 'groups' }"
        class="tab px-4 py-2 text-lg font-medium"
        @click="activeTab = 'groups'"
      >
        Groups
      </button>
    </div>

    <!-- Courses Tab -->
    <div v-if="activeTab === 'courses'" class="bg-white rounded-lg shadow p-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Manage Courses</h3>
      <div class="flex justify-between mb-4">
        <router-link
          to="/admin/courses"
          class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
        >
          Create New Course
        </router-link>
        <div>
          <label class="text-gray-600 mr-2">Filter by Group:</label>
          <select v-model="courseGroupFilter" class="p-2 border rounded">
            <option value="">All Groups</option>
            <option v-for="group in groups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full table-auto">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left">Title</th>
              <th class="px-4 py-2 text-left">Groups</th>
              <th class="px-4 py-2 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in filteredCourses" :key="course.id" class="border-b">
              <td class="px-4 py-2">
                <router-link :to="`/courses/${course.id}`" class="text-blue-600 hover:underline">
                  {{ course.title }}
                </router-link>
              </td>
              <td class="px-4 py-2">{{ course.allowedGroups.join(', ') || 'None' }}</td>
              <td class="px-4 py-2 text-right">
                <router-link
                  :to="`/admin/courses/${course.id}`"
                  class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 mr-2"
                >
                  Edit
                </router-link>
                <button
                  @click="deleteCourse(course.id)"
                  class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  Delete
                </button>
              </td>
            </tr>
            <tr v-if="!filteredCourses.length">
              <td colspan="3" class="px-4 py-2 text-center text-gray-500">No courses available.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Users Tab -->
    <div v-if="activeTab === 'users'" class="bg-white rounded-lg shadow p-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Manage Users</h3>
      <div class="flex justify-between mb-4">
        <div>
          <label class="text-gray-600 mr-2">Filter by Group:</label>
          <select v-model="userGroupFilter" class="p-2 border rounded">
            <option value="">All Groups</option>
            <option v-for="group in groups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
        </div>
      </div>
      <form @submit.prevent="createUser" class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">Username</label>
          <input
            v-model="userForm.username"
            type="text"
            class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            placeholder="Enter username"
            required
          />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">Password</label>
          <input
            v-model="userForm.password"
            type="password"
            class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            placeholder="Enter password"
            required
          />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">Role</label>
          <select
            v-model="userForm.role"
            class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
          >
            <option value="student">Student</option>
            <option value="admin">Admin</option>
          </select>
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">Groups</label>
          <select
            v-model="userForm.groups"
            multiple
            class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
          >
            <option v-for="group in groups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
        </div>
        <div class="md:col-span-2">
          <button
            type="submit"
            class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
          >
            Create User
          </button>
        </div>
      </form>
      <div class="overflow-x-auto">
        <table class="w-full table-auto">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left">Username</th>
              <th class="px-4 py-2 text-left">Role</th>
              <th class="px-4 py-2 text-left">Groups</th>
              <th class="px-4 py-2 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id" class="border-b">
              <td class="px-4 py-2">{{ user.username }}</td>
              <td class="px-4 py-2">{{ user.role }}</td>
              <td class="px-4 py-2">{{ user.groups.join(', ') || 'None' }}</td>
              <td class="px-4 py-2 text-right">
                <button
                  @click="deleteUser(user.id)"
                  class="px-3 py-1 bg-red-600 text-white rounded hover:bg-red-700"
                >
                  Delete
                </button>
              </td>
            </tr>
            <tr v-if="!filteredUsers.length">
              <td colspan="4" class="px-4 py-2 text-center text-gray-500">No users available.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Groups Tab -->
    <div v-if="activeTab === 'groups'" class="bg-white rounded-lg shadow p-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Manage Groups</h3>
      <form @submit.prevent="createGroup" class="mb-6 grid grid-cols-1 gap-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">Group Name</label>
          <input
            v-model="groupForm.name"
            type="text"
            class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            placeholder="Enter group name"
            required
          />
        </div>
        <div>
          <button
            type="submit"
            class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition"
          >
            Create Group
          </button>
        </div>
      </form>
      <div class="overflow-x-auto">
        <table class="w-full table-auto">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left">Name</th>
              <th class="px-4 py-2 text-left">Users</th>
              <th class="px-4 py-2 text-left">Courses</th>
              <th class="px-4 py-2 text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="group in groups" :key="group.id" class="border-b">
              <td class="px-4 py-2">{{ group.name }}</td>
              <td class="px-4 py-2">{{ group.users.join(', ') || 'None' }}</td>
              <td class="px-4 py-2">{{ group.allowedCourses.join(', ') || 'None' }}</td>
              <td class="px-4 py-2 text-right">
                <button
                  @click="editGroup(group)"
                  class="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Edit
                </button>
              </td>
            </tr>
            <tr v-if="!groups.length">
              <td colspan="4" class="px-4 py-2 text-center text-gray-500">No groups available.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Edit Group Modal -->
    <div v-if="showEditGroupModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-xl font-semibold mb-4">Edit Group: {{ editGroupForm.name }}</h3>
        <form @submit.prevent="saveGroupEdit">
          <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-1">Users</label>
            <select
              v-model="editGroupForm.users"
              multiple
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            >
              <option v-for="user in users" :key="user.id" :value="user.username">
                {{ user.username }}
              </option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-1">Allowed Courses</label>
            <select
              v-model="editGroupForm.allowedCourses"
              multiple
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
            >
              <option v-for="course in courses" :key="course.id" :value="course.id">
                {{ course.title }}
              </option>
            </select>
          </div>
          <div class="flex justify-end">
            <button
              type="button"
              @click="showEditGroupModal = false"
              class="px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 mr-2"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      activeTab: 'courses',
      courses: [],
      users: [],
      groups: [],
      courseGroupFilter: '',
      userGroupFilter: '',
      userForm: {
        username: '',
        password: '',
        role: 'student',
        groups: [],
      },
      groupForm: {
        name: '',
      },
      showEditGroupModal: false,
      editGroupForm: {
        id: '',
        name: '',
        users: [],
        allowedCourses: [],
      },
    }
  },
  computed: {
    filteredCourses() {
      if (!this.courseGroupFilter) return this.courses
      return this.courses.filter(course =>
        course.allowedGroups.includes(this.courseGroupFilter)
      )
    },
    filteredUsers() {
      if (!this.userGroupFilter) return this.users
      return this.users.filter(user =>
        user.groups.includes(this.userGroupFilter)
      )
    },
  },
  async created() {
    await Promise.all([this.fetchCourses(), this.fetchUsers(), this.fetchGroups()])
  },
  watch: {
    courseGroupFilter() {
      this.fetchCourses()
    },
    userGroupFilter() {
      this.fetchUsers()
    },
  },
  methods: {
    async fetchCourses() {
      try {
        const token = localStorage.getItem('token')
        console.log('Fetching courses with filter:', this.courseGroupFilter)
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/courses`, {
          headers: { Authorization: `Bearer ${token}` },
          params: this.courseGroupFilter ? { group: this.courseGroupFilter } : {},
        })
        this.courses = response.data
        console.log('Courses fetched:', this.courses)
      } catch (error) {
        console.error('Failed to fetch courses:', error.response || error)
        this.courses = []
      }
    },
    async deleteCourse(courseId) {
      if (!confirm('Are you sure you want to delete this course?')) return
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${import.meta.env.VITE_API_URL}/courses/${courseId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.courses = this.courses.filter(c => c.id !== courseId)
        alert('Course deleted successfully!')
      } catch (error) {
        console.error('Failed to delete course:', error.response || error)
        alert(`Failed to delete course: ${error.response?.data?.detail || error.message}`)
      }
    },
    async fetchUsers() {
      try {
        const token = localStorage.getItem('token')
        console.log('Fetching users with filter:', this.userGroupFilter)
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/users`, {
          headers: { Authorization: `Bearer ${token}` },
          params: this.userGroupFilter ? { group: this.userGroupFilter } : {},
        })
        this.users = response.data
        console.log('Users fetched:', this.users)
      } catch (error) {
        console.error('Failed to fetch users:', error.response || error)
        this.users = []
      }
    },
    async createUser() {
      try {
        const token = localStorage.getItem('token')
        const payload = {
          ...this.userForm,
          groups: this.userForm.groups,
        }
        await axios.post(`${import.meta.env.VITE_API_URL}/users`, payload, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.userForm.username = ''
        this.userForm.password = ''
        this.userForm.role = 'student'
        this.userForm.groups = []
        await this.fetchUsers()
        alert('User created successfully!')
      } catch (error) {
        console.error('Failed to create user:', error.response || error)
        alert(`Failed to create user: ${error.response?.data?.detail || error.message}`)
      }
    },
    async deleteUser(userId) {
      if (!confirm('Are you sure you want to delete this user?')) return
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${import.meta.env.VITE_API_URL}/users/${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.users = this.users.filter(u => u.id !== userId)
        await this.fetchGroups()
        alert('User deleted successfully!')
      } catch (error) {
        console.error('Failed to delete user:', error.response || error)
        alert(`Failed to delete user: ${error.response?.data?.detail || error.message}`)
      }
    },
    async fetchGroups() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/users/groups`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.groups = response.data
        console.log('Groups fetched:', this.groups)
      } catch (error) {
        console.error('Failed to fetch groups:', error.response || error)
        this.groups = []
      }
    },
    async createGroup() {
      try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No authorization token found')
        console.log('Creating group:', this.groupForm)
        const payload = {
          name: this.groupForm.name,
          users: [],
          allowedCourses: [],
        }
        const groupResponse = await axios.post(
          `${import.meta.env.VITE_API_URL}/users/groups`,
          payload,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        console.log('Group created:', groupResponse.data)
        this.groupForm.name = ''
        await this.fetchGroups()
        alert('Group created successfully!')
      } catch (error) {
        console.error('Failed to create group:', error.response || error)
        alert(`Failed to create group: ${error.response?.data?.detail || error.message}`)
      }
    },
    editGroup(group) {
      this.editGroupForm = {
        id: group.id,
        name: group.name,
        users: group.users,
        allowedCourses: group.allowedCourses,
      }
      this.showEditGroupModal = true
    },
    async saveGroupEdit() {
      try {
        const token = localStorage.getItem('token')
        const payload = {
          name: this.editGroupForm.name,
          users: this.editGroupForm.users,
          allowedCourses: this.editGroupForm.allowedCourses,
        }
        await axios.put(
          `${import.meta.env.VITE_API_URL}/users/groups/${this.editGroupForm.id}`,
          payload,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        for (const username of this.editGroupForm.users) {
          const user = this.users.find(u => u.username === username)
          if (user) {
            const userGroups = user.groups.includes(this.editGroupForm.name)
              ? user.groups
              : [...user.groups, this.editGroupForm.name]
            await axios.put(
              `${import.meta.env.VITE_API_URL}/users/by-username/${username}`,
              { groups: userGroups },
              { headers: { Authorization: `Bearer ${token}` } }
            )
          }
        }
        this.showEditGroupModal = false
        await this.fetchGroups()
        await this.fetchUsers()
        alert('Group updated successfully!')
      } catch (error) {
        console.error('Failed to update group:', error.response || error)
        alert(`Failed to update group: ${error.response?.data?.detail || error.message}`)
      }
    },
  },
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}
.tab {
  color: #4b5563;
}
.tab:hover {
  color: #16a34a;
}
.table-auto th, .table-auto td {
  padding: 0.75rem;
}
.transition {
  transition: all 0.3s ease;
}
</style>