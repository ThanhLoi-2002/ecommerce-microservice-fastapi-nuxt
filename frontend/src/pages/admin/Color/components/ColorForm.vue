<template>
    <form @submit.prevent="submitForm">
        <div class="form-group">
            <label>Tên <span class="text-danger">*</span></label>
            <input type="text" class="form-control" v-model="colorForm.name" required
                placeholder="Nhập tên danh mục..." />
        </div>
        <div class="form-group">
            <label>Code <span class="text-danger">*</span></label>
            <input type="text" class="form-control" v-model="colorForm.code" required placeholder="Nhập code..." />
        </div>
        <div class="form-group">
            <label>Code <span class="text-danger">*</span></label>
            <input type="color" class="form-control" v-model="colorForm.code" required />
        </div>

        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">
                Hủy
            </button>
            <BaseButton :isLoading="isSubmitting" :label="color ? 'Cập nhật' : 'Thêm mới'" class="btn btn-primary" />
        </div>
    </form>
</template>

<script setup lang="ts">
import BaseButton from '@/components/common/button/BaseButton.vue';
import type { ColorType } from '@/types/entities';
import { reactive, ref, watch } from 'vue';
import { useSize } from '@/composables/useSize';
import type { ColorFormType } from '@/types/form/color.form';
import { useColor } from '@/composables/useColor';

const props = defineProps<{
    closeModal: () => void
    color?: ColorType
}>()

const colorFormDefaultValue = (): ColorFormType => ({
    name: "",
    code: ""
})

const { create, update } = useColor()

let colorForm = reactive<ColorFormType>(colorFormDefaultValue());
const isSubmitting = ref(false)

const submitForm = async () => {
    isSubmitting.value = true

    let result
    if (props.color) result = await update(props.color.id, colorForm)
    else result = await create(colorForm)

    isSubmitting.value = false

    // close form if success
    if (result) {
        props.closeModal()
    }
}

// Watch for changes in props.size
watch(() => props.color, (newSize) => {
    if (newSize) {
        colorForm.name = newSize.name;  // Update colorForm.name if size exists
    } else {
        colorForm.name = "";  // Reset name if no size
    }
}, { immediate: true })  // Run immediately on component mount
</script>