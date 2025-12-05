<template>
  <div class="d-flex justify-content-center align-items-center">
    <div class="card p-4 shadow" style="width: 380px">
      <h4 class="text-center mb-4">Đăng nhập</h4>

      <form @submit.prevent="onSubmit">
        <div class="form-group mb-3">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            class="form-control"
            placeholder="Nhập email"
            required
          />
        </div>

        <div class="form-group mb-3">
          <label>Mật khẩu</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            placeholder="Nhập mật khẩu"
            required
          />
        </div>

        <button class="btn btn-primary w-100" type="submit">Đăng nhập</button>

        <div class="text-center mt-3">
          <small
            >Bạn chưa có tài khoản?
            <router-link to="/signup">Đăng ký</router-link>
          </small>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const email = ref("");
const password = ref("");

const onSubmit = () => {
  console.log("Login data:", email.value, password.value);
};
</script>
