<template>
    <div class="min-vh-100" style="background-color: #f8f9fa;">
        <!-- Header -->
        <Header label="Sizes" />

        <div class="container-fluid mt-4">
            <div class="card shadow-sm">
                <Action label="Thêm Size" :onClick="() => showModal()" />
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
                                    <tr v-for="(item, index) in sizes" :key="item.id" class="text-center">
                                        <td>{{ index + 1 }}</td>
                                        <td>{{ item.name }}</td>
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
        <Modal :open="modalVisible" :title="size ? '✏️ Chỉnh sửa' : '➕ Thêm mới'" :closeModal="closeModal">
            <SizeForm :closeModal="closeModal" :size="size" />
        </Modal>

        <!-- Delete Confirm Modal -->
        <ConfirmModal :onConfirm="() => remove()" :isOpen="isOpenConfirmModal" :onClose="() => closeConfirmModal()"
            :text="sizeName" />
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Header from '@/components/admin/Header.vue';
import LoadingSpinner from '@/components/common/loading/LoadingSpinner.vue';
import Action from '@/components/admin/Action.vue';
import Modal from '@/components/common/modal/Modal.vue';
import ConfirmModal from '@/components/common/modal/ConfirmModal.vue';
import type { SizeType } from '@/types/entities';
import { useSize } from '@/composables/useSize';
import SizeForm from './components/SizeForm.vue';
import { useSizeStore } from '@/stores/size.store';
import { storeToRefs } from 'pinia';

// State
const { getSizes, deleteSize } = useSize()
const sizeStore = useSizeStore()
const {sizes, isLoading} = storeToRefs(sizeStore)

const modalVisible = ref(false);
const isOpenConfirmModal = ref(false);
const size = ref<SizeType | undefined>(undefined)
const sizeName = ref<string>('')

const showModal = (selectedSize?: SizeType) => {
    size.value = selectedSize;
    modalVisible.value = true;
};

const closeModal = () => {
    modalVisible.value = false;
};

const openConfirmModal = (selectedSize: SizeType) => {
    isOpenConfirmModal.value = true
    size.value = selectedSize
    sizeName.value = selectedSize.name
}

const closeConfirmModal = () => {
    isOpenConfirmModal.value = false
    size.value = undefined
    sizeName.value = ''
}

const edit = (size: SizeType): void => {
    showModal(size)
};

const remove = async () => {
    await deleteSize(size.value!.id!)
};

// Lifecycle
onMounted(async () => {
    await getSizes()
});
</script>