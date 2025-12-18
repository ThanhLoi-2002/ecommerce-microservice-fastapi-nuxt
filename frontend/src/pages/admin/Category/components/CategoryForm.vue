<template>
    <div v-if="isLoading" class="text-center">
        <LoadingSpinner />
    </div>
    <form @submit.prevent="submitForm" v-else>

        <div class="form-group">
            <label>Tên danh mục <span class="text-danger">*</span></label>
            <input type="text" class="form-control" v-model="categoryForm.name" required
                placeholder="Nhập tên danh mục..." />
        </div>

        <div class="form-group">
            <label>Mô tả</label>
            <textarea class="form-control" v-model="categoryForm.description" placeholder="Nhập mô tả..."
                style="height: 100px;" />
        </div>

        <div class="form-group">
            <label>Hình ảnh</label>
            <UploadFile :chooseFile="chooseFile" :image="categoryForm.img" />
            <!-- Error message -->
            <p v-if="errorMessage" class="text-danger mt-2">{{ errorMessage }}</p>
        </div>

        <div class="form-group position-relative">
            <label>Danh mục cha</label>
            <select v-model="categoryForm.pid" class="form-control">
                <option :value="undefined">-- Không có (Danh mục gốc) --</option>
                <option v-for="cat in parentCategories" :key="cat.id" :value="cat.id"
                    :disabled="props.id !== undefined && cat.id === props.id">
                    {{ cat.name }}
                </option>
            </select>
            <div class="position-absolute" style="right: 20px; top: 75%; transform: translateY(-55%);">
                <LoadingSpinner size="16px" v-if="isLoadingParentCategories" />
            </div>
        </div>

        <Radio label="Chọn giới tính" :options="genderOptions" :value="categoryForm.gender" :chooseRadio="chooseGender"
            name="gender" />

        <div class="form-group">
            <div class="custom-control custom-switch">
                <input type="checkbox" class="custom-control-input" id="statusSwitch" v-model="categoryForm.status" />
                <label class="custom-control-label" for="statusSwitch">
                    Trạng thái: {{ categoryForm.status ? '✓ Hoạt động' : '✗ Không hoạt động' }}
                </label>
            </div>
        </div>

        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
                Hủy
            </button>
            <BaseButton :isLoading="isSubmitting" :label="id ? 'Cập nhật' : 'Thêm mới'" class="btn btn-primary" />
        </div>
    </form>
</template>
<script setup lang="ts">
import BaseButton from '@/components/common/button/BaseButton.vue';
import LoadingSpinner from '@/components/common/loading/LoadingSpinner.vue';
import Radio from '@/components/common/radio/Radio.vue';
import UploadFile from '@/components/common/upload/UploadFile.vue';
import { useCategory } from '@/composables/useCategory';
import type { CategoryFilter } from '@/types/common';
import type { CategoryType } from '@/types/entities';
import { onBeforeMount, onMounted, onUpdated, ref, watch } from 'vue';
import { genderOptions } from '@/utils/constants';

const props = defineProps<{
    closeModal: () => void
    id?: number
    filters: CategoryFilter
    resetFilters: () => void
}>()

const { categoryForm, createOrUpdate, getParentCategories, getCategory, getCategories } = useCategory()
const isSubmitting = ref(false)
const isLoading = ref(false)
const isLoadingParentCategories = ref(false)
const category = ref<CategoryType | undefined>(undefined)
const parentCategories = ref<CategoryType[]>([])
const errorMessage = ref(""); // To hold the error message

const submitForm = async () => {
    if (!categoryForm.img) {
        errorMessage.value = 'Vui lòng chọn một ảnh trước khi gửi!'; // Show error if no image is selected
        return; // Prevent form submission if no image is selected
    }

    isSubmitting.value = true
    const result = await createOrUpdate(categoryForm)
    isSubmitting.value = false

    // close form if success
    if (result) {
        props.closeModal()
        props.resetFilters()
        getCategories({ page: 1, limit: props.filters.limit })
    }
}

const chooseFile = (file: any) => {
    categoryForm.img = file
}

const chooseGender = (value: any) => {
    categoryForm.gender = value
}

const init = async () => {
    if (props.id) {
        isLoading.value = true
        category.value = await getCategory(props.id)
        isLoading.value = false
    }
    isLoadingParentCategories.value = true
    parentCategories.value = await getParentCategories()
    isLoadingParentCategories.value = false
}
init()
// onUpdated(async () => {

// })

watch(
    category,
    (val) => {
        if (!val) return

        // Update categoryForm fields directly
        Object.assign(categoryForm, val);
    },
    { immediate: true }
)
</script>