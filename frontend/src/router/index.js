import { createRouter, createWebHistory } from 'vue-router'
import AdminPanel from '../views/AdminPanel.vue'
import AdminCourseEditor from '../views/AdminCourseEditor.vue'
import HomeView from '@/views/HomeView.vue'
import CoursesView from '@/views/CoursesView.vue'
import CourseView from '@/views/CourseView.vue'
import ProfileView from '@/views/ProfileView.vue'
import LoginView from '@/views/LoginView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/courses', name: 'Courses', component: CoursesView },
  { path: '/courses/:id', name: 'Course', component: CourseView },
  { path: '/profile', name: 'Profile', component: ProfileView },
  { path: '/admin/panel', name: 'AdminPanel', component: AdminPanel },
  { path: '/admin/courses', name: 'AdminCourseEditor', component: AdminCourseEditor },
  { path: '/admin/courses/:id', name: 'AdminCourseEditorEdit', component: AdminCourseEditor },
  { path: '/login', name: 'Login', component: LoginView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})


export default router