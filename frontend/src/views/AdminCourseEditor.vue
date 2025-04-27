<template>
  <div class="container mx-auto p-6 bg-gray-50 min-h-screen">
    <h2 class="text-3xl font-extrabold text-gray-900 mb-6">{{ isEditing ? 'Редактировать курс' : 'Создать курс' }}</h2>
    <div v-if="error" class="text-red-600 mb-4 p-3 bg-red-100 rounded-md">{{ error }}</div>
    <form @submit.prevent="saveCourse" class="space-y-6">
      <div>
        <label class="block text-gray-700 font-medium mb-1">Название</label>
        <input
          v-model="form.title"
          type="text"
          class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          placeholder="Введите название курса"
          required
        />
      </div>
      <div>
        <label class="block text-gray-700 font-medium mb-1">Описание</label>
        <textarea
          v-model="form.description"
          class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          placeholder="Введите описание курса"
          rows="4"
          required
        ></textarea>
      </div>
      <div>
        <label class="block text-gray-700 font-medium mb-1">Содержимое (Markdown)</label>
        <textarea ref="editor" class="w-full border border-gray-300 rounded-md"></textarea>
      </div>
      <div>
        <label class="block text-gray-700 font-medium mb-1">Разрешенные группы (через запятую)</label>
        <input
          v-model="form.allowedGroups"
          type="text"
          class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
          placeholder="например, group1,group2"
        />
      </div>
      <div>
        <label class="block text-gray-700 font-medium mb-1">Загрузить .docx (опционально)</label>
        <input
          type="file"
          @change="uploadFile"
          accept=".docx"
          class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-green-600 file:text-white hover:file:bg-green-700 transition duration-200"
        />
      </div>
      <div class="flex space-x-4">
        <button
          type="submit"
          class="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition duration-200"
        >
          {{ isEditing ? 'Обновить курс' : 'Создать курс' }}
        </button>
        <button
          type="button"
          @click="$router.push('/admin/panel')"
          class="px-4 py-2 bg-gray-600 text-white rounded-md hover:bg-gray-700 transition duration-200"
        >
          Отмена
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import EasyMDE from 'easymde'
import 'easymde/dist/easymde.min.css'

