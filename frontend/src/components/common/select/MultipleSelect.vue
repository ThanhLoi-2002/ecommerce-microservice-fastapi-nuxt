<template>
  <div class="multiple-select">
    <div class="form-group">
      <label v-if="label" class="font-weight-bold">{{ label }}</label>
      
      <div class="position-relative">
        <!-- Main select box -->
        <div 
          class="form-control d-flex flex-wrap align-items-center"
          style="min-height: 48px; cursor: pointer"
          @click="toggleDropdown"
        >
          <span v-if="selectedItems.length === 0" class="text-muted">
            {{ placeholder }}
          </span>
          
          <span 
            v-for="item in selectedItems"
            :key="item.id"
            class="badge badge-primary mr-2 mb-1 d-flex align-items-center"
            style="font-size: 14px; padding: 6px 10px"
          >
            {{ item.label }}
            <button
              class="btn btn-sm ml-2 p-0"
              style="background: none; border: none; color: white; font-size: 16px; line-height: 1"
              @click.stop="removeItem(item.id)"
            >
              ×
            </button>
          </span>
        </div>

        <!-- Dropdown menu -->
        <div 
          v-if="isOpen"
          class="card position-absolute w-100 mt-1"
          style="z-index: 1000; max-height: 300px; overflow: auto"
        >
          <div class="card-body p-2">
            <!-- Search input -->
            <input
              v-model="searchTerm"
              type="text"
              class="form-control form-control-sm mb-2"
              placeholder="Tìm kiếm..."
              @click.stop
            />

            <!-- Clear all button -->
            <button
              v-if="selectedItems.length > 0"
              class="btn btn-sm btn-link text-danger p-0 mb-2"
              @click.stop="clearAll"
            >
              Xóa tất cả
            </button>

            <!-- Options list -->
            <div class="list-group list-group-flush">
              <button
                v-for="option in filteredOptions"
                :key="option.id"
                class="list-group-item list-group-item-action d-flex align-items-center"
                :class="{ active: isSelected(option.id) }"
                style="cursor: pointer"
                @click.stop="toggleOption(option)"
              >
                <input
                  type="checkbox"
                  :checked="isSelected(option.id)"
                  class="mr-2"
                  @change.stop
                />
                {{ option.label }}
              </button>
            </div>

            <div v-if="filteredOptions.length === 0" class="text-center text-muted py-2">
              Không tìm thấy kết quả
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

interface Option {
  id: number;
  value: string;
  label: string;
}

interface Props {
  modelValue: Option[];
  options: Option[];
  label?: string;
  placeholder?: string;
}

const props = withDefaults(defineProps<Props>(), {
  label: '',
  placeholder: 'Chọn một hoặc nhiều tùy chọn...'
});

const emit = defineEmits<{
  'update:modelValue': [value: Option[]];
}>();

const isOpen = ref(false);
const searchTerm = ref('');

const selectedItems = computed(() => props.modelValue);

const filteredOptions = computed(() => {
  return props.options.filter(option =>
    option.label.toLowerCase().includes(searchTerm.value.toLowerCase())
  );
});

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};

const isSelected = (id: number) => {
  return selectedItems.value.some(item => item.id === id);
};

const toggleOption = (option: Option) => {
  const exists = selectedItems.value.find(item => item.id === option.id);
  if (exists) {
    emit('update:modelValue', selectedItems.value.filter(item => item.id !== option.id));
  } else {
    emit('update:modelValue', [...selectedItems.value, option]);
  }
};

const removeItem = (id: number) => {
  emit('update:modelValue', selectedItems.value.filter(item => item.id !== id));
};

const clearAll = () => {
  emit('update:modelValue', []);
};
</script>

<style scoped>
.multiple-select {
  width: 100%;
}
</style>