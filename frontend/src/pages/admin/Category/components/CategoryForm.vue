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
                <option :value="null">-- Không có (Danh mục gốc) --</option>
                <option v-for="cat in parentCategories" :key="cat.id" :value="cat.id"
                    :disabled="props.id !== undefined && cat.id === props.id">
                    {{ cat.name }} ({{ categoryGender(cat.gender) }})
                </option>
            </select>
            <div class="position-absolute" style="right: 20px; top: 75%; transform: translateY(-55%);">
                <LoadingSpinner size="16px" v-if="isLoadingParentCategories" />
            </div>
        </div>

        <Radio label="Chọn giới tính" :options="genderOptions" :value="categoryForm.gender" :chooseRadio="chooseGender"
            name="gender" />

        <div class="form-group">
            <div class="form-check d-flex align-items-center">
                <input type="checkbox" class="form-check-input" id="statusSwitch" v-model="categoryForm.status" />
                <label class="form-check-label" for="statusSwitch">
                    {{ categoryForm.status ? '✓ Hoạt động' : '✗ Không hoạt động' }}
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
import { GenderEnum, type CategoryFilter } from '@/types/common';
import type { CategoryType } from '@/types/entities';
import { reactive, ref } from 'vue';
import { genderOptions } from '@/utils/constants';
import type { CategoryFormType } from '@/types/form/category.form';
import { categoryGender } from '@/utils/translateFromEnum';

const props = defineProps<{
    closeModal: () => void
    id?: number
    filters: CategoryFilter
    resetFilters: () => void
}>()

const categoryFormDefaultValue = (): CategoryFormType => ({
    name: "",
    description: "",
    img: undefined,
    pid: null,
    status: true,
    gender: GenderEnum.MALE
})


const { createOrUpdate, getParentCategories, getCategory, getCategories, changeImage } = useCategory()

let categoryForm = reactive<CategoryFormType>(categoryFormDefaultValue());
const isSubmitting = ref(false)
const isLoading = ref(false)
const isLoadingParentCategories = ref(false)
const parentCategories = ref<CategoryType[]>([])
const errorMessage = ref(""); // To hold the error message

const submitForm = async () => {
    if (!categoryForm.img) {
        errorMessage.value = 'Vui lòng chọn một ảnh trước khi gửi!'; // Show error if no image is selected
        return; // Prevent form submission if no image is selected
    }

    isSubmitting.value = true
    const result = await createOrUpdate(categoryForm, props.id)
    isSubmitting.value = false

    // close form if success
    if (result) {
        props.closeModal()
        props.resetFilters()
        getCategories({ page: 1, limit: props.filters.limit })
    }
}

const chooseFile = async (file: File) => {
    if (!props.id) {
        categoryForm.img = file
    } else {
        categoryForm.img = await changeImage(props.id, file, categoryForm.img.public_id)
    }
    errorMessage.value = ''
}

const chooseGender = (value: any) => {
    categoryForm.gender = value
}

const init = async () => {
    if (props.id) {
        isLoading.value = true
        Object.assign(categoryForm, (await getCategory(props.id)))
        isLoading.value = false
    } else {
        Object.assign(categoryForm, categoryFormDefaultValue)
    }
    isLoadingParentCategories.value = true
    parentCategories.value = await getParentCategories()
    isLoadingParentCategories.value = false
}
init()
</script>