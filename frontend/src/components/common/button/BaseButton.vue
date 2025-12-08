<template>
  <button :class="class" :type="type" :disabled="isLoading">
    <span v-if="isLoading">
      <LoadingSpinner />
    </span>
    <span v-else>
      {{ label }}
    </span>
  </button>
</template>

<script setup lang="ts">
import LoadingSpinner from '../loading/LoadingSpinner.vue';

// Định nghĩa các props cho button
const props = defineProps<{
  label: string;       // Văn bản hiển thị trên button
  type?: "button" | "submit" | "reset" | undefined ;      // Loại button, mặc định là "button"
  isLoading: boolean;  // Trạng thái loading
  class?: string;     // Class tùy chỉnh
}>();
</script>