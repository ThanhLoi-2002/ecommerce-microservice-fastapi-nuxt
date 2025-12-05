<template>
  <div class="toast-container">
    <div
      v-for="toast in toasts"
      :key="toast.id"
      :class="['toast', toast.type]"
      @click="remove(toast.id)"
    >
      <span>{{ toast.message }}</span>
      <button class="close-btn" @click.stop="remove(toast.id)">×</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useToast } from '../../../composables/useToast';

const { toasts, remove } = useToast()
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  min-width: 300px;
  padding: 14px 20px;
  border-radius: 8px;
  color: white;
  font-weight: 500;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  justify-content: space-between;
  animation: slideIn 0.3s ease;
  cursor: pointer;
}

.toast.success { background: #10b981; }
.toast.error   { background: #ef4444; }
.toast.warning { background: #f59e0b; }
.toast.info    { background: #3b82f6; }

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
  margin-left: 15px;
  opacity: 0.8;
}

.close-btn:hover { opacity: 1; }

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
</style>