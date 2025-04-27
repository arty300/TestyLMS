<template>
  <div class="container mx-auto p-6 bg-gray-50 min-h-screen">
    <h2 class="text-3xl font-extrabold text-gray-900 mb-4">{{ course.title }}</h2>
    <p class="text-gray-600 mb-4 max-w-4xl">{{ course.description }}</p>
    <div class="prose max-w-4xl text-left bg-white p-6 rounded-lg shadow-md">
      <template v-for="(part, index) in contentParts" :key="index">
        <div v-if="part.type === 'markdown'" v-html="part.content" class="mb-4"></div>
        <div v-else-if="part.type === 'hidden'" class="hidden-section border border-gray-300 rounded-md p-3 bg-gray-100 mb-4">
          <p v-if="part.section.isUnlocked" class="text-green-600 mb-2 font-medium">Раздел разблокирован!</p>
          <p v-else class="text-gray-600 mb-2 font-medium">Этот раздел скрыт. Стоимость разблокировки: {{ part.section.cost }} баллов</p>
          <button
            v-if="!part.section.isUnlocked"
            @click="unlockSection(part.sectionIndex)"
            class="unlock-button px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition duration-200"
            :class="{ 'opacity-50 cursor-not-allowed': user.points < part.section.cost }"
            :disabled="user.points < part.section.cost"
          >
            Разблокировать ({{ part.section.cost }} баллов)
          </button>
          <p v-if="!part.section.isUnlocked && user.points < part.section.cost" class="text-red-600 text-sm mt-1">Недостаточно баллов. У вас: {{ user.points }}</p>
          <div v-if="part.section.isUnlocked" v-html="part.section.content" class="mt-2"></div>
        </div>
      </template>
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
      user: {
        points: 0,
      },
      contentParts: [],
      apiBaseUrl: `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}`
    }
  },
  async created() {
    await Promise.all([this.fetchCourse(), this.fetchUser()]);
  },
  methods: {
    async fetchCourse() {
      try {
        const courseId = this.$route.params.id
        console.log('Fetching course ID:', courseId)
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No authorization token found')
        const { data } = await axios.get(`${this.apiBaseUrl}/courses/${courseId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        console.log('Course fetched:', JSON.stringify(data, null, 2))
        this.course = data
        this.processContent(data.content || '')
      } catch (error) {
        console.error('Failed to fetch course:', error.response || error)
        this.$router.push('/courses')
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
      } catch (error) {
        console.error('Failed to fetch user data:', error.response || error)
      }
    },
    processContent(content) {
      if (!content) {
        console.warn('Content is empty')
        this.contentParts = [{ type: 'markdown', content: '' }];
        return;
      }
      console.log('Processing content:', content);
      
      // Разбиваем контент на части: обычный Markdown и скрытые разделы
      const parts = [];
      let currentIndex = 0;
      const hiddenSectionRegex = /\[\[HIDDEN SECTION: hidden-(\d+)-(\d+) \| Cost: (\d+) points\]\]/g;
      let match;
      let hiddenSectionCounter = 0;
      
      while ((match = hiddenSectionRegex.exec(content)) !== null) {
        const start = match.index;
        const end = start + match[0].length;
        
        // Добавляем Markdown-часть перед скрытым разделом
        if (start > currentIndex) {
          const markdownPart = content.slice(currentIndex, start);
          // Применяем замену URL для изображений
          const updatedMarkdownPart = markdownPart.replace(
            /!\[(.*?)\]\(\/images\/([a-f0-9]+)\)/g,
            (match, altText, imageId) => {
              const fullUrl = `${this.apiBaseUrl}/images/${imageId}`;
              console.log(`Replacing image URL: ${match} -> ![${altText}](${fullUrl})`);
              return `![${altText}](${fullUrl})`;
            }
          );
          const html = marked(updatedMarkdownPart, { async: false, breaks: true, gfm: true });
          parts.push({ type: 'markdown', content: html });
        }
        
        // Используем счетчик для сопоставления с индексом в hiddenSections
        const sectionIndex = hiddenSectionCounter;
        hiddenSectionCounter++;
        
        if (sectionIndex < this.course.hiddenSections.length && this.course.hiddenSections[sectionIndex]) {
          const section = { ...this.course.hiddenSections[sectionIndex] };
          // Если раздел разблокирован, преобразуем его содержимое в HTML с заменой URL изображений
          if (section.isUnlocked) {
            section.content = marked(
              section.content.replace(
                /!\[(.*?)\]\(\/images\/([a-f0-9]+)\)/g,
                (match, altText, imageId) => {
                  const fullUrl = `${this.apiBaseUrl}/images/${imageId}`;
                  console.log(`Replacing image URL in hidden section: ${match} -> ![${altText}](${fullUrl})`);
                  return `![${altText}](${fullUrl})`;
                }
              ),
              { async: false, breaks: true, gfm: true }
            );
          }
          parts.push({ type: 'hidden', section, sectionIndex });
        } else {
          parts.push({ type: 'markdown', content: '<p class="text-red-600">Ошибка: скрытый раздел не найден</p>' });
        }
        
        currentIndex = end;
      }
      
      // Добавляем оставшуюся часть контента после последнего скрытого раздела
      if (currentIndex < content.length) {
        const markdownPart = content.slice(currentIndex);
        // Применяем замену URL для изображений
        const updatedMarkdownPart = markdownPart.replace(
          /!\[(.*?)\]\(\/images\/([a-f0-9]+)\)/g,
          (match, altText, imageId) => {
            const fullUrl = `${this.apiBaseUrl}/images/${imageId}`;
            console.log(`Replacing image URL: ${match} -> ![${altText}](${fullUrl})`);
            return `![${altText}](${fullUrl})`;
          }
        );
        const html = marked(updatedMarkdownPart, { async: false, breaks: true, gfm: true });
        parts.push({ type: 'markdown', content: html });
      }
      
      this.contentParts = parts;
      console.log('Content parts:', parts);
    },
    async unlockSection(sectionIndex) {
      try {
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No authorization token found')
        const courseId = this.$route.params.id
        const { data } = await axios.post(
          `${this.apiBaseUrl}/courses/${courseId}/unlock/${sectionIndex}`,
          {},
          { headers: { Authorization: `Bearer ${token}` } }
        )
        // Обновляем данные пользователя и курса после успешной разблокировки
        this.user.points = data.remainingPoints
        this.course.hiddenSections[sectionIndex].isUnlocked = true
        // Обновляем contentParts, чтобы отобразить разблокированный раздел
        const sectionContent = marked(
          this.course.hiddenSections[sectionIndex].content.replace(
            /!\[(.*?)\]\(\/images\/([a-f0-9]+)\)/g,
            (match, altText, imageId) => {
              const fullUrl = `${this.apiBaseUrl}/images/${imageId}`;
              console.log(`Replacing image URL in unlocked section: ${match} -> ![${altText}](${fullUrl})`);
              return `![${altText}](${fullUrl})`;
            }
          ),
          { async: false, breaks: true, gfm: true }
        );
        this.contentParts = this.contentParts.map(part => {
          if (part.type === 'hidden' && part.sectionIndex === sectionIndex) {
            return { ...part, section: { ...part.section, isUnlocked: true, content: sectionContent } };
          }
          return part;
        });
        // Обновляем данные пользователя в localStorage и в App.vue через событие
        localStorage.setItem('user', JSON.stringify(this.user));
        this.$emit('user-updated', this.user); // Сообщаем родительскому компоненту об обновлении
        alert('Раздел успешно разблокирован!');
      } catch (error) {
        console.error('Failed to unlock section:', error.response || error)
        alert(`Не удалось разблокировать раздел: ${error.response?.data?.detail || error.message}`);
      }
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
.hidden-section {
  border: 1px solid #d1d5db;
  border-radius: 0.25rem;
  padding: 0.75rem;
  background-color: #f9fafb;
  margin-bottom: 0.5rem;
}
.text-left {
  text-align: left;
}
</style>