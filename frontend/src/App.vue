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
import NoLayout from "./layouts/noLayout.vue";
import ToastContainer from "./components/common/toast/ToastContainer.vue";

const route = useRoute();

const layout = computed(() => {
  const name = route.meta.layout
  switch (name) {
    case "auth":
      return AuthLayout

    case "admin":
      return AdminLayout

    case "default":
      return DefaultLayout

    default:
      return NoLayout
  }
})
</script>