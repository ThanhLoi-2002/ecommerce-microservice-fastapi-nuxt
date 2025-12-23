<template>
    <form @submit.prevent="submitForm">
        <div class="form-group">
            <label>Tên <span class="text-danger">*</span></label>
            <input type="text" class="form-control" v-model="sizeForm.name" required
                placeholder="Nhập tên danh mục..." />
        </div>

        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
                Hủy
            </button>
            <BaseButton :isLoading="isSubmitting" :label="size ? 'Cập nhật' : 'Thêm mới'" class="btn btn-primary" />
        </div>
    </form>
</template>
<script setup lang="ts">
import BaseButton from '@/components/common/button/BaseButton.vue';
import type { SizeType } from '@/types/entities';
import { reactive, ref, watch } from 'vue';
import type { SizeFormType } from '@/types/form/size.form';
import { useSize } from '@/composables/useSize';

const props = defineProps<{
    closeModal: () => void
    size?: SizeType
}>()

const sizeFormDefaultValue = (): SizeFormType => ({
    name: "",
})


const { create, update } = useSize()

let sizeForm = reactive<SizeFormType>(sizeFormDefaultValue());
const isSubmitting = ref(false)

const submitForm = async () => {
    isSubmitting.value = true

    let result
    if (props.size) result = await update(props.size.id, sizeForm)
    else result = await create(sizeForm)

    isSubmitting.value = false

    // close form if success
    if (result) {
        props.closeModal()
    }
}

// Watch for changes in props.size
watch(() => props.size, (newSize) => {
    if (newSize) {
        sizeForm.name = newSize.name;  // Update sizeForm.name if size exists
    } else {
        sizeForm.name = "";  // Reset name if no size
    }
}, { immediate: true })  // Run immediately on component mount
</script>