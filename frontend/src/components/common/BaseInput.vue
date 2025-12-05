<template>
  <div class="w-full">
    <label v-if="label" class="block text-sm font-medium mb-1">{{ label }}</label>

    <input
      v-bind="$attrs"
      :type="type"
      v-model="model"
      class="w-full px-3 py-2 rounded-md border border-gray-300 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  modelValue: string;
  type?: string;
  label?: string;
}>();

const emits = defineEmits(["update:modelValue"]);

const model = computed({
  get: () => props.modelValue,
  set: (value) => emits("update:modelValue", value),
});
</script>
