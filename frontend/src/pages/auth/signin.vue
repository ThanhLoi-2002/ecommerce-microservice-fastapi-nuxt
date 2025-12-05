<template>
  <div class="bg-white h-screen flex justify-center items-center">
    <div class="w-[300px]">
      <h1 class="text-2xl mb-5 font-semibold">Sign In</h1>

      <form @submit.prevent="onSubmit" class="flex flex-col gap-3">

        <!-- EMAIL -->
        <div>
          <BaseInput
            v-model="values.email"
            type="text"
            placeholder="info@gmail.com"
          />
          <FormError :errors="errors.email ? [errors.email] : []" />
        </div>

        <!-- PASSWORD -->
        <div>
          <BaseInput
            v-model="values.password"
            type="password"
            placeholder="password"
          />
          <FormError :errors="errors.password ? [errors.password] : []" />
        </div>

        <!-- <BaseBtn :loading="auth.loading" label="Sign in" /> -->

      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
// import FormError from "@/components/FormError.vue"
// import BaseInput from "@/components/BaseInput.vue"
// import BaseBtn from "@/components/BaseBtn.vue"
// import { useAuthStore } from "@/stores/auth"

import { useForm } from "vee-validate"
import { z } from "zod"
import { toFormValidator } from "@vee-validate/zod"

// const auth = useAuthStore()

const LoginSchema = z.object({
  email: z.string().email("Email không hợp lệ"),
  password: z.string().min(1, "Mật khẩu không được để trống"),
})

const { errors, values, handleSubmit } = useForm({
  validationSchema: toFormValidator(LoginSchema),
})

const onSubmit = handleSubmit(async (formData) => {
  // await auth.login(formData)
})
</script>
