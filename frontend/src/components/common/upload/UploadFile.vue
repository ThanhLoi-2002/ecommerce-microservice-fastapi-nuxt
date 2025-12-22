<template>
  <div class="d-flex align-items-center justify-content-center w-100">
    <div
      class="w-100 border border-secondary rounded p-5 bg-light text-center position-relative"
      :class="{ 'border-primary': isDragging }"
      style="min-height: 300px; border-style: dashed !important; cursor: pointer;"
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      @click="($refs.fileInput as any).click()"
    >
      <!-- Khi đã có ảnh: hiển thị preview -->
      <div v-if="previewUrl" class="h-100 d-flex flex-column align-items-center justify-content-center">
        <img :src="previewUrl" class="img-fluid rounded shadow" style="max-height: 250px;" alt="Preview" />
        <p class="mt-3 text-muted">
          <small>Click hoặc kéo thả để <strong>đổi ảnh</strong></small>
        </p>
        <p class="text-muted">
          <small>Kích thước tối đa: <strong>30MB</strong></small>
        </p>
      </div>

      <!-- Khi chưa có ảnh: hiển thị hướng dẫn upload -->
      <div v-else class="d-flex flex-column align-items-center justify-content-center py-5">
        <i class="pi pi-upload" style="font-size: xx-large"/>
        <p class="mb-2 text-muted">
          <small>Kéo thả file vào đây hoặc click để chọn</small>
        </p>
        <p class="mb-3 text-muted">
          <small>Kích thước tối đa: <strong>30MB</strong></small>
        </p>
        <button type="button" class="btn btn-primary">
          Chọn file
        </button>
      </div>
    </div>

    <!-- Hidden file input -->
    <input
      ref="fileInput"
      type="file"
      class="d-none"
      accept="image/*"
      @change="handleFileChange"
    />
  </div>
</template>

<script setup lang="ts">
import type { ImageType } from '@/types/common';
import { ref } from 'vue';

const props = defineProps<{
  chooseFile: (file: File) => void
  image?: ImageType
}>()

const previewUrl = ref(props.image?.url || null);
const selectedFile = ref<any>(null); // Bạn có thể emit file này ra parent nếu cần upload
const isDragging = ref(false);

const MAX_SIZE = 30 * 1024 * 1024; // 30MB

const handleFile = (file: File) => {
  if (!file) return;

  if (file.size > MAX_SIZE) {
    alert('File quá lớn! Vui lòng chọn file dưới 30MB.');
    return;
  }

  if (!file.type.startsWith('image/')) {
    alert('Vui lòng chọn file ảnh!');
    return;
  }

  selectedFile.value = file;
  props.chooseFile(file)

  const reader = new FileReader();
  reader.onload = (e: any) => {
    previewUrl.value = e.target.result;
  };
  reader.readAsDataURL(file);
};

const handleDrop = (e: any) => {
  isDragging.value = false;
  const file = e.dataTransfer.files[0];
  handleFile(file);
};

const handleFileChange = (e: any) => {
  const file = e.target.files[0];
  handleFile(file);
};

// Nếu cần emit file ra component cha:
// const emit = defineEmits(['update:file']);
// watch(selectedFile, (newFile) => emit('update:file', newFile));
</script>