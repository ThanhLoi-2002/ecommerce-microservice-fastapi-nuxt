<template>
  <component :is="layout">
    <router-view />
  </component>
  <ToastContainer />
</template>

<script setup lang="ts">
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";

import AuthLayout from "./layouts/auth.vue";
import AdminLayout from "./layouts/admin.vue";
import DefaultLayout from "./layouts/default.vue";
import ToastContainer from "./components/common/toast/ToastContainer.vue";
import { getToken } from "./utils/token";
import { useUserStore } from "./stores/user.store";

const userStore = useUserStore()

const route = useRoute();
const token = getToken();

// 👉 Nếu có token thì load user info
onMounted(async () => {
  if (token) {
    await userStore.getMeHandler();
  }
});


const layout = computed(() => {
  const name = route.meta.layout
  switch (name) {
    case "auth":
      return AuthLayout

    case "admin":
      return AdminLayout

    default:
      return DefaultLayout
  }
})
</script>