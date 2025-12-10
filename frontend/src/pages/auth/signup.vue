<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px">
      <h4 class="text-center mb-4">Sign Up</h4>

      <form @submit.prevent="onSubmit">
        <InputField label="Name" name="name" v-model="signUpForm.name" required />

        <InputField label="Email" name="email" v-model="signUpForm.email" required />

        <InputField label="Password" name="password" v-model="signUpForm.password" type="password" required />

        <BaseButton label="Sign Up" :isLoading="isLoading" class="btn btn-primary w-100" />
        <div class="text-center mt-3">
          <small>
            Already an account?
            <router-link to="/auth/signin">Login</router-link>
          </small>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "@/stores/auth.store";
import InputField from "../../components/common/input/InputField.vue";
import { useAuth } from "../../composables/useAuth";
import { storeToRefs } from "pinia";
import BaseButton from "@/components/common/button/BaseButton.vue";

const { signUpForm } = useAuth()
const authStore = useAuthStore()
const { isLoading } = storeToRefs(authStore)


const onSubmit = () => {
  authStore.signUpHandler(signUpForm)
};
</script>
