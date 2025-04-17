<template>
  <div class="container mx-auto p-6">
    <h2 class="text-3xl font-bold text-gray-800 mb-4">{{ course.title }}</h2>
    <p class="text-gray-600 mb-4">{{ course.description }}</p>
    <div class="prose max-w-none" v-html="renderedContent"></div>
    <div v-if="course.hiddenSections && course.hiddenSections.length" class="mt-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-2">Hidden Sections</h3>
      <div v-for="(section, index) in course.hiddenSections" :key="index" class="mb-4">
        <h4 class="text-lg font-medium text-gray-700">{{ section.title }}</h4>
        <div class="prose max-w-none" v-html="renderMarkdown(section.content)"></div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { marked } from 'marked'

export default {
  data() {
    return {
      course: {
        title: '',
        description: '',
        content: '',
        instructor: '',
        allowedGroups: [],
        hiddenSections: [],
      },
      renderedContent: '',
    }
  },
  async created() {
    await this.fetchCourse()
  },
  methods: {
    async fetchCourse() {
      try {
        const courseId = this.$route.params.id
        console.log('Fetching course ID:', courseId)
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No authorization token found')
        const { data } = await axios.get(`${import.meta.env.VITE_API_URL}/courses/${courseId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        console.log('Course fetched:', JSON.stringify(data, null, 2))
        this.course = data
        this.renderedContent = this.renderMarkdown(data.content || '')
      } catch (error) {
        console.error('Failed to fetch course:', error.response || error)
        this.$router.push('/courses')
      }
    },
    renderMarkdown(content) {
      if (!content) {
        console.warn('Content is empty')
        return ''
      }
      console.log('Rendering Markdown:', content)
      // Вручную добавляем полный URL к изображениям
      const updatedContent = content.replace(
        /!\[(.*?)\]\(\/images\/([a-f0-9]+)\)/g,
        `![$1](${import.meta.env.VITE_API_URL}/images/$2)`
      )
      console.log('Updated Markdown:', updatedContent)
      const html = marked(updatedContent, {
        async: false,
        breaks: true,
        gfm: true,
      })
      console.log('Rendered HTML:', html)
      return html
    },
  },
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}
.prose {
  color: #374151;
}
.prose img {
  max-width: 100%;
  height: auto;
}
</style>