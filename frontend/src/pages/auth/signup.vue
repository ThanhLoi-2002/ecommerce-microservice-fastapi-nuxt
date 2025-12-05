<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px">
      <h4 class="text-center mb-4">Sign Up</h4>

      <form @submit.prevent="onSubmit">
        <InputField label="Name" name="name" v-model="signUpForm.name" required />

        <InputField label="Email" name="email" v-model="signUpForm.email" required />

        <InputField label="Password" name="password" v-model="signUpForm.password" type="password" required />

        <button class="btn btn-primary w-100" type="submit">Sign Up</button>

        <div class="text-center mt-3">
          <small>
            Already an account?
            <router-link to="/signin">Login</router-link>
          </small>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import InputField from "../../components/common/input/InputField.vue";
import { useAuth } from "../../composables/useAuth";

const { signUpHandler, signUpForm } = useAuth()


const onSubmit = () => {
  signUpHandler(signUpForm)
};
</script>
