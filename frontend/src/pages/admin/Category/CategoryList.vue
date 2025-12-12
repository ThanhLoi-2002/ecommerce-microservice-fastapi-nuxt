// CategoryList.vue
<template>
    <div class="min-vh-100" style="background-color: #f8f9fa;">
        <!-- Header -->
        <Header label="Categories" />

        <div class="container-fluid mt-4">
            <div class="card shadow-sm">
                <div class="card-header bg-white">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Danh sách Thể loại Sản phẩm</h5>
                        <button class="btn btn-primary" @click="showModal('create')">
                            ➕ Thêm danh mục
                        </button>
                    </div>
                </div>
                <div class="card-body">
                    <!-- Tìm kiếm và bộ lọc -->
                    <div class="row mb-4">
                        <div class="col-md-4">
                            <input type="text" class="form-control" placeholder="🔍 Tìm kiếm danh mục..."
                                v-model="filters.search" @input="debouncedSearch" />
                        </div>
                        <div class="col-md-3">
                            <select class="form-control" v-model="filters.status" @change="loadCategories">
                                <option :value="null">Tất cả trạng thái</option>
                                <option :value="true">Đang hoạt động</option>
                                <option :value="false">Không hoạt động</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <select class="form-control" v-model="filters.parentOnly" @change="loadCategories">
                                <option :value="false">Tất cả</option>
                                <option :value="true">Danh mục cha</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <select class="form-control" v-model="sortBy">
                                <option value="">Sắp xếp </option>
                                <option value="name">Sắp xếp theo tên</option>
                                <option value="count">Số sản phẩm</option>
                            </select>
                        </div>

                        <div class="col-md-1">
                            <button class="btn btn-outline-secondary btn-block" @click="resetFilters">
                                🔄
                            </button>
                        </div>
                    </div>

                    <!-- Thống kê tổng quan -->
                    <div class="row mb-4">
                        <div class="col-md-3">
                            <div class="alert alert-primary mb-0">
                                <h4 class="mb-0">{{ pagination.total }}</h4>
                                <small>Tổng danh mục</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="alert alert-success mb-0">
                                <h4 class="mb-0">{{ activeCount }}</h4>
                                <small>Đang hoạt động</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="alert alert-info mb-0">
                                <h4 class="mb-0">{{ parentCount }}</h4>
                                <small>Danh mục cha</small>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="alert alert-warning mb-0">
                                <h4 class="mb-0">{{ childrenCount }}</h4>
                                <small>Danh mục con</small>
                            </div>
                        </div>
                    </div>

                    <!-- Loading -->
                    <div v-if="loading" class="text-center py-5">
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
                                                        :alt="category.name" class="category-img me-2" />
                                                    {{ category.name }}
                                                </h5>
                                            </div>
                                            <span
                                                :class="category.status === true ? 'badge badge-success' : 'badge badge-secondary'">
                                                {{ category.status === true ? 'Hoạt động' : 'Tắt' }}
                                            </span>
                                        </div>

                                        <p class="card-text text-muted mb-3 text-truncate" style="min-height: 25px;">
                                            {{ category.description }}
                                        </p>

                                        <span v-if="category.pid" class="badge badge-info">
                                            {{ getParentName(category.pid) }}
                                        </span>
                                        <span v-else class="badge badge-secondary">Danh mục gốc</span>

                                        <div class="d-flex justify-content-between align-items-center">
                                            <small class="text-muted">
                                                Cập nhật: {{ formatDate(category.updated_at) }}
                                            </small>
                                            <div>
                                                <button class="btn btn-sm btn-outline-info mr-1" title="Xem sản phẩm"
                                                    @click="viewProducts(category.id)">
                                                    👁️
                                                </button>
                                                <button class="btn btn-sm btn-outline-warning mr-1" title="Chỉnh sửa"
                                                    @click="editCategory(category.id)">
                                                    ✏️
                                                </button>
                                                <button class="btn btn-sm btn-outline-danger" title="Xóa"
                                                    @click="deleteCategory(category.id)">
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
                                        <th>Mô tả</th>
                                        <th>Danh mục cha</th>
                                        <th width="120">Trạng thái</th>
                                        <th width="150">Thao tác</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="category in categories" :key="category.id">
                                        <td>{{ category.id }}</td>
                                        <td style="text-align: center;"><img v-if="category.img" :src="category.img.url"
                                                :alt="category.name" class="category-img me-2" /></td>
                                        <td><strong>{{ category.name }}</strong></td>
                                        <td><small class="text-muted">{{ category.description }}</small></td>
                                        <td>
                                            <span v-if="category.pid" class="badge badge-info">
                                                {{ getParentName(category.pid) }}
                                            </span>
                                            <span v-else class="badge badge-secondary">Danh mục gốc</span>
                                        </td>
                                        <td>
                                            <span
                                                :class="category.status === true ? 'badge badge-success' : 'badge badge-secondary'">
                                                {{ category.status === true ? 'Hoạt động' : 'Tắt' }}
                                            </span>
                                        </td>
                                        <td>
                                            <button class="btn btn-sm btn-info mr-1" title="Xem sản phẩm"
                                                @click="viewProducts(category.id)">👁️</button>
                                            <button class="btn btn-sm btn-warning mr-1" title="Chỉnh sửa"
                                                @click="editCategory(category.id)">✏️</button>
                                            <button class="btn btn-sm btn-danger" title="Xóa"
                                                @click="deleteCategory(category.id)">🗑️</button>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Phân trang -->
                    <div class="d-flex justify-content-between align-items-center mt-3">
                        <div class="d-flex align-items-center">
                            <span class="text-muted mr-2">
                                Hiển thị {{ (pagination.page - 1) * perPage + 1 }} -
                                {{ Math.min(pagination.page * perPage, pagination.total) }} /
                                <strong>{{ pagination.total }}</strong> danh mục
                            </span>
                            <div class="">
                                <select class="form-control" v-model="perPage" @change="loadCategories">
                                    <option :value="10">10</option>
                                    <option :value="20">20</option>
                                    <option :value="50">50</option>
                                </select>
                            </div>
                        </div>
                        <nav>
                            <ul class="pagination mb-0">
                                <li class="page-item" :class="{ disabled: pagination.page === 1 }">
                                    <a class="page-link" href="#" @click.prevent="changePage(pagination.page - 1)">‹</a>
                                </li>
                                <li v-for="page in displayPages" :key="page" class="page-item"
                                    :class="{ active: page === pagination.page }">
                                    <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                                </li>
                                <li class="page-item" :class="{ disabled: pagination.page === pagination.totalPages }">
                                    <a class="page-link" href="#" @click.prevent="changePage(pagination.page + 1)">›</a>
                                </li>
                            </ul>
                        </nav>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal Create/Edit -->
        <div v-if="modalVisible" class="modal-backdrop" @click="closeModal">
            <div class="modal-dialog" @click.stop>
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            {{ modalMode === 'create' ? '➕ Thêm danh mục mới' : '✏️ Chỉnh sửa danh mục' }}
                        </h5>
                        <button type="button" class="close" @click="closeModal">
                            <span>&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="submitForm">
                            <div class="form-group">
                                <label>Tên danh mục <span class="text-danger">*</span></label>
                                <input type="text" class="form-control" v-model="formData.name" required
                                    placeholder="Nhập tên danh mục..." />
                            </div>

                            <div class="form-group">
                                <label>Hình ảnh (URL)</label>
                                <input type="url" class="form-control" v-model="formData.img"
                                    placeholder="https://example.com/image.jpg" />
                                <img v-if="formData.img" :src="formData.img.url" alt="Preview"
                                    class="mt-2 img-thumbnail" style="max-height: 100px;" />
                            </div>

                            <div class="form-group">
                                <label>Danh mục cha</label>
                                <select class="form-control" v-model="formData.pid">
                                    <option :value="null">-- Không có (Danh mục gốc) --</option>
                                    <option v-for="cat in parentCategories" :key="cat.id" :value="cat.id"
                                        :disabled="modalMode === 'edit' && cat.id === formData.id">
                                        {{ cat.name }}
                                    </option>
                                </select>
                            </div>

                            <div class="form-group">
                                <div class="custom-control custom-switch">
                                    <input type="checkbox" class="custom-control-input" id="statusSwitch"
                                        v-model="formData.status" />
                                    <label class="custom-control-label" for="statusSwitch">
                                        Trạng thái: {{ formData.status ? '✓ Hoạt động' : '✗ Không hoạt động' }}
                                    </label>
                                </div>
                            </div>

                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" @click="closeModal">
                                    Hủy
                                </button>
                                <button type="submit" class="btn btn-primary" :disabled="submitting">
                                    {{ submitting ? 'Đang xử lý...' : (modalMode === 'create' ? 'Thêm mới' : 'Cập nhật')
                                    }}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import axios from "../../../api/axios";
