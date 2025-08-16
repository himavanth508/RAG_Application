<template>
  <div class="auth-container">
    <h2>Create Account</h2>
    <div class="error-message" v-if="errorMsg">{{ errorMsg }}</div>
    <div class="form-group">
      <input 
        v-model="username" 
        placeholder="Username" 
        :class="{ 'error': errorMsg }"
      />
      <input 
        v-model="password" 
        type="password" 
        placeholder="Password" 
        :class="{ 'error': errorMsg }"
      />
      <button @click="register" :disabled="isLoading">
        {{ isLoading ? 'Creating Account...' : 'Register' }}
      </button>
    </div>
    <p class="login-link">
      Already have an account?
      <router-link to="/login">Login</router-link>
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

const register = async () => {
  if (!username.value || !password.value) {
    errorMsg.value = 'Please fill in all fields'
    return
  }
  
  try {
    isLoading.value = true
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Registration failed')
    }

    router.push('/login')
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
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: white;
}

h2 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
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
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
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
  font-size: 0.9rem;
}

button {
  padding: 0.8rem;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #45a049;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

a {
  color: #4CAF50;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

a:hover {
  color: #45a049;
  text-decoration: underline;
}
</style>
