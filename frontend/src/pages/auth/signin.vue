<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px">
      <h4 class="text-center mb-4">Sign In</h4>

      <form @submit.prevent="onSubmit" novalidate>
        <InputField label="Email" name="email" type="email" v-model="signInForm.email" required
          placeholder="user@gmail.com" />

        <InputField label="Password" name="password" type="password" v-model="signInForm.password" required
          placeholder="Enter password" />

        <BaseButton label="Sign In" :isLoading="isLoading" class="btn btn-primary w-100" />

        <div class="text-center mt-3">
          <small>
            Already an account?
            <router-link to="/auth/signup">Sign up</router-link>
          </small>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useAuth } from "@/composables/useAuth";
import InputField from "../../components/common/input/InputField.vue";
import { useAuthStore } from "@/stores/auth.store";
import { storeToRefs } from "pinia";
import BaseButton from "@/components/common/button/BaseButton.vue";

const { signInForm } = useAuth()
const authStore = useAuthStore()
const { isLoading } = storeToRefs(authStore)

const onSubmit = () => {
  authStore.signInHandler(signInForm)
};
</script>
