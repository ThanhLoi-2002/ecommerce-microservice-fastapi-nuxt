<template>
  <div class="spinner"></div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.spinner {
  width:25px;        /* Đường kính của spinner */
  height:24px;       /* Đường kính của spinner */
  border: 4px solid rgba(255, 255, 255, 0.3); /* Biên mờ */
  border-top: 4px solid #3498db; /* Biên màu cho hiệu ứng loading */
  border-radius: 50%;  /* Để tạo hình tròn */
  animation: spin 1s linear infinite; /* Hiệu ứng xoay */
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>