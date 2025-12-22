<template>
  <div class="custom-switch-wrapper">
    <label class="custom-switch" :class="[sizeClass, colorClass, { 'disabled': disabled || isLoading }]">
      <input 
        type="checkbox" 
        class="custom-switch-input" 
        :checked="localValue" 
        :disabled="disabled || isLoading"
        @change="handleChange" 
      />
      <span class="custom-switch-slider"></span>
    </label>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { computed } from 'vue';

interface Props {
  modelValue: boolean;
  onClick: () => Promise<void>
  label?: string;
  disabled?: boolean;
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'success' | 'danger' | 'warning' | 'info';
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  size: 'sm',
  color: 'success'
});

const emit = defineEmits<{
  'update:modelValue': [value: boolean];
}>();

const isLoading = ref(false);
const localValue = ref(props.modelValue);

// Sync localValue với modelValue từ parent
watch(() => props.modelValue, (newVal) => {
  localValue.value = newVal;
});

const sizeClass = computed(() => {
  return `switch-${props.size}`;
});

const colorClass = computed(() => {
  return `switch-${props.color}`;
});

const handleChange = async () => {
  if (isLoading.value) return;
  
  isLoading.value = true;
  
  try {
    // Gọi API
    await props.onClick();
    
    // Chỉ cập nhật sau khi API thành công
    const newValue = !localValue.value;
    localValue.value = newValue;
    emit('update:modelValue', newValue);
  } catch (error) {
    // Nếu API fail, giữ nguyên trạng thái cũ
    console.error('Switch update failed:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.custom-switch-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.custom-switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
  cursor: pointer;
}

.custom-switch.disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.custom-switch-input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}

.custom-switch-slider {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 24px;
}

.custom-switch-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Khi checked - nút trượt sang phải */
.custom-switch-input:checked+.custom-switch-slider:before {
  transform: translateX(26px);
}

.custom-switch-input:disabled+.custom-switch-slider {
  cursor: not-allowed;
}

.custom-switch-label {
  cursor: pointer;
  user-select: none;
  font-weight: 500;
}

.custom-switch.disabled+.custom-switch-label {
  cursor: not-allowed;
}

/* Sizes */
.switch-sm {
  width: 40px;
  height: 20px;
}

.switch-sm .custom-switch-slider:before {
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
}

.switch-sm .custom-switch-input:checked+.custom-switch-slider:before {
  transform: translateX(20px);
}

.switch-md {
  width: 50px;
  height: 24px;
}

.switch-lg {
  width: 60px;
  height: 28px;
}

.switch-lg .custom-switch-slider:before {
  height: 22px;
  width: 22px;
  left: 3px;
  bottom: 3px;
}

.switch-lg .custom-switch-input:checked+.custom-switch-slider:before {
  transform: translateX(32px);
}

/* Colors - Background khi bật */
.switch-success .custom-switch-input:checked+.custom-switch-slider {
  background-color: #28a745;
}

.switch-primary .custom-switch-input:checked+.custom-switch-slider {
  background-color: #007bff;
}

.switch-danger .custom-switch-input:checked+.custom-switch-slider {
  background-color: #dc3545;
}

.switch-warning .custom-switch-input:checked+.custom-switch-slider {
  background-color: #ffc107;
}

.switch-info .custom-switch-input:checked+.custom-switch-slider {
  background-color: #17a2b8;
}

/* Focus state */
.custom-switch-input:focus+.custom-switch-slider {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}
</style>