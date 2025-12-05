<template>
  <div class="bg-white h-screen">
    <div class="flex justify-between">
      <div></div>
      <div class="w-[300px] mt-20">
        <div class="flex flex-col gap-2">
          <h1 class="text-2xl mb-3">Sign up</h1>
          <FormError :errors="v$.name.$errors">
            <BaseInput
              v-model="registerInput.name"
              :type="'text'"
              :placeholder="'name'"
            />
          </FormError>

          <FormError :errors="v$.email.$errors">
            <BaseInput
              v-model="registerInput.email"
              :type="'text'"
              :placeholder="'info@gmail.com'"
            />
          </FormError>

          <FormError :errors="v$.password.$errors">
            <BaseInput
              v-model="registerInput.password"
              :type="'password'"
              :placeholder="'password'"
            />
          </FormError>

          <BaseBtn
            @click="submitInput"
            :loading="loading"
            label="Sign up"
          ></BaseBtn>

          <p
            class="text-sm font-normal text-center text-gray-700 dark:text-gray-500 sm:text-start"
          >
            Already have an account?
            <router-link
              to="/signin"
              class="text-indigo-500 hover:text-brand-600 font-semibold"
              >Sign in</router-link
            >
          </p>
        </div>
      </div>
      <div></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useVuelidate } from "@vuelidate/core";
import { required, email } from "@vuelidate/validators";
import { useSignUpStore } from '../../stores/auth.store'

const rules = {
  name: { required },
  email: { required, email }, // Matches state.firstName
  password: { required }, // Matches state.lastName
};

const signUpStore = useSignUpStore();
const { registerInput } = storeToRefs(signUpStore);

const v$ = useVuelidate(rules, registerInput);
const loading = ref(false);
const router = useRouter();

async function submitInput() {
  const isValid = await v$.$validate();
  if (!isValid) return;
  try {
    loading.value = true;
    const res = await fetch("/api/auth/register", {
      method: "POST",
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerInput.value),
    });
    loading.value = false;
    router.push("/auth/email-verification");
  } catch (error) {
    loading.value = false;
    console.error(error);
  }
}

function showLoginOrSignUpError(error) {
  console.error(error);
}
</script>