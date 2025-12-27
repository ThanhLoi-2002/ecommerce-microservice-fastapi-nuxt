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
import { computed, onBeforeUnmount, watch } from "vue";
import { useRoute } from "vue-router";

import AuthLayout from "./layouts/auth.vue";
import AdminLayout from "./layouts/admin.vue";
import DefaultLayout from "./layouts/default.vue";
import ChatLayout from "./layouts/chat.vue";
import NoLayout from "./layouts/noLayout.vue";
import ToastContainer from "./components/common/toast/ToastContainer.vue";
import { storeToRefs } from "pinia";
import LoadingSpinner from "./components/common/loading/LoadingSpinner.vue";
import { useAuthStore } from "./stores/auth.store";
import { useSocket } from "./composables/useSocket";
import { useUserStore } from "./stores/user.store";

const authStore = useAuthStore()
const { isAuthLoading } = storeToRefs(authStore)
const userStore = useUserStore()
const { user } = storeToRefs(userStore)
const route = useRoute();
const socket = useSocket()

// khi user login → emit user_id
watch(
  user,
  (u) => {
    if (u?.id) {
      socket.auth = {
        user_id: u.id,   // ✅ set trước
      };

      socket.connect(); // ✅ rồi mới connect
    } else {
      socket.disconnect();
    }
  },
  { immediate: true }
);

onBeforeUnmount(() => {
  socket.disconnect();
});


const layout = computed(() => {
  const name = route.meta.layout
  switch (name) {
    case "auth":
      return AuthLayout

    case "admin":
      return AdminLayout

    case "default":
      return DefaultLayout
    
    case "chat":
      return ChatLayout

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