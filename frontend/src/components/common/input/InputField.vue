<template>
  <div class="form-group mb-3">
    <label class="d-flex align-items-center font-weight-normal">
      {{ label }}
      <span v-if="required" class="text-danger ml-1">*</span>
    </label>

    <input
      :value="modelValue"
      :type="type"
      class="form-control"
      :class="{ 'is-invalid': error }"
      @input="onInput"
    />

    <div class="invalid-feedback" v-if="error">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  label: string;
  modelValue: string;
  type?: string;
  error?: string;
  required?: boolean;
}>();

const emit = defineEmits(["update:modelValue"]);

const onInput = (e: Event) => {
  emit("update:modelValue", (e.target as HTMLInputElement).value);
};
</script>
