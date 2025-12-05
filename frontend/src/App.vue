<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

import AuthLayout from "./layouts/auth.vue";
import AdminLayout from "./layouts/admin.vue";
import DefaultLayout from "./layouts/default.vue";

const route = useRoute();

const layout = computed(() => {
  const name = route.meta.layout
  console.log(name)
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