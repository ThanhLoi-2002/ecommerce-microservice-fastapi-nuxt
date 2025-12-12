<template>
  <component :is="layout">
    <div class="loading-container" v-if="isAuthLoading">
      <div class="text-center">
        <LoadingSpinner size="40px" />
        <p>Loading....</p>
      </div>
    </div>
    <router-view v-else />
  </component>
  <ToastContainer />
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";

import AuthLayout from "./layouts/auth.vue";
import AdminLayout from "./layouts/admin.vue";
import DefaultLayout from "./layouts/default.vue";
import NoLayout from "./layouts/noLayout.vue";
import ToastContainer from "./components/common/toast/ToastContainer.vue";
import { storeToRefs } from "pinia";
import LoadingSpinner from "./components/common/loading/LoadingSpinner.vue";
import { useAuthStore } from "./stores/auth.store";

const authStore = useAuthStore()
const { isAuthLoading } = storeToRefs(authStore)
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

<style>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>