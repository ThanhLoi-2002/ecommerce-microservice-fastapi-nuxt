<template>
  <button :class="class" :type="type" :disabled="isLoading" @click="onClick">
    <span v-if="isLoading" class="d-flex align-items-center justify-content-center">
      <span class="mr-2 d-flex"><LoadingSpinner /></span>
      {{ loadingLabel || "Loading" }}
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
  loadingLabel?: string;
  type?: "button" | "submit" | "reset" | undefined;      // Loại button, mặc định là "button"
  isLoading?: boolean;  // Trạng thái loading
  class?: string;     // Class tùy chỉnh
  onClick?: () => void
}>();
</script>