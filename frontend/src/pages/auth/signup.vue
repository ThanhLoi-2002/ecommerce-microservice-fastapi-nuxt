<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px">
      <h4 class="text-center mb-4">Đăng ký</h4>

      <form @submit.prevent="onSubmit" novalidate>
        <InputField
          label="Họ tên"
          v-model="values.name"
          :error="errors.name"
          required
        />
        <!-- Họ tên
        <div class="form-group mb-3">
          <label className="d-flex align-items-center font-weight-normal">
            Họ tên {isRequired &&
            <div className="has-error">*</div>
            }
          </label>

          <input
            v-model="values.name"
            type="text"
            class="form-control"
            :class="{ 'is-invalid': errors.name }"
          />
          <div class="invalid-feedback">{{ errors.name }}</div>
        </div> -->

        <!-- Email -->
        <div class="form-group mb-3">
          <label>Email</label>
          <input
            v-model="values.email"
            type="email"
            class="form-control"
            :class="{ 'is-invalid': errors.email }"
          />
          <div class="invalid-feedback">{{ errors.email }}</div>
        </div>

        <!-- Mật khẩu -->
        <div class="form-group mb-3">
          <label>Mật khẩu</label>
          <input
            v-model="values.password"
            type="password"
            class="form-control"
            :class="{ 'is-invalid': errors.password }"
          />
          <div class="invalid-feedback">{{ errors.password }}</div>
        </div>

        <button class="btn btn-primary w-100" type="submit">Đăng ký</button>

        <div class="text-center mt-3">
          <small>
            Bạn đã có tài khoản?
            <router-link to="/login">Đăng nhập</router-link>
          </small>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">

import { useForm } from "vee-validate";
import { toTypedSchema } from "@vee-validate/zod";
import { signupSchema } from "../../schemas/auth";
import InputField from "@/components/common/input/InputField.vue";

const { handleSubmit, errors, values } = useForm({
  validationSchema: toTypedSchema(signupSchema),
});

const onSubmit = handleSubmit((formData) => {
  console.log("Form submit:", formData);
});
</script>
