<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Logo from '../assets/HCAD_Alumni_Org_Logo.jpg'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  first_name: '',
  middle_name: '',
  last_name: '',
  student_id: '',
  date_of_birth: '',
  degree_program: '',
  batch_year: '',
  campus_chapter: 'Digos City',
  email: '',
  phone: '',
  employment_status: '',
  industry_field: '',
  password: '',
  privacy_consent: false,
})

const localError = ref('')
const localMessage = ref('')

const handleRegister = async () => {
  localError.value = ''
  localMessage.value = ''

  if (!form.value.privacy_consent) {
    localError.value = 'Please agree to the data privacy consent.'
    return
  }

  try {
    await authStore.register({
      ...form.value,
      batch_year: Number(form.value.batch_year),
    })
    localMessage.value = 'Registration successful. Redirecting...'
    router.push('/portal')
  } catch (error) {
    localError.value = authStore.error || 'Registration failed.'
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 py-6 space-y-4">
    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-3 flex items-center gap-4">
      <img :src="Logo" alt="HCAD Alumni" class="h-12 w-12 rounded-full border border-emerald-100 object-cover bg-white shadow-sm" />
      <div class="space-y-1">
        <p class="text-xs uppercase tracking-wide text-emerald-600 font-semibold">HCAD Alumni</p>
        <h1 class="text-2xl font-semibold text-slate-900">Create your alumni portal account</h1>
        <p class="text-sm text-slate-600">
          Provide your alumni identity and contact details. You will use your Student ID (temporary) or email with a password to sign in. Approved accounts receive an Alumni ID.
        </p>
      </div>
    </div>

    <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
      <div>
        <h2 class="text-lg font-semibold text-slate-900">1) Identity & Security</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mt-3">
          <div>
            <label class="text-sm font-semibold text-slate-700">First name</label>
            <input v-model="form.first_name" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Middle name</label>
            <input v-model="form.middle_name" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Last name</label>
            <input v-model="form.last_name" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div class="lg:col-span-1 md:col-span-2">
            <label class="text-sm font-semibold text-slate-700">Student ID (from HCAD/Registrar)</label>
            <input v-model="form.student_id" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
            <p class="text-xs text-slate-500 mt-1">If you need assistance, contact the alumni office.</p>
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Date of birth</label>
            <input v-model="form.date_of_birth" type="date" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Official email</label>
            <input v-model="form.email" type="email" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Mobile number</label>
            <input v-model="form.phone" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Password (min 8 characters)</label>
            <input v-model="form.password" type="password" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
        </div>
      </div>

      <div>
        <h2 class="text-lg font-semibold text-slate-900">2) Alumni profile</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-3">
          <div>
            <label class="text-sm font-semibold text-slate-700">Degree / Program</label>
            <input v-model="form.degree_program" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Batch / Year Graduated</label>
            <input v-model="form.batch_year" type="number" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Employment status</label>
            <input v-model="form.employment_status" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Industry / Field of work</label>
            <input v-model="form.industry_field" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Campus / Chapter</label>
            <input v-model="form.campus_chapter" type="text" class="w-full mt-1 rounded-lg border border-slate-300 px-3 py-2 shadow-sm" />
          </div>
        </div>
      </div>

      <div class="space-y-2">
        <label class="flex items-center gap-2 text-sm text-slate-700">
          <input type="checkbox" v-model="form.privacy_consent" />
          I consent to the processing of my personal data for alumni communications and elections.
        </label>
        <div class="text-xs text-slate-500">
          We use your details to verify alumni status, send election updates, and improve alumni programs.
        </div>
      </div>

      <div class="flex items-center gap-3">
        <button
          @click="handleRegister"
          :disabled="authStore.loading"
          class="px-4 py-2 rounded-lg bg-emerald-600 text-white font-semibold shadow-sm hover:bg-emerald-700 disabled:opacity-60"
        >
          <span v-if="authStore.loading">Submitting...</span>
          <span v-else>Register</span>
        </button>
        <RouterLink to="/login" class="text-sm text-slate-600 hover:underline">Already registered? Log in</RouterLink>
      </div>

      <div class="min-h-[32px]">
        <p v-if="localMessage" class="text-sm text-emerald-700">{{ localMessage }}</p>
        <p v-if="localError" class="text-sm text-rose-600">{{ localError }}</p>
      </div>
    </div>
  </div>
</template>
