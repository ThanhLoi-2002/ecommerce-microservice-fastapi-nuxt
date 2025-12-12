<template>
  <div :class="['pi pi-spinner-dotted', 'spinning']" :style="{ fontSize: size }"></div>
</template>


<script setup lang="ts">
const props = defineProps({
  size: {
    type: String,
    default: '20px', // Giá trị mặc định
  },
});
</script>

<style>
.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>