export default {
  data() {
    return {
      editor: null,
      form: {
        title: '',
        description: '',
        content: '',
        allowedGroups: '',
        hiddenSections: [],
      },
      isEditing: false,
      editingCourseId: null,
      error: null,
    }
  },
  async created() {
    if (this.$route.params.id) {
      this.isEditing = true
      this.editingCourseId = this.$route.params.id
      await this.loadCourse(this.$route.params.id)
    }
  },
  mounted() {
    try {
      this.editor = new EasyMDE({
        element: this.$refs.editor,
        autoDownloadFontAwesome: true,
        spellChecker: false,
        toolbar: [
          'bold', 'italic', 'heading', '|',
          'quote', 'unordered-list', 'ordered-list', '|',
          'link', {
            name: 'image',
            action: this.uploadImage,
            className: 'fa fa-picture-o',
            title: 'Загрузить изображение',
          }, 'table', {
            name: 'hideSection',
            action: this.hideSection,
            className: 'fa fa-lock',
            title: 'Скрыть раздел со стоимостью',
          }, '|',
          'preview', 'side-by-side', 'fullscreen', '|',
          'guide'
        ],
        status: ['autosave', 'lines', 'words', 'cursor'],
      })
      if (this.form.content) {
        this.editor.value(this.form.content)
      }
      this.editor.codemirror.on('change', () => {
        this.form.content = this.editor.value()
      })
      console.log('EasyMDE initialized')
    } catch (error) {
      console.error('Failed to initialize EasyMDE:', error)
      this.error = 'Не удалось инициализировать редактор.'
    }
  },
  methods: {
    async loadCourse(courseId) {
      try {
        console.log('Loading course ID:', courseId)
        const token = localStorage.getItem('token')
        if (!token) throw new Error('No authorization token found')
        const { data } = await axios.get(`${import.meta.env.VITE_API_URL}/courses/${courseId}`, {
          headers: { Authorization: `Bearer ${token}` },
        })
        console.log('Course loaded:', data)
        this.form.title = data.title
        this.form.description = data.description
        this.form.content = data.content
        this.form.allowedGroups = data.allowedGroups ? data.allowedGroups.join(',') : ''
        this.form.hiddenSections = data.hiddenSections || []
        if (this.editor) {
          this.editor.value(data.content)
        }
        this.error = null
      } catch (error) {
        console.error('Failed to load course:', error.response || error)
        this.error = `Не удалось загрузить курс: ${
          error.response?.data?.detail || error.message || 'Неизвестная ошибка'
        }`
      }
    },
    async saveCourse() {
      if (!this.form.title.trim() || !this.form.description.trim()) {
        this.error = 'Название и описание обязательны.'
        return
      }
      const token = localStorage.getItem('token')
      if (!token) {
        this.error = 'Токен авторизации не найден.'
        return
      }
      const content = this.editor ? this.editor.value() : this.form.content
      if (!content) {
        this.error = 'Содержимое не может быть пустым.'
        return
      }
      const hiddenSections = this.form.hiddenSections.map(section => ({
        content: section.content,
        cost: section.cost
      }));
      const payload = {
        title: this.form.title,
        description: this.form.description,
        content,
        instructor: 'Admin',
        allowedGroups: this.form.allowedGroups
          ? this.form.allowedGroups.split(',').map(g => g.trim()).filter(g => g)
          : [],
        hiddenSections: hiddenSections,
      }
      try {
        if (this.isEditing) {
          console.log('Updating course:', this.editingCourseId, payload)
          await axios.put(
            `${import.meta.env.VITE_API_URL}/courses/${this.editingCourseId}`,
            payload,
            { headers: { Authorization: `Bearer ${token}` } }
          )
          alert('Курс успешно обновлен!')
        } else {
          console.log('Creating course:', payload)
          await axios.post(
            `${import.meta.env.VITE_API_URL}/courses`,
            payload,
            { headers: { Authorization: `Bearer ${token}` } }
          )
          alert('Курс успешно создан!')
        }
        this.$router.push('/admin/panel')
      } catch (error) {
        console.error('Failed to save course:', error.response || error)
        this.error = `Не удалось сохранить курс: ${
          error.response?.data?.detail || error.message || 'Неизвестная ошибка'
        }`
      }
    },
    async uploadFile(event) {
      const file = event.target.files[0]
      if (!file) return
      const formData = new FormData()
      formData.append('file', file)
      const token = localStorage.getItem('token')
      if (!token) {
        this.error = 'Токен авторизации не найден.'
        return
      }
      try {
        const { data } = await axios.post(`${import.meta.env.VITE_API_URL}/courses/upload`, formData, {
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' },
        })
        this.form.title = data.title
        this.form.description = data.description
        this.form.content = data.content
        if (this.editor) this.editor.value(data.content)
        this.error = null
      } catch (error) {
        console.error('Failed to upload file:', error.response || error)
        this.error = `Не удалось загрузить файл: ${
          error.response?.data?.detail || error.message || 'Неизвестная ошибка'
        }`
      }
    },
    async uploadImage(editor) {
      const input = document.createElement('input')
      input.type = 'file'
      input.accept = 'image/*'
      input.onchange = async () => {
        const file = input.files[0]
        if (!file) return
        const formData = new FormData()
        formData.append('file', file)
        try {
          const token = localStorage.getItem('token')
          if (!token) throw new Error('No authorization token found')
          console.log('Uploading image:', file.name, 'Size:', file.size)
          const { data } = await axios.post(
            `${import.meta.env.VITE_API_URL}/courses/upload-image`,
            formData,
            {
              headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' },
            }
          )
          console.log('Image uploaded:', data.url)
          const cm = editor.codemirror
          cm.replaceSelection(`![${file.name}](${data.url})`)
          this.error = null
        } catch (error) {
          console.error('Failed to upload image:', error.response || error)
          this.error = `Не удалось загрузить изображение: ${
            error.response?.data?.detail || error.message || 'Неизвестная ошибка'
          }`
        }
      }
      input.click()
    },
    hideSection(editor) {
      const cm = editor.codemirror;
      const selectedText = cm.getSelection();
      if (!selectedText) {
        alert('Пожалуйста, выделите текст или изображение для скрытия.');
        return;
      }
      const cost = prompt('Введите стоимость разблокировки в баллах:', '10');
      if (cost === null) return; // Отмена
      const costNum = parseInt(cost);
      if (isNaN(costNum) || costNum <= 0) {
        alert('Пожалуйста, введите корректное число баллов.');
        return;
      }
      const sectionId = `hidden-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
      const placeholder = `[[HIDDEN SECTION: ${sectionId} | Cost: ${costNum} points]]`;
      cm.replaceSelection(placeholder);
      this.form.hiddenSections.push({
        content: selectedText,
        cost: costNum,
        placeholder: placeholder,
        sectionId: sectionId
      });
      console.log('Hidden section added:', this.form.hiddenSections);
    },
  },
  beforeDestroy() {
    if (this.editor) {
      this.editor.toTextArea()
      this.editor = null
    }
  },
}
</script>

<style scoped>
.container {
  max-width: 1200px;
}
.transition {
  transition: all 0.3s ease;
}
</style>