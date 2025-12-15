<script setup>
import { onMounted, ref, computed } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const profile = ref({
  name: '',
  first_name: '',
  middle_name: '',
  last_name: '',
  voter_id: '',
  batch_year: '',
  campus_chapter: '',
  email: '',
  phone: '',
  privacy_consent: false,
})
const loadingProfile = ref(true)
const savingProfile = ref(false)
const profileMessage = ref('')
const profileError = ref('')
const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: '',
})
const pinResetMessage = ref('')
const pinResetError = ref('')
const passwordSaving = ref(false)
const passwordMessage = ref('')
const passwordError = ref('')

const historyLoading = ref(true)
const historyError = ref('')
const voteHistory = ref([])
const nominationHistory = ref([])

const voterName = computed(() => authStore.voter?.name || profile.value.name || 'Voter')
const voterDisplayName = computed(() => {
  const parts = [
    profile.value.first_name || authStore.voter?.first_name,
    profile.value.middle_name || authStore.voter?.middle_name,
    profile.value.last_name || authStore.voter?.last_name,
  ].filter(Boolean)
  return parts.length ? parts.join(' ') : voterName.value
})
const voterId = computed(() => authStore.voter?.voter_id || profile.value.voter_id || '')
const studentId = computed(() => authStore.voter?.student_id || profile.value.student_id || '')
const alumniId = computed(() => authStore.voter?.alumni_id || profile.value.alumni_id || '')
const isApproved = computed(() => authStore.voter?.is_approved !== false && profile.value.is_approved !== false)

const loadProfile = async () => {
  loadingProfile.value = true
  profileError.value = ''
  try {
    const res = await api.get('voter/profile/')
    profile.value = res.data
    authStore.setVoter({
      ...(authStore.voter || {}),
      ...res.data,
    })
  } catch (err) {
    profileError.value = err.response?.data?.error || 'Failed to load your profile.'
  } finally {
    loadingProfile.value = false
  }
}

const saveProfile = async () => {
  savingProfile.value = true
  profileMessage.value = ''
  profileError.value = ''
  try {
    const res = await api.put('voter/profile/', profile.value)
    profile.value = {
      ...profile.value,
      ...res.data,
    }
    authStore.setVoter({
      ...(authStore.voter || {}),
      ...res.data,
    })
    profileMessage.value = 'Profile updated'
  } catch (err) {
    profileError.value =
      err.response?.data?.error ||
      (err.response?.data && Object.values(err.response.data).join(' ')) ||
      'Could not save changes.'
  } finally {
    savingProfile.value = false
  }
}

const loadHistory = async () => {
  historyLoading.value = true
  historyError.value = ''
  try {
    const res = await api.get('voter/history/')
    voteHistory.value = res.data?.votes || []
    nominationHistory.value = res.data?.nominations || []
  } catch (err) {
    historyError.value = err.response?.data?.error || 'Failed to load your activity.'
  } finally {
    historyLoading.value = false
  }
}

const changePassword = async () => {
  passwordMessage.value = ''
  passwordError.value = ''
  if (!passwordForm.value.current_password || !passwordForm.value.new_password) {
    passwordError.value = 'Enter current and new password.'
    return
  }
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    passwordError.value = 'New password and confirmation must match.'
    return
  }
  passwordSaving.value = true
  try {
    await api.post('voter/change-password/', passwordForm.value)
    passwordMessage.value = 'Password updated. Please log in again.'
    passwordForm.value.current_password = ''
    passwordForm.value.new_password = ''
    passwordForm.value.confirm_password = ''
    authStore.logout()
  } catch (err) {
    passwordError.value = err.response?.data?.error || 'Could not update password.'
  } finally {
    passwordSaving.value = false
  }
}

const requestAdminReset = async () => {
  pinResetMessage.value = ''
  pinResetError.value = ''
  try {
    await api.post('voter/request-reset-pin/', { identifier: authStore.voter?.voter_id || authStore.voter?.alumni_id || authStore.voter?.student_id })
    pinResetMessage.value = 'Reset request sent to admin.'
  } catch (err) {
    pinResetError.value = err.response?.data?.error || 'Could not send reset request.'
  }
}

onMounted(() => {
  loadProfile()
  loadHistory()
})
</script>

