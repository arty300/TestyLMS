<template>
  <div class="container mx-auto p-4">
    <h2 class="text-2xl font-bold mb-4">{{ isEditing ? 'Edit Course' : 'Create Course' }}</h2>
    <div v-if="error" class="text-red-600 mb-4">{{ error }}</div>
    <form @submit.prevent="saveCourse">
      <div class="mb-4">
        <label class="block text-gray-700 font-medium mb-1">Title</label>
        <input
          v-model="form.title"
          type="text"
          class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
          placeholder="Enter course title"
          required
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-medium mb-1">Description</label>
        <textarea
          v-model="form.description"
          class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
          placeholder="Enter course description"
          rows="4"
          required
        ></textarea>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-medium mb-1">Content (Markdown)</label>
        <textarea ref="editor" class="w-full border rounded"></textarea>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-medium mb-1">Allowed Groups (comma-separated)</label>
        <input
          v-model="form.allowedGroups"
          type="text"
          class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-600"
          placeholder="e.g., group1,group2"
        />
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-medium mb-1">Upload .docx (Optional)</label>
        <input
          type="file"
          @change="uploadFile"
          accept=".docx"
          class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-green-600 file:text-white hover:file:bg-green-700"
        />
      </div>
      <button
        type="submit"
        class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
      >
        {{ isEditing ? 'Update Course' : 'Create Course' }}
      </button>
      <button
        type="button"
        @click="$router.push('/admin/panel')"
        class="ml-4 px-4 py-2 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
      >
        Cancel
      </button>
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
            title: 'Upload Image',
          }, 'table', '|',
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
      this.error = 'Failed to initialize editor.'
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
        if (this.editor) {
          this.editor.value(data.content)
        }
        this.error = null
      } catch (error) {
        console.error('Failed to load course:', error.response || error)
        this.error = `Failed to load course: ${
          error.response?.data?.detail || error.message || 'Unknown error'
        }`
      }
    },
    async saveCourse() {
      if (!this.form.title.trim() || !this.form.description.trim()) {
        this.error = 'Title and description are required.'
        return
      }
      const token = localStorage.getItem('token')
      if (!token) {
        this.error = 'No authorization token found.'
        return
      }
      const content = this.editor ? this.editor.value() : this.form.content
      if (!content) {
        this.error = 'Content cannot be empty.'
        return
      }
      const payload = {
        title: this.form.title,
        description: this.form.description,
        content,
        instructor: 'Admin',
        allowedGroups: this.form.allowedGroups
          ? this.form.allowedGroups.split(',').map(g => g.trim()).filter(g => g)
          : [],
        hiddenSections: [],
      }
      try {
        if (this.isEditing) {
          console.log('Updating course:', this.editingCourseId, payload)
          await axios.put(
            `${import.meta.env.VITE_API_URL}/courses/${this.editingCourseId}`,
            payload,
            { headers: { Authorization: `Bearer ${token}` } }
          )
          alert('Course updated successfully!')
        } else {
          console.log('Creating course:', payload)
          await axios.post(
            `${import.meta.env.VITE_API_URL}/courses`,
            payload,
            { headers: { Authorization: `Bearer ${token}` } }
          )
          alert('Course created successfully!')
        }
        this.$router.push('/admin/panel')
      } catch (error) {
        console.error('Failed to save course:', error.response || error)
        this.error = `Failed to save course: ${
          error.response?.data?.detail || error.message || 'Unknown error'
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
        this.error = 'No authorization token found.'
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
        this.error = `Failed to upload file: ${
          error.response?.data?.detail || error.message || 'Unknown error'
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
          this.error = `Failed to upload image: ${
            error.response?.data?.detail || error.message || 'Unknown error'
          }`
        }
      }
      input.click()
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
.mb-4 {
  margin-bottom: 1rem;
}
.block {
  display: block;
}
.text-gray-700 {
  color: #374151;
}
.w-full {
  width: 100%;
}
.p-2 {
  padding: 0.5rem;
}
.border {
  border: 1px solid #e5e7eb;
}
.rounded {
  border-radius: 0.25rem;
}
.transition-colors {
  transition: color 0.3s ease, background-color 0.3s ease;
}
</style>