import Header from '@/components/admin/Header.vue';
import type { ImageType } from '@/types/common';
import LoadingSpinner from '@/components/common/loading/LoadingSpinner.vue';

interface CategoryType {
    id: number;
    name: string;
    slug: string;
    description: string | null
    img: ImageType;
    pid: number | null;
    status: boolean;
    children_count: number;
    created_at: string;
    updated_at: string;
}

interface Filters {
    search: string;
    status: boolean | null;
    parentOnly: boolean;
}

// API Base URL
const API_URL = '/categories';

// State
const categories = ref<CategoryType[]>([]);
const allCategories = ref<CategoryType[]>([]);
const loading = ref(false);
const submitting = ref(false);
const modalVisible = ref(false);
const modalMode = ref<'create' | 'edit'>('create');
const sortBy = ref<string>('');
const viewMode = ref<string>('cards');

const filters = ref<Filters>({
    search: '',
    status: null,
    parentOnly: false
});

const pagination = ref({
    page: 1,
    perPage: 10,
    total: 0,
    totalPages: 0
});

const perPage = ref(10);

const formData = ref({
    id: null as number | null,
    name: '',
    img: null as ImageType | null,
    pid: null as number | null,
    status: true
});

// Computed
const parentCategories = computed(() => {
    return allCategories.value.filter(cat => cat.pid === null);
});