<template>
  <div class="max-w-6xl mx-auto space-y-6">
    <div class="bg-white rounded-2xl shadow-md border border-slate-200 p-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p class="text-sm text-slate-500">Welcome back</p>
        <p class="text-2xl font-semibold text-slate-800">{{ voterDisplayName }}</p>
        <p class="text-sm text-slate-500">Student ID: {{ studentId || '—' }} • Alumni ID: {{ alumniId || 'pending' }} • Voter ID: {{ voterId || '—' }}</p>
      </div>
      <div class="flex gap-2">
        <span class="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-100">Voter portal</span>
        <span
          v-if="!isApproved"
          class="px-3 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-700 border border-amber-200"
        >
          Pending approval
        </span>
        <span
          v-else-if="authStore.voter?.has_voted"
          class="px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200"
        >
          Ballot submitted
        </span>
      </div>
  </div>

  <div class="grid grid-cols-1 lg:grid-cols-3 gap-4">
    <div class="bg-white rounded-2xl shadow-md border border-slate-200 p-5 lg:col-span-2">
      <div v-if="!isApproved" class="mb-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
        Your registration is pending approval. You can review your profile, but nomination and voting unlock after verification. Alumni ID will be issued upon approval.
      </div>
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-lg font-semibold text-slate-800">Profile & Contact</h2>
        <span v-if="loadingProfile" class="text-xs text-slate-500">Loading…</span>
      </div>
        <p class="text-sm text-slate-500 mb-4">
          Keep your info current so we can reach you about elections and alumni updates.
        </p>

        <div v-if="profileError" class="mb-3 text-sm text-rose-600 bg-rose-50 border border-rose-100 rounded-xl px-3 py-2">
          {{ profileError }}
        </div>
        <div v-if="profileMessage" class="mb-3 text-sm text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-xl px-3 py-2">
          {{ profileMessage }}
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label class="text-sm font-semibold text-slate-700">First name</label>
            <input
              v-model="profile.first_name"
              type="text"
              class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
              placeholder="Juan"
            />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Middle name</label>
            <input
              v-model="profile.middle_name"
              type="text"
              class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
              placeholder="Santos"
            />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Last name</label>
            <input
              v-model="profile.last_name"
              type="text"
              class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
              placeholder="Dela Cruz"
            />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Batch year</label>
            <input
              v-model="profile.batch_year"
              type="number"
              class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
              placeholder="2010"
            />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Campus / Chapter</label>
            <input
              v-model="profile.campus_chapter"
              type="text"
              class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
              placeholder="Digos City"
            />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Email</label>
            <input
              v-model="profile.email"
              type="email"
              class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
              placeholder="you@example.com"
            />
          </div>
          <div>
            <label class="text-sm font-semibold text-slate-700">Phone</label>
            <input
              v-model="profile.phone"
              type="text"
              class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
              placeholder="+63 9xx xxx xxxx"
            />
          </div>
          <div class="flex items-center gap-2 mt-6">
            <input id="consent" v-model="profile.privacy_consent" type="checkbox" class="h-4 w-4" />
            <label for="consent" class="text-sm text-slate-700">I agree to receive updates and reminders.</label>
          </div>
        </div>

        <div class="mt-4 flex gap-2">
          <button
            class="px-4 py-2 rounded-lg bg-emerald-600 text-white font-semibold shadow-sm hover:bg-emerald-700 disabled:opacity-60"
            :disabled="savingProfile || loadingProfile"
            @click="saveProfile"
          >
            {{ savingProfile ? 'Saving…' : 'Save changes' }}
          </button>
          <button
            class="px-4 py-2 rounded-lg border border-slate-300 text-slate-700 hover:bg-slate-50"
            :disabled="loadingProfile"
            @click="loadProfile"
          >
            Refresh
          </button>
        </div>
      </div>

    <div class="bg-white rounded-2xl shadow-md border border-slate-200 p-5">
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-lg font-semibold text-slate-800">Account Snapshot</h2>
      </div>
        <ul class="text-sm text-slate-700 space-y-2">
          <li class="flex justify-between">
            <span>Status</span>
            <span class="font-semibold">
              {{ authStore.voter?.is_active === false ? 'Inactive' : isApproved ? 'Active' : 'Pending approval' }}
            </span>
          </li>
          <li class="flex justify-between">
            <span>Has voted</span>
            <span class="font-semibold">{{ authStore.voter?.has_voted ? 'Yes' : 'No' }}</span>
          </li>
          <li class="flex justify-between">
            <span>Student ID</span>
            <span class="font-semibold">{{ studentId || '—' }}</span>
          </li>
          <li class="flex justify-between">
            <span>Alumni ID</span>
            <span class="font-semibold">{{ alumniId || 'Pending' }}</span>
          </li>
          <li class="flex justify-between">
            <span>Batch year</span>
            <span class="font-semibold">{{ profile.batch_year || '—' }}</span>
          </li>
          <li class="flex justify-between">
            <span>Chapter</span>
            <span class="font-semibold">{{ profile.campus_chapter || '—' }}</span>
          </li>
        </ul>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-md border border-slate-200 p-5 lg:col-span-1">
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-lg font-semibold text-slate-800">Change password</h2>
      </div>
      <p class="text-sm text-slate-500 mb-3">Confirm with your current password to set a new one.</p>
      <div v-if="passwordError" class="mb-2 text-sm text-rose-600 bg-rose-50 border border-rose-100 rounded-xl px-3 py-2">
        {{ passwordError }}
      </div>
      <div v-if="passwordMessage" class="mb-2 text-sm text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-xl px-3 py-2">
        {{ passwordMessage }}
      </div>
      <div class="space-y-2">
        <div>
          <label class="text-sm font-semibold text-slate-700">Current password</label>
          <input
            v-model="passwordForm.current_password"
            type="password"
            class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
          />
        </div>
        <div>
          <label class="text-sm font-semibold text-slate-700">New password</label>
          <input
            v-model="passwordForm.new_password"
            type="password"
            class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
          />
        </div>
        <div>
          <label class="text-sm font-semibold text-slate-700">Confirm new password</label>
          <input
            v-model="passwordForm.confirm_password"
            type="password"
            class="w-full mt-1 rounded-lg border border-slate-200 px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-[rgba(196,151,60,0.35)]"
          />
        </div>
        <button
          class="w-full rounded-lg bg-[var(--hcad-navy)] text-white font-semibold py-2.5 shadow-sm hover:bg-[var(--hcad-navy-dark)] disabled:opacity-60"
          :disabled="passwordSaving"
          @click="changePassword"
        >
          {{ passwordSaving ? 'Updating…' : 'Update password' }}
        </button>
        <div class="pt-2 border-t border-slate-200 space-y-2">
          <p class="text-[13px] text-slate-600">Forgot your password? Request an admin reset.</p>
          <div v-if="pinResetError" class="text-sm text-rose-600 bg-rose-50 border border-rose-100 rounded-xl px-3 py-2">
            {{ pinResetError }}
          </div>
          <div v-if="pinResetMessage" class="text-sm text-emerald-700 bg-emerald-50 border border-emerald-100 rounded-xl px-3 py-2">
            {{ pinResetMessage }}
          </div>
          <button
            type="button"
            class="w-full rounded-lg border border-slate-300 bg-white text-slate-700 font-semibold py-2.5 shadow-sm hover:bg-slate-50"
            @click="requestAdminReset"
          >
            Request admin reset PIN
          </button>
        </div>
      </div>
    </div>

    <div class="bg-white rounded-2xl shadow-md border border-slate-200 p-5">
      <div class="flex items-center justify-between mb-3">
        <h2 class="text-lg font-semibold text-slate-800">Participation history</h2>
        <span v-if="historyLoading" class="text-xs text-slate-500">Loading…</span>
      </div>
      <p class="text-sm text-slate-500 mb-4">
        A running log of your nominations and ballots so you can track your engagement.
      </p>
      <div v-if="historyError" class="mb-3 text-sm text-rose-600 bg-rose-50 border border-rose-100 rounded-xl px-3 py-2">
        {{ historyError }}
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <div class="border border-slate-200 rounded-xl p-4">
          <h3 class="text-md font-semibold text-slate-800 mb-2">Votes</h3>
          <p v-if="!voteHistory.length && !historyLoading" class="text-sm text-slate-500">No votes yet.</p>
          <ul v-else class="space-y-3 max-h-72 overflow-y-auto pr-1">
            <li
              v-for="vote in voteHistory"
              :key="vote.id"
              class="rounded-lg border border-slate-200 px-3 py-2 bg-slate-50"
            >
              <p class="font-semibold text-slate-800">{{ vote.candidate_name }}</p>
              <p class="text-sm text-slate-600">{{ vote.position_name }} • {{ vote.election_name || 'Election' }}</p>
              <p class="text-xs text-slate-500">
                {{ new Date(vote.created_at).toLocaleString('en-PH', { dateStyle: 'medium', timeStyle: 'short' }) }}
              </p>
            </li>
          </ul>
        </div>
        <div class="border border-slate-200 rounded-xl p-4">
          <h3 class="text-md font-semibold text-slate-800 mb-2">Nominations</h3>
          <p v-if="!nominationHistory.length && !historyLoading" class="text-sm text-slate-500">No nominations submitted.</p>
          <ul v-else class="space-y-3 max-h-72 overflow-y-auto pr-1">
            <li
              v-for="nom in nominationHistory"
              :key="nom.id"
              class="rounded-lg border border-slate-200 px-3 py-2 bg-slate-50"
            >
              <p class="font-semibold text-slate-800">{{ nom.nominee_full_name }}</p>
              <p class="text-sm text-slate-600">{{ nom.position_name }} • {{ nom.election_name || 'Election' }}</p>
              <p class="text-xs text-slate-500 capitalize">Status: {{ nom.status }}</p>
              <p class="text-xs text-slate-500">
                {{ new Date(nom.created_at).toLocaleString('en-PH', { dateStyle: 'medium', timeStyle: 'short' }) }}
              </p>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
