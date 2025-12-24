// CategoryList.vue
<template>
    <div class="min-vh-100" style="background-color: #f8f9fa;">
        <!-- Header -->
        <Header label="Categories" />

        <div class="container-fluid mt-4">
            <div class="card shadow-sm">
                <Action label="Thêm danh mục" :onClick="() => showModal()" />
                <div class="card-body">
                    <!-- Tìm kiếm và bộ lọc -->
                    <Filters :filters="filters" :setFilters="setFilters" :resetFilters="resetFilters" />

                    <!-- Thống kê tổng quan -->
                    <Summary :total="total" :parentCount="metadata.parentCount" :childrenCount="metadata.childrenCount"
                        :activeCount="metadata.activeCount" />

                    <!-- Loading -->
                    <div v-if="isLoading" class="text-center py-5">
                        <div class="text-center">
                            <LoadingSpinner size="40px" />
                            <p>Loading....</p>
                        </div>
                    </div>
                    <!-- Bảng danh mục -->
                    <div v-else class="table-responsive">
                        <!-- Nút chuyển đổi view -->
                        <div class="d-flex justify-content-between align-items-center mb-3">
                            <h6 class="mb-0">{{ viewMode === 'cards' ? 'Chế độ xem thẻ' : 'Chế độ xem bảng' }}</h6>
                            <button class="btn btn-sm btn-outline-primary" @click="toggleView">
                                {{ viewMode === 'cards' ? '📋 Xem dạng bảng' : '📇 Xem dạng thẻ' }}
                            </button>
                        </div>

                        <!-- Danh sách dạng Card -->
                        <div v-if="viewMode === 'cards'" class="row">
                            <div v-for="category in categories" :key="category.id" class="col-md-6 col-lg-4 mb-4">
                                <div class="card h-100 border shadow-sm category-card">
                                    <div class="card-body">
                                        <div class="d-flex justify-content-between align-items-start mb-3">
                                            <div>
                                                <h5 class="card-title mb-1">
                                                    <img v-if="category.img" :src="category.img.url"
                                                        :alt="category.name" class="category-img" />
                                                </h5>
                                            </div>

                                            <div class="d-flex flex-column align-items-end gap-1">
                                                <span v-if="category.pid" class="badge badge-info">
                                                    {{ category.parent?.name }} ({{
                                                    categoryGender(category.parent?.gender) }})
                                                </span>
                                                <span v-else class="badge badge-secondary">Danh mục gốc</span>
                                                <Switch v-model="category.status"
                                                    :onClick="() => changeStatus(category.id, !category.status)" />
                                            </div>

                                        </div>
                                        <div>{{ category.name }}
                                            ({{ categoryGender(category.gender) }})</div>

                                        <div class="d-flex justify-content-between align-items-center">
                                            <small class="text-muted">
                                                Cập nhật: {{ formatDate(category.updated_at) }}
                                            </small>
                                            <div class="d-flex gap-1 flex-wrap justify-content-end">
                                                <button class="btn btn-sm btn-outline-info" title="Xem sản phẩm"
                                                    @click="viewProducts(category.id)"
                                                    v-if="category.children_count > 0">
                                                    👁️
                                                </button>
                                                <button class="btn btn-sm btn-outline-warning" title="Chỉnh sửa"
                                                    @click="editCategory(category.id)">
                                                    ✏️
                                                </button>
                                                <button class="btn btn-sm btn-outline-danger" title="Xóa"
                                                    @click="openConfirmModal(category.id, category.name)">
                                                    🗑️
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Danh sách dạng Bảng -->
                        <div v-else class="table-responsive">
                            <table class="table table-hover table-bordered">
                                <thead class="thead-light">
                                    <tr>
                                        <th width="50">#</th>
                                        <th width="80">Hình ảnh</th>
                                        <th>Tên danh mục</th>
                                        <!-- <th>Mô tả</th> -->
                                        <th>Danh mục cha</th>
                                        <th width="120">Trạng thái</th>
                                        <th width="150">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(category, index) in categories" :key="category.id">
                                        <td>{{ (filters.page - 1) * filters.limit + index + 1 }}</td>
                                        <td style="text-align: center;"><img v-if="category.img" :src="category.img.url"
                                                :alt="category.name" class="category-img me-2" /></td>
                                        <td><strong>{{ category.name }}</strong> ({{ categoryGender(category.gender) }})
                                        </td>
                                        <td>
                                            <span v-if="category.pid" class="badge badge-info">
                                                {{ category.parent?.name }} ({{ categoryGender(category.parent?.gender)
                                                }})
                                            </span>
                                            <span v-else class="badge badge-secondary">Danh mục gốc</span>
                                        </td>
                                        <td>
                                            <Switch v-model="category.status"
                                                :onClick="() => changeStatus(category.id, !category.status)" />
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-info mr-1" title="Xem sản phẩm"
                                                @click="viewProducts(category.id)">👁️</button>
                                            <button class="btn btn-sm btn-warning mr-1" title="Chỉnh sửa"
                                                @click="editCategory(category.id)">✏️</button>
                                            <button class="btn btn-sm btn-danger" title="Xóa"
                                                @click="openConfirmModal(category.id, category.name)">🗑️</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Phân trang -->
                    <Pagination :limit="filters.limit" :total="total" :page="filters.page" :total_pages="total_pages"
                        :changeLimit="changeLimit" :changePage="changePage" />
                </div>
            </div>
        </div>

        <!-- Modal Create/Edit -->
        <Modal :open="modalVisible" :title="id ? '✏️ Chỉnh sửa danh mục' : '➕ Thêm danh mục mới'"
            :closeModal="closeModal">
            <CategoryForm :closeModal="closeModal" :filters="filters" :resetFilters="resetFilters" :id="id" />
        </Modal>

        <!-- Delete Confirm Modal -->
        <ConfirmModal :onConfirm="() => removeCategory()" :isOpen="isOpenConfirmModal"
            :onClose="() => closeConfirmModal()" :text="categoryName" />

        <!-- Modal Danh mục con -->
        <Modal :open="childModalVisible" title="📂 Danh mục con" :closeModal="() => childModalVisible = false">
            <CategoryChildren :category="selectedCategory" />
        </Modal>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Header from '@/components/admin/Header.vue';
