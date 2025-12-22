<template>
    <div class="modal-backdrop" v-if="isOpen" @click="onClose">
        <div class="modal-dialog" @click.stop>
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Xác nhận xóa</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="onClose">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    {{ text }}
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="onClose">Hủy</button>
                    <BaseButton label="Xóa" :isLoading="isLoading" class="btn btn-danger" :onClick="confirmDelete"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import BaseButton from '../button/BaseButton.vue';

const props = defineProps<{
    onConfirm: () => Promise<void>,
    isOpen: boolean
    onClose: () => void
    text: string
}>()

const isLoading = ref(false)

const confirmDelete = async () => {
    isLoading.value = true
    await props.onConfirm()
    isLoading.value = false
    props.onClose();
}
</script>