const activeCount = computed(() => {
    return categories.value.filter(cat => cat.status).length;
});

const parentCount = computed(() => {
    return categories.value.filter(cat => cat.pid === null).length;
});

const childrenCount = computed(() => {
    return categories.value.filter(cat => cat.pid !== null).length;
});

const toggleView = (): void => {
    viewMode.value = viewMode.value === 'cards' ? 'table' : 'cards';
};

const displayPages = computed(() => {
    const pages: number[] = [];
    const total = pagination.value.totalPages;
    const current = pagination.value.page;

    if (total <= 7) {
        for (let i = 1; i <= total; i++) {
            pages.push(i);
        }
    } else {
        pages.push(1);
        if (current > 3) pages.push(-1); // ellipsis

        for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
            pages.push(i);
        }

        if (current < total - 2) pages.push(-1);
        pages.push(total);
    }

    return pages;
});

// Methods
const loadCategories = async () => {
    loading.value = true;
    try {
        const params: any = {
            page: pagination.value.page,
            per_page: perPage.value
        };

        if (filters.value.search) params.search = filters.value.search;
        if (filters.value.status !== null) params.status = filters.value.status;
        if (filters.value.parentOnly) params.parent_only = true;

        const { data } = await axios.get(API_URL, { params });

        categories.value = data.items;
        pagination.value = {
            page: data.page,
            perPage: data.per_page,
            total: data.total,
            totalPages: data.total_pages
        };
    } catch (error) {
        console.error('Error loading categories:', error);
        alert('Lỗi khi tải danh mục!');
    } finally {
        loading.value = false;
    }
};

