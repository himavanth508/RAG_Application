<template>
  <div class="auth-container">
    <h2>Login</h2>
    <div class="error-message" v-if="errorMsg">{{ errorMsg }}</div>
    <div class="form-group">
      <input v-model="username" placeholder="Username" :class="{ 'error': errorMsg }" />
      <input v-model="password" type="password" placeholder="Password" :class="{ 'error': errorMsg }" />
      <button @click="login" :disabled="isLoading">
        {{ isLoading ? 'Logging in...' : 'Login' }}
      </button>
    </div>
    <p>
      Don't have an account?
      <router-link to="/register">Register</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const isLoading = ref(false)

const login = async () => {
  try {
    errorMsg.value = ''
    isLoading.value = true
    
    const form = new URLSearchParams()
    form.append('username', username.value)
    form.append('password', password.value)

    const res = await fetch('http://localhost:8000/token', {
      method: 'POST',
      body: form
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || 'Login failed')
    }

    const data = await res.json()
    localStorage.setItem('token', data.access_token)
    router.push('/chat')  // Use router instead of window.location.reload()
  } catch (error) {
    errorMsg.value = error.message
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

input {
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input.error {
  border-color: #ff4444;
}

.error-message {
  color: #ff4444;
  margin-bottom: 1rem;
  padding: 0.5rem;
  background-color: #ffebee;
  border-radius: 4px;
}

button {
  padding: 0.8rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

a {
  color: #4CAF50;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
