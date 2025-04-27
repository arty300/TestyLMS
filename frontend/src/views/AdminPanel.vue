<template>
  <div class="container mx-auto p-6 bg-gray-50 min-h-screen">
    <h2 class="text-3xl font-extrabold text-gray-900 mb-6">Панель администратора</h2>
    <div class="tabs flex border-b border-gray-200 mb-8">
      <button
        :class="{ 'border-b-2 border-green-600 text-green-600': activeTab === 'courses' }"
        class="tab px-4 py-2 text-lg font-medium text-gray-600 hover:text-green-600 transition duration-200"
        @click="activeTab = 'courses'"
      >
        Курсы
      </button>
      <button
        :class="{ 'border-b-2 border-green-600 text-green-600': activeTab === 'users' }"
        class="tab px-4 py-2 text-lg font-medium text-gray-600 hover:text-green-600 transition duration-200"
        @click="activeTab = 'users'"
      >
        Пользователи
      </button>
      <button
        :class="{ 'border-b-2 border-green-600 text-green-600': activeTab === 'groups' }"
        class="tab px-4 py-2 text-lg font-medium text-gray-600 hover:text-green-600 transition duration-200"
        @click="activeTab = 'groups'"
      >
        Группы
      </button>
      <button
        :class="{ 'border-b-2 border-green-600 text-green-600': activeTab === 'analytics' }"
        class="tab px-4 py-2 text-lg font-medium text-gray-600 hover:text-green-600 transition duration-200"
        @click="activeTab = 'analytics'; debugAnalytics()"
      >
        Аналитика
      </button>
    </div>

    <!-- Courses Tab -->
    <div v-if="activeTab === 'courses'" class="bg-white rounded-lg shadow-md p-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Управление курсами</h3>
      <div class="flex justify-between mb-4">
        <router-link
          to="/admin/courses"
          class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition duration-200"
        >
          Создать новый курс
        </router-link>
        <div>
          <label class="text-gray-600 mr-2">Фильтр по группе:</label>
          <select v-model="courseGroupFilter" class="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500">
            <option value="">Все группы</option>
            <option v-for="group in groups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full table-auto border-collapse">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Название</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Группы</th>
              <th class="px-4 py-2 text-right text-gray-700 font-medium">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="course in filteredCourses" :key="course.id" class="border-b hover:bg-gray-50 transition duration-200">
              <td class="px-4 py-2">
                <router-link :to="`/courses/${course.id}`" class="text-blue-600 hover:underline">
                  {{ course.title }}
                </router-link>
              </td>
              <td class="px-4 py-2">{{ course.allowedGroups.join(', ') || 'Нет' }}</td>
              <td class="px-4 py-2 text-right">
                <router-link
                  :to="`/admin/courses/${course.id}`"
                  class="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 mr-2 transition duration-200"
                >
                  Редактировать
                </router-link>
                <button
                  @click="deleteCourse(course.id)"
                  class="px-3 py-1 bg-red-600 text-white rounded-md hover:bg-red-700 transition duration-200"
                >
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="!filteredCourses.length">
              <td colspan="3" class="px-4 py-2 text-center text-gray-500">Курсы отсутствуют.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Users Tab -->
    <div v-if="activeTab === 'users'" class="bg-white rounded-lg shadow-md p-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Управление пользователями</h3>
      <div class="flex justify-between mb-4">
        <div>
          <label class="text-gray-600 mr-2">Фильтр по группе:</label>
          <select v-model="userGroupFilter" class="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500">
            <option value="">Все группы</option>
            <option v-for="group in groups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
        </div>
      </div>
      <form @submit.prevent="createUser" class="mb-6 grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">Имя пользователя</label>
          <input
            v-model="userForm.username"
            type="text"
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="Введите имя пользователя"
            required
          />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">Пароль</label>
          <input
            v-model="userForm.password"
            type="password"
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="Введите пароль"
            required
          />
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">Роль</label>
          <select
            v-model="userForm.role"
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          >
            <option value="student">Студент</option>
            <option value="admin">Администратор</option>
          </select>
        </div>
        <div>
          <label class="block text-gray-700 font-medium mb-1">Группы</label>
          <select
            v-model="userForm.groups"
            multiple
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 max-h-24"
          >
            <option v-for="group in groups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
        </div>
        <div class="md:col-span-2">
          <button
            type="submit"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition duration-200"
          >
            Создать пользователя
          </button>
        </div>
      </form>
      <div class="overflow-x-auto">
        <table class="w-full table-auto border-collapse">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Имя пользователя</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Роль</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Группы</th>
              <th class="px-4 py-2 text-right text-gray-700 font-medium">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id" class="border-b hover:bg-gray-50 transition duration-200">
              <td class="px-4 py-2">{{ user.username }}</td>
              <td class="px-4 py-2">{{ user.role === 'admin' ? 'Администратор' : 'Студент' }}</td>
              <td class="px-4 py-2">{{ user.groups.join(', ') || 'Нет' }}</td>
              <td class="px-4 py-2 text-right">
                <button
                  @click="deleteUser(user.id)"
                  class="px-3 py-1 bg-red-600 text-white rounded-md hover:bg-red-700 transition duration-200"
                >
                  Удалить
                </button>
              </td>
            </tr>
            <tr v-if="!filteredUsers.length">
              <td colspan="4" class="px-4 py-2 text-center text-gray-500">Пользователи отсутствуют.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Groups Tab -->
    <div v-if="activeTab === 'groups'" class="bg-white rounded-lg shadow-md p-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Управление группами</h3>
      <form @submit.prevent="createGroup" class="mb-6 grid grid-cols-1 gap-4">
        <div>
          <label class="block text-gray-700 font-medium mb-1">Название группы</label>
          <input
            v-model="groupForm.name"
            type="text"
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            placeholder="Введите название группы"
            required
          />
        </div>
        <div>
          <button
            type="submit"
            class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition duration-200"
          >
            Создать группу
          </button>
        </div>
      </form>
      <div class="overflow-x-auto">
        <table class="w-full table-auto border-collapse">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Название</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Пользователи</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Курсы</th>
              <th class="px-4 py-2 text-right text-gray-700 font-medium">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="group in groups" :key="group.id" class="border-b hover:bg-gray-50 transition duration-200">
              <td class="px-4 py-2">{{ group.name }}</td>
              <td class="px-4 py-2">
                {{ group.users.slice(0, 3).join(', ') || 'Нет' }}
                <span v-if="group.users.length > 3" class="text-blue-600 cursor-pointer hover:underline" @click="showUsersModal(group)">
                  ...и еще {{ group.users.length - 3 }}
                </span>
              </td>
              <td class="px-4 py-2">
                {{ getCourseTitles(group.allowedCourses).slice(0, 3).join(', ') || 'Нет' }}
                <span v-if="group.allowedCourses.length > 3" class="text-blue-600 cursor-pointer hover:underline" @click="showCoursesModal(group)">
                  ...и еще {{ group.allowedCourses.length - 3 }}
                </span>
              </td>
              <td class="px-4 py-2 text-right">
                <button
                  @click="editGroup(group)"
                  class="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition duration-200"
                >
                  Редактировать
                </button>
              </td>
            </tr>
            <tr v-if="!groups.length">
              <td colspan="4" class="px-4 py-2 text-center text-gray-500">Группы отсутствуют.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Edit Group Modal -->
    <div v-if="showEditGroupModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-3xl max-h-[80vh] overflow-y-auto">
        <h3 class="text-xl font-semibold mb-4">Редактировать группу: {{ editGroupForm.name }}</h3>
        <form @submit.prevent="saveGroupEdit">
          <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-1">Пользователи</label>
            <div class="mb-2">
              <input
                v-model="userSearchQuery"
                type="text"
                placeholder="Поиск по имени пользователя..."
                class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
              />
            </div>
            <div class="border border-gray-300 rounded-md p-2 max-h-40 overflow-y-auto">
              <div v-for="user in filteredUsers" :key="user.id" class="flex items-center mb-2">
                <input
                  type="checkbox"
                  :id="'user-' + user.id"
                  :value="user.username"
                  v-model="editGroupForm.users"
                  class="mr-2 h-5 w-5 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label :for="'user-' + user.id" class="cursor-pointer text-gray-800">{{ user.username }}</label>
              </div>
              <div v-if="!filteredUsers.length" class="text-gray-500">Пользователей не найдено</div>
            </div>
          </div>
          <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-1">Разрешенные курсы</label>
            <div class="border border-gray-300 rounded-md p-2 max-h-40 overflow-y-auto">
              <div v-for="course in courses" :key="course.id" class="flex items-center mb-2">
                <input
                  type="checkbox"
                  :id="'course-' + course.id"
                  :value="course.id"
                  v-model="editGroupForm.allowedCourses"
                  class="mr-2 h-5 w-5 text-green-600 focus:ring-green-500 border-gray-300 rounded"
                />
                <label :for="'course-' + course.id" class="cursor-pointer text-gray-800">{{ course.title }}</label>
              </div>
              <div v-if="!courses.length" class="text-gray-500">Курсов нет</div>
            </div>
          </div>
          <div class="flex justify-between mb-4">
            <button
              type="button"
              @click="deleteGroup(editGroupForm.id)"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition duration-200"
            >
              Удалить группу
            </button>
            <div class="flex">
              <button
                type="button"
                @click="showEditGroupModal = false"
                class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 mr-2 transition duration-200"
              >
                Отмена
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition duration-200"
              >
                Сохранить
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>

    <!-- Модальное окно для полного списка пользователей -->
    <div v-if="showUsersModalFlag" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md max-h-[80vh] overflow-y-auto">
        <h3 class="text-xl font-semibold mb-4">Пользователи в группе: {{ selectedGroup.name }}</h3>
        <div class="max-h-60 overflow-y-auto mb-4">
          <p v-for="user in selectedGroup.users" :key="user" class="border-b py-1 text-gray-800">{{ user }}</p>
          <p v-if="!selectedGroup.users.length" class="text-gray-500">Пользователей нет</p>
        </div>
        <div class="flex justify-end">
          <button
            type="button"
            @click="showUsersModalFlag = false"
            class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition duration-200"
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для полного списка курсов -->
    <div v-if="showCoursesModalFlag" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md max-h-[80vh] overflow-y-auto">
        <h3 class="text-xl font-semibold mb-4">Курсы в группе: {{ selectedGroup.name }}</h3>
        <div class="max-h-60 overflow-y-auto mb-4">
          <p v-for="courseTitle in getCourseTitles(selectedGroup.allowedCourses)" :key="courseTitle" class="border-b py-1 text-gray-800">{{ courseTitle }}</p>
          <p v-if="!selectedGroup.allowedCourses.length" class="text-gray-500">Курсов нет</p>
        </div>
        <div class="flex justify-end">
          <button
            type="button"
            @click="showCoursesModalFlag = false"
            class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition duration-200"
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>

    <!-- Analytics Tab -->
    <div v-if="activeTab === 'analytics'" class="bg-white rounded-lg shadow-md p-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-4">Аналитика</h3>
      <div v-if="debugMessage" class="text-red-500 mb-4">{{ debugMessage }}</div>
      <div class="flex justify-between mb-4">
        <div>
          <label class="text-gray-600 mr-2">Фильтр по группе:</label>
          <select v-model="analyticsGroupFilter" class="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500">
            <option value="">Все группы</option>
            <option v-for="group in groups" :key="group.id" :value="group.name">
              {{ group.name }}
            </option>
          </select>
        </div>
        <div>
          <label class="text-gray-600 mr-2">Фильтр по пользователю:</label>
          <select v-model="selectedUserId" class="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500">
            <option value="">Все пользователи</option>
            <option v-for="user in filteredAnalyticsUsersWithSearch" :key="user.id" :value="user.id">
              {{ user.username }}
            </option>
          </select>
        </div>
        <div>
          <label class="text-gray-600 mr-2">Поиск по имени:</label>
          <input
            v-model="userSearchQueryAnalytics"
            type="text"
            placeholder="Введите имя пользователя..."
            class="p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          />
        </div>
      </div>
      <div class="overflow-x-auto">
        <h4 class="text-lg font-medium text-gray-700 mb-2">Статистика по пользователям</h4>
        <table class="w-full table-auto border-collapse mb-6">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Имя пользователя</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Группы</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Пройденные курсы</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Процент прохождения</th>
              <th class="px-4 py-2 text-right text-gray-700 font-medium">Действия</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredAnalyticsUsersWithSearch" :key="user.id" class="border-b hover:bg-gray-50 transition duration-200">
              <td class="px-4 py-2">{{ user.username }}</td>
              <td class="px-4 py-2">{{ user.groups.join(', ') || 'Нет' }}</td>
              <td class="px-4 py-2">{{ user.completedCourses }} из {{ user.totalCourses }}</td>
              <td class="px-4 py-2">{{ user.completionPercentage }}%</td>
              <td class="px-4 py-2 text-right">
                <button
                  @click="selectedUserId = user.id"
                  class="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition duration-200"
                >
                  Подробности
                </button>
              </td>
            </tr>
            <tr v-if="!filteredAnalyticsUsersWithSearch.length">
              <td colspan="5" class="px-4 py-2 text-center text-gray-500">Пользователи отсутствуют.</td>
            </tr>
          </tbody>
        </table>
        
        <div v-if="selectedUserId" class="mt-6 p-4 border border-gray-200 rounded-lg">
          <h4 class="text-lg font-medium text-gray-700 mb-2">Подробная статистика по пользователю: {{ selectedUser.username }}</h4>
          <div class="space-y-4">
            <div>
              <p class="text-gray-600"><span class="font-medium">Роль:</span> {{ selectedUser.role === 'admin' ? 'Администратор' : 'Студент' }}</p>
              <p class="text-gray-600"><span class="font-medium">Баллы:</span> {{ selectedUser.points }}</p>
              <p class="text-gray-600"><span class="font-medium">Группы:</span> {{ selectedUser.groups.join(', ') || 'Нет' }}</p>
            </div>
            <div>
              <h5 class="font-medium text-gray-800">Прогресс по курсам:</h5>
              <div v-if="selectedUserCourses.length === 0" class="text-gray-500 py-2">
                <p>Пользователь не записан на курсы.</p>
              </div>
              <div v-else class="space-y-2">
                <div v-for="course in selectedUserCourses" :key="course.id" class="border border-gray-200 rounded-lg p-3 flex flex-col md:flex-row justify-between items-center gap-3">
                  <div>
                    <h6 class="font-medium text-gray-800">{{ course.title }}</h6>
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
          <div class="flex justify-end mt-4">
            <button
              @click="selectedUserId = ''"
              class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition duration-200"
            >
              Закрыть
            </button>
          </div>
        </div>
        
        <h4 class="text-lg font-medium text-gray-700 mb-2 mt-8">Статистика по группам</h4>
        <table class="w-full table-auto border-collapse">
          <thead>
            <tr class="bg-gray-100">
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Название группы</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Количество пользователей</th>
              <th class="px-4 py-2 text-left text-gray-700 font-medium">Средний процент прохождения</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="group in filteredAnalyticsGroups" :key="group.id" class="border-b hover:bg-gray-50 transition duration-200">
              <td class="px-4 py-2">{{ group.name }}</td>
              <td class="px-4 py-2">{{ group.users.length }}</td>
              <td class="px-4 py-2">{{ group.averageCompletion }}%</td>
            </tr>
            <tr v-if="!filteredAnalyticsGroups.length">
              <td colspan="3" class="px-4 py-2 text-center text-gray-500">Группы отсутствуют.</td>
            </tr>
          </tbody>
        </table>
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
      analyticsGroupFilter: '',
      selectedUserId: '',
      userSearchQuery: '',
      userSearchQueryAnalytics: '',
      debugMessage: '',
      showEditGroupModal: false,
      editGroupForm: {
        id: '',
        name: '',
        users: [],
        allowedCourses: [],
      },
      showUsersModalFlag: false,
      showCoursesModalFlag: false,
      selectedGroup: {},
      userForm: {
        username: '',
        password: '',
        role: 'student',
        groups: [],
      },
      groupForm: {
        name: '',
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
      if (!this.userGroupFilter) {
        if (this.userSearchQuery) {
          return this.users.filter(user =>
            user.username.toLowerCase().includes(this.userSearchQuery.toLowerCase())
          )
        }
        return this.users
      }
      return this.users.filter(user =>
        user.groups.includes(this.userGroupFilter)
      )
    },
    filteredAnalyticsUsers() {
      let filteredUsers = this.users;
      if (this.analyticsGroupFilter) {
        filteredUsers = filteredUsers.filter(user =>
          user.groups.includes(this.analyticsGroupFilter)
        );
      }
      return filteredUsers.map(user => {
        const totalCourses = this.courses.length;
        const unlockedSections = user.unlockedSections || {};
        let completedCourses = 0;
        this.courses.forEach(course => {
          const courseUnlockedSections = unlockedSections[course.id] || [];
          const hiddenSectionsCount = course.hiddenSections ? course.hiddenSections.length : 0;
          if (hiddenSectionsCount > 0 && courseUnlockedSections.length === hiddenSectionsCount) {
            completedCourses++;
          }
        });
        const completionPercentage = totalCourses > 0 ? Math.round((completedCourses / totalCourses) * 100) : 0;
        return {
          ...user,
          completedCourses,
          totalCourses,
          completionPercentage
        };
      });
    },
    filteredAnalyticsGroups() {
      let filteredGroups = this.groups;
      if (this.analyticsGroupFilter) {
        filteredGroups = filteredGroups.filter(group =>
          group.name === this.analyticsGroupFilter
        );
      }
      return filteredGroups.map(group => {
        const groupUsers = this.users.filter(user => user.groups.includes(group.name));
        let totalCompletion = 0;
        groupUsers.forEach(user => {
          const userStats = this.filteredAnalyticsUsers.find(u => u.id === user.id);
          if (userStats) {
            totalCompletion += userStats.completionPercentage;
          }
        });
        const averageCompletion = groupUsers.length > 0 ? Math.round(totalCompletion / groupUsers.length) : 0;
        return {
          ...group,
          averageCompletion
        };
      });
    },
    selectedUser() {
      if (!this.selectedUserId) return null;
      return this.filteredAnalyticsUsers.find(user => user.id === this.selectedUserId) || null;
    },
    selectedUserCourses() {
      if (!this.selectedUser) return [];
      const unlockedSections = this.selectedUser.unlockedSections || {};
      return this.courses.map(course => {
        const totalSections = course.hiddenSections ? course.hiddenSections.length : 0;
        const unlockedSectionsCount = unlockedSections[course.id] ? unlockedSections[course.id].length : 0;
        const progress = totalSections > 0 ? Math.round((unlockedSectionsCount / totalSections) * 100) : 0;
        return {
          ...course,
          progress,
          unlockedSections: unlockedSectionsCount,
          totalSections
        };
      });
    },
    filteredAnalyticsUsersWithSearch() {
      let filteredUsers = this.filteredAnalyticsUsers;
      if (this.userSearchQueryAnalytics) {
        filteredUsers = filteredUsers.filter(user =>
          user.username.toLowerCase().includes(this.userSearchQueryAnalytics.toLowerCase())
        );
      }
      return filteredUsers;
    }
  },
  async created() {
    await this.checkAdminAccess();
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
    async checkAdminAccess() {
      try {
        const token = localStorage.getItem('token')
        if (!token) {
          this.$router.push('/login')
          alert('Пожалуйста, войдите в систему.')
          return
        }
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/users/me`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        if (response.data.role !== 'admin') {
          this.$router.push('/courses')
          alert('Доступ запрещен. Только для администраторов.')
        }
      } catch (error) {
        console.error('Ошибка при проверке доступа администратора:', error.response || error)
        this.$router.push('/login')
        alert('Ошибка при проверке доступа. Пожалуйста, войдите снова.')
      }
    },
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
      if (!confirm('Вы уверены, что хотите удалить этот курс?')) return
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${import.meta.env.VITE_API_URL}/courses/${courseId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.courses = this.courses.filter(c => c.id !== courseId)
        alert('Курс успешно удален!')
      } catch (error) {
        console.error('Failed to delete course:', error.response || error)
        alert(`Не удалось удалить курс: ${error.response?.data?.detail || error.message}`)
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
        alert('Пользователь успешно создан!')
      } catch (error) {
        console.error('Failed to create user:', error.response || error)
        alert(`Не удалось создать пользователя: ${error.response?.data?.detail || error.message}`)
      }
    },
    async deleteUser(userId) {
      if (!confirm('Вы уверены, что хотите удалить этого пользователя?')) return
      try {
        const token = localStorage.getItem('token')
        await axios.delete(`${import.meta.env.VITE_API_URL}/users/${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.users = this.users.filter(u => u.id !== userId)
        await this.fetchGroups()
        alert('Пользователь успешно удален!')
      } catch (error) {
        console.error('Failed to delete user:', error.response || error)
        alert(`Не удалось удалить пользователя: ${error.response?.data?.detail || error.message}`)
      }
    },
    async fetchGroups() {
      try {
        const token = localStorage.getItem('token')
        const response = await axios.get(`${import.meta.env.VITE_API_URL}/users/groups`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        this.groups = response.data
        console.log('Groups fetched with detailed structure:', JSON.stringify(this.groups, null, 2))
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
        alert('Группа успешно создана!')
      } catch (error) {
        console.error('Failed to create group:', error.response || error)
        alert(`Не удалось создать группу: ${error.response?.data?.detail || error.message}`)
      }
    },
    editGroup(group) {
      console.log('Editing group with detailed structure:', JSON.stringify(group, null, 2));
      const groupId = group.id || group._id || group.groupId || '';
      if (!groupId) {
        console.error('No ID found for group. Available properties:', Object.keys(group));
      }
      this.editGroupForm = {
        id: groupId,
        name: group.name || '',
        users: group.users || [],
        allowedCourses: group.allowedCourses || [],
      }
      console.log('Edit group form after setting values:', this.editGroupForm);
      this.showEditGroupModal = true;
    },
    async saveGroupEdit() {
      try {
        const token = localStorage.getItem('token')
        const payload = {
          name: this.editGroupForm.name,
          users: this.editGroupForm.users,
          allowedCourses: this.editGroupForm.allowedCourses,
        }
        console.log('Saving group edit with multiple users and courses:', payload)
        if (!this.editGroupForm.id) {
          throw new Error('ID группы не определен. Пожалуйста, убедитесь, что группа была правильно выбрана для редактирования.')
        }
        await axios.put(
          `${import.meta.env.VITE_API_URL}/users/groups/${this.editGroupForm.id}`,
          payload,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.showEditGroupModal = false
        await this.fetchGroups()
        await this.fetchUsers()
        alert('Группа успешно обновлена!')
      } catch (error) {
        console.error('Failed to update group:', error.response || error)
        alert(`Не удалось обновить группу: ${error.response?.data?.detail || error.message}`)
      }
    },
    async deleteGroup(groupId) {
      if (!confirm('Вы уверены, что хотите удалить эту группу?')) return;
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`${import.meta.env.VITE_API_URL}/users/groups/${groupId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        this.showEditGroupModal = false;
        await this.fetchGroups();
        alert('Группа успешно удалена!');
      } catch (error) {
        console.error('Failed to delete group:', error.response || error);
        alert(`Не удалось удалить группу: ${error.response?.data?.detail || error.message}`);
      }
    },
    showUsersModal(group) {
      this.selectedGroup = group;
      this.showUsersModalFlag = true;
    },
    showCoursesModal(group) {
      this.selectedGroup = group;
      this.showCoursesModalFlag = true;
    },
    getCourseTitles(courseIds) {
      return courseIds.map(id => {
        const course = this.courses.find(c => c.id === id);
        return course ? course.title : id;
      });
    },
    debugAnalytics() {
      console.log('Opening Analytics Tab');
      console.log('Users:', this.users);
      console.log('Courses:', this.courses);
      console.log('Groups:', this.groups);
      if (this.users.length === 0) {
        this.debugMessage = 'Ошибка: Данные о пользователях не загружены. Попробуйте обновить страницу или проверить консоль для ошибок.';
      } else if (this.courses.length === 0) {
        this.debugMessage = 'Ошибка: Данные о курсах не загружены. Попробуйте обновить страницу или проверить консоль для ошибок.';
      } else {
        this.debugMessage = '';
      }
    }
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
.z-50 {
  z-index: 50;
}
.max-h-80vh {
  max-height: 80vh;
}
.overflow-y-auto {
  overflow-y: auto;
}
</style>