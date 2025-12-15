<!-- src/views/LoginView.vue -->
<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const identifier = ref('')
const password = ref('')
const localError = ref('')
const localMessage = ref('')

const handleLogin = async () => {
  localError.value = ''
  localMessage.value = ''

  if (!identifier.value.trim() || !password.value) {
    localError.value = 'Enter your Alumni ID / Voter ID / Email and password.'
    return
  }

  try {
    await authStore.login(identifier.value.trim(), password.value)
    localMessage.value = `Welcome, ${authStore.voter.name || 'voter'}. Redirecting...`
    router.push('/portal')
  } catch (error) {
    localError.value = authStore.error || 'Login failed.'
  }
}

const requestReset = async () => {
  localError.value = ''
  localMessage.value = ''
  if (!identifier.value.trim()) {
    localError.value = 'Enter your Student/Alumni/Voter ID or email to request a reset.'
    return
  }
  try {
    await api.post('voter/request-reset-pin/', { identifier: identifier.value.trim() })
    localMessage.value = 'Reset request sent to admin.'
  } catch (err) {
    localError.value = err.response?.data?.error || 'Could not send reset request.'
  }
}
</script>

<template>
  <div class="min-h-[70vh] flex items-center justify-center px-4">
    <div class="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
      <div class="text-center space-y-1">
        <p class="text-xs uppercase tracking-wide text-emerald-600 font-semibold">HCAD Alumni</p>
        <h1 class="text-2xl font-semibold">Alumni Login</h1>
        <p class="text-xs text-slate-500">Use your Student ID / Alumni ID / Voter ID / Email with your password.</p>
      </div>

      <div class="space-y-3">
        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Student ID / Alumni ID / Voter ID / Email</label>
          <input
            v-model="identifier"
            type="text"
            class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            placeholder="e.g. S-12345 or you@example.com"
          />
        </div>

        <div>
          <label class="block text-xs font-semibold text-slate-600 mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            class="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
            placeholder="Enter your password"
          />
        </div>

        <button
          @click="handleLogin"
          :disabled="authStore.loading"
          class="w-full inline-flex justify-center items-center rounded-lg bg-emerald-600 px-4 py-2 text-sm font-medium text-white shadow-sm disabled:bg-slate-300 disabled:cursor-not-allowed hover:bg-emerald-700"
        >
          <span v-if="authStore.loading">Logging in...</span>
          <span v-else>Login</span>
        </button>

        <div class="min-h-[32px]">
          <p v-if="localMessage" class="text-xs text-emerald-600">
            {{ localMessage }}
          </p>
          <p v-if="localError" class="text-xs text-rose-600">
            {{ localError }}
          </p>
        </div>

        <button
          @click="requestReset"
          type="button"
          class="w-full inline-flex justify-center items-center rounded-lg border border-slate-300 px-4 py-2 text-xs font-medium text-slate-700 bg-white hover:bg-slate-50"
        >
          Request admin to reset PIN
        </button>
      </div>

      <div class="text-[11px] text-slate-500 text-center space-y-1">
        <RouterLink to="/register" class="text-emerald-700 font-semibold">Need an account? Register here</RouterLink>
        <p>Admins / COMELEC: please use the admin login to manage voters, nominations, and results.</p>
        <RouterLink to="/admin-login" class="text-emerald-700 font-semibold">Go to admin login</RouterLink>
      </div>
    </div>
  </div>
</template>
