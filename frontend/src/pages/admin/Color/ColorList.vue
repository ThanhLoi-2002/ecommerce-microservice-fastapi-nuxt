<template>
    <div class="min-vh-100" style="background-color: #f8f9fa;">
        <!-- Header -->
        <Header label="Colors" />

        <div class="container-fluid mt-4">
            <div class="card shadow-sm">
                <Action label="Thêm Color" :onClick="() => showModal()" />
                <div class="card-body">
                    <!-- Loading -->
                    <div v-if="isLoading" class="text-center py-5">
                        <div class="text-center">
                            <LoadingSpinner size="40px" />
                            <p>Loading....</p>
                        </div>
                    </div>
                    <!-- Bảng danh mục -->
                    <div v-else class="table-responsive">
                        <!-- Danh sách dạng Bảng -->
                        <div class="table-responsive">
                            <table class="table table-hover table-bordered">
                                <thead class="thead-light">
                                    <tr class="text-center">
                                        <th width="50">#</th>
                                        <th>Tên</th>
                                        <th width="150">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(item, index) in colors" :key="item.id" class="text-center">
                                        <td>{{ index + 1 }}</td>
                                        <td>
                                            <div class="d-flex justify-content-between align-items-center"><span>{{
                                                item.name }}</span>
                                                <span
                                                    :style="`width: 20px; height: 20px; border-radius: 50%; border: 1px solid black; background: ${item.code}`"></span>
                                            </div>
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-warning mr-1" title="Chỉnh sửa"
                                                @click="edit(item)">✏️</button>
                                            <button class="btn btn-sm btn-danger" title="Xóa"
                                                @click="openConfirmModal(item)">🗑️</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal Create/Edit -->
        <Modal :open="modalVisible" :title="color ? '✏️ Chỉnh sửa' : '➕ Thêm mới'" :closeModal="closeModal">
            <ColorForm :closeModal="closeModal" :color="color" />
        </Modal>

        <!-- Delete Confirm Modal -->
        <ConfirmModal :onConfirm="() => remove()" :isOpen="isOpenConfirmModal" :onClose="() => closeConfirmModal()"
            :text="colorName" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Header from '@/components/admin/Header.vue';
import LoadingSpinner from '@/components/common/loading/LoadingSpinner.vue';
import Action from '@/components/admin/Action.vue';
import Modal from '@/components/common/modal/Modal.vue';
import ConfirmModal from '@/components/common/modal/ConfirmModal.vue';
import type { ColorType } from '@/types/entities';
import ColorForm from './components/ColorForm.vue';
import { storeToRefs } from 'pinia';
import { useColor } from '@/composables/useColor';
import { useColorStore } from '@/stores/color.store';

// State
const { getColors, deleteColor } = useColor()
const colorStore = useColorStore()
const { colors, isLoading } = storeToRefs(colorStore)

const modalVisible = ref(false);
const isOpenConfirmModal = ref(false);
const color = ref<ColorType | undefined>(undefined)
const colorName = ref<string>('')

const showModal = (selectedSize?: ColorType) => {
    color.value = selectedSize;
    modalVisible.value = true;
};

const closeModal = () => {
    modalVisible.value = false;
};

const openConfirmModal = (selectedSize: ColorType) => {
    isOpenConfirmModal.value = true
    color.value = selectedSize
    colorName.value = selectedSize.name
}

const closeConfirmModal = () => {
    isOpenConfirmModal.value = false
    color.value = undefined
    colorName.value = ''
}

const edit = (color: ColorType): void => {
    showModal(color)
};

const remove = async () => {
    await deleteColor(color.value!.id!)
};

// Lifecycle
onMounted(async () => {
    await getColors()
});
</script>