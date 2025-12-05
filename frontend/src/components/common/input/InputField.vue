<!-- components/common/input/InputField.vue -->
<template>
  <div class="form-group mb-3">
    <label class="d-flex align-items-center font-weight-normal">
      {{ label }}
      <span v-if="required" class="text-danger ml-1">*</span>
    </label>

    <input
      :type="type || 'text'"
      class="form-control"
      :value="modelValue"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      :required="required"
      :name="name"
      :placeholder="placeholder"
    />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  label: string;
  name?: string;
  type?: string;
  required?: boolean;
  modelValue: string;        // bắt buộc có để v-model hoạt động
  placeholder?: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>();
</script>