import type { CategoryFilter } from '@/types/common';
import LoadingSpinner from '@/components/common/loading/LoadingSpinner.vue';
import Action from '@/components/admin/Action.vue';
import Filters from './components/Filters.vue';
import { useCategoryStore } from '@/stores/category.store';
import { storeToRefs } from 'pinia';
import { useCategory } from '@/composables/useCategory';
import { categoryFilterDefault } from '@/utils/constants';
import Pagination from '@/components/admin/Pagination.vue';
import Summary from './components/Summary.vue';
import { formatDate } from '@/utils/date'
import Modal from '@/components/common/modal/Modal.vue';
import CategoryForm from './components/CategoryForm.vue';
import ConfirmModal from '@/components/common/modal/ConfirmModal.vue';
import Switch from '@/components/common/switch/Switch.vue';
import type { CategoryType } from '@/types/entities';
import CategoryChildren from './components/CategoryChildren.vue';
import { categoryGender } from '@/utils/translateFromEnum';

// State
const { getCategories, deleteCategory, changeStatus } = useCategory()
const categoryStore = useCategoryStore()
const { isLoading, categories, total_pages, total, metadata } = storeToRefs(categoryStore)

const filters = ref<CategoryFilter>(categoryFilterDefault);
const modalVisible = ref(false);
const isOpenConfirmModal = ref(false);
const viewMode = ref<string>('cards')
const id = ref<number | undefined>(undefined)
const categoryName = ref<string>('')
const childModalVisible = ref(false)
const selectedCategory = ref<CategoryType>()

const toggleView: any = (): void => {
    viewMode.value = viewMode.value === 'cards' ? 'table' : 'cards';
};

// Methods
const changePage = (page: number) => {
    filters.value = { ...filters.value, page }
    getCategories(filters.value);
};

const changeLimit = (e: any) => {
    filters.value = { ...filters.value, limit: e.target?.value, page: 1 }
    getCategories(filters.value);
};

const setFilters = <K extends keyof CategoryFilter>(
    key: K,
    value: CategoryFilter[K]
) => {
    filters.value = {
        ...filters.value,
        [key]: value,
    }

    getCategories(filters.value)
}

const resetFilters = () => {
    filters.value = categoryFilterDefault;
    getCategories(filters.value)
};

const showModal = (selectedId?: number) => {
    id.value = selectedId;
    modalVisible.value = true;
};

const closeModal = () => {
    modalVisible.value = false;
};

const openConfirmModal = (selectedId: number, name: string) => {
    isOpenConfirmModal.value = true
    id.value = selectedId
    categoryName.value = name
}

const closeConfirmModal = () => {
    isOpenConfirmModal.value = false
    id.value = undefined
    categoryName.value = ''
}

// Methods
const viewProducts = (id: number): void => {
    const category = categories.value.find(c => c.id === id)
    if (!category || !category.children || category.children.length === 0) return

    selectedCategory.value = category
    childModalVisible.value = true
};

const editCategory = (id: number): void => {
    showModal(id)
};

const removeCategory = async () => {
    await deleteCategory(id.value!)
    getCategories(filters.value)
};

// Lifecycle
onMounted(() => {
    getCategories(filters.value);
});
</script>

<style>
.category-img {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: 8px;
}

.category-img-placeholder {
    width: 60px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #f0f0f0;
    border-radius: 8px;
    font-size: 1.5rem;
}
</style>