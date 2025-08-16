<template>
  <div class="container">
    <h1 class="title">🧠 AI Assistant</h1>

    <!-- Upload Section -->
    <div class="upload-box">
      <label class="label">Upload a Document</label>
      <input type="file" @change="handleFileUpload" />
      <button @click="uploadDoc" class="upload-btn">Upload & Index</button>
    </div>

    <!-- Chat Window -->
    <div class="chat-window">
      <div ref="chatContainer" class="chat-log">
        <div v-for="(message, index) in chatLog" :key="index">
          <div :class="message.role === 'user' ? 'user-msg' : 'bot-msg'">
            <div v-html="md.render(message.text)"></div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="chat-input">
        <input
          v-model="query"
          @keyup.enter="askQuestion"
          placeholder="Type your question..."
        />
        <button @click="askQuestion">Ask</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt()

const file = ref(null)
const query = ref('')
const chatLog = ref([])
const chatContainer = ref(null)

const handleFileUpload = (e) => {
  file.value = e.target.files[0]
}

const uploadDoc = async () => {
  if (!file.value) {
    alert('Please upload a file.')
    return
  }

  const formData = new FormData()
  formData.append('file', file.value)
  const token = localStorage.getItem('token')

  const res= await fetch('http://localhost:8000/upload', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData
  })

  if(res.ok) {
    const error = await res.json()
    alert(`Error: ${error.detail || 'Failed to upload file'}`)
    return
  }
  alert('File uploaded and indexed!')
}

const askQuestion = async () => {
  const q = query.value.trim()
  if (!q) return

  chatLog.value.push({ role: 'user', text: q })
  query.value = ''

  await nextTick(() => {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  })

  const formData = new FormData()
  formData.append('query', q)
  const token = localStorage.getItem('token')

  const res = await fetch('http://localhost:8000/query', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData
  })
  const data = await res.json()

  chatLog.value.push({ role: 'bot', text: data.answer || 'No response' })

  await nextTick(() => {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  })
}
</script>

<style scoped>
.container {
  max-width: 700px;
  margin: 0 auto;
  padding: 2rem;
  font-family: Arial, sans-serif;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 2rem;
  color: #333;
}

.upload-box {
  background: #f4f4f4;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

.upload-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.upload-btn:hover {
  background: #0056b3;
}

.chat-window {
  display: flex;
  flex-direction: column;
  border: 1px solid #ccc;
  border-radius: 8px;
  height: 60vh;
  overflow: hidden;
}

.chat-log {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  background: #fafafa;
}

.user-msg {
  background: #d6e9ff;
  color: #003366;
  padding: 0.5rem 1rem;
  margin: 0.5rem 0;
  border-radius: 15px;
  text-align: right;
  max-width: 70%;
  margin-left: auto;
}

.bot-msg {
  background: #eaeaea;
  color: #333;
  padding: 0.5rem 1rem;
  margin: 0.5rem 0;
  border-radius: 15px;
  text-align: left;
  max-width: 70%;
  margin-right: auto;
}

.chat-input {
  display: flex;
  padding: 0.75rem;
  border-top: 1px solid #ddd;
  background: white;
}

.chat-input input {
  flex: 1;
  padding: 0.5rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-right: 0.5rem;
}

.chat-input button {
  padding: 0.5rem 1rem;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.chat-input button:hover {
  background: #218838;
}
</style>