const loadAllCategories = async () => {
    try {
        const { data } = await axios.get(API_URL, {
            params: { page: 1, per_page: 1000 }
        });
        allCategories.value = data.items;
    } catch (error) {
        console.error('Error loading all categories:', error);
    }
};

let searchTimeout: any = null;
const debouncedSearch = () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        pagination.value.page = 1;
        loadCategories();
    }, 500);
};

const changePage = (page: number) => {
    if (page >= 1 && page <= pagination.value.totalPages) {
        pagination.value.page = page;
        loadCategories();
    }
};

const resetFilters = () => {
    filters.value = {
        search: '',
        status: null,
        parentOnly: false
    };
    pagination.value.page = 1;
    loadCategories();
};

const showModal = (mode: 'create' | 'edit', category?: CategoryType) => {
    modalMode.value = mode;

    if (mode === 'edit' && category) {
        formData.value = {
            id: category.id,
            name: category.name,
            img: { ...category.img },
            pid: category.pid,
            status: category.status
        };
    } else {
        formData.value = {
            id: null,
            name: '',
            img: null,
            pid: null,
            status: true
        };
    }

    modalVisible.value = true;
};

const closeModal = () => {
    modalVisible.value = false;
};

const submitForm = async () => {
    submitting.value = true;
    try {
        const payload = {
            name: formData.value.name,
            img: formData.value.img || null,
            pid: formData.value.pid || null,
            status: formData.value.status
        };

        if (modalMode.value === 'create') {
            await axios.post(API_URL, payload);
            alert('Thêm danh mục thành công!');
        } else {
            await axios.put(`${API_URL}/${formData.value.id}`, payload);
            alert('Cập nhật danh mục thành công!');
        }

        closeModal();
        loadCategories();
        loadAllCategories();
    } catch (error: any) {
        console.error('Error submitting form:', error);
        alert(error.response?.data?.detail || 'Có lỗi xảy ra!');
    } finally {
        submitting.value = false;
    }
};

const confirmDelete = async (id: number) => {
    if (!confirm('Bạn có chắc muốn xóa danh mục này?')) return;

    try {
        await axios.delete(`${API_URL}/${id}`);
        alert('Xóa danh mục thành công!');
        loadCategories();
        loadAllCategories();
    } catch (error: any) {
        console.error('Error deleting category:', error);
        alert(error.response?.data?.detail || 'Có lỗi xảy ra!');
    }
};

const viewCategory = (category: CategoryType) => {
    alert(`Xem chi tiết danh mục:\nID: ${category.id}\nTên: ${category.name}\nSlug: ${category.slug}`);
};

const getParentName = (pid: number): string => {
    const parent = allCategories.value.find(cat => cat.id === pid);
    return parent?.name || 'N/A';
};

const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('vi-VN') + ' ' + date.toLocaleTimeString('vi-VN');
};

// Methods
const getProgressWidth = (count: number): number => {
    const max = Math.max(...categories.value.map(c => c.children_count));
    return (count / max) * 100;
};

const viewProducts = (id: number): void => {
    console.log('Xem sản phẩm của danh mục:', id);
};

const editCategory = (id: number): void => {
    console.log('Chỉnh sửa danh mục ID:', id);
};

const deleteCategory = (id: number): void => {
    if (confirm('Bạn có chắc muốn xóa danh mục này?')) {
        const index = categories.value.findIndex(c => c.id === id);
        if (index !== -1) {
            categories.value.splice(index, 1);
        }
    }
};

// Lifecycle
onMounted(() => {
    loadCategories();
    loadAllCategories();
});
</script>

<style scoped>
.table td {
    vertical-align: middle;
}

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

.modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1050;
}

.modal-dialog {
    background: white;
    border-radius: 8px;
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    padding: 1rem 1.5rem;
    border-bottom: 1px solid #dee2e6;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-body {
    padding: 1.5rem;
}

.modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #dee2e6;
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
}

.close {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}
</style>