// CategoryList.vue
<template>
    <div class="min-vh-100" style="background-color: #f8f9fa;">
        <!-- Header -->
        <Header label="Categories" />

        <div class="container-fluid mt-4">
            <div class="row">

                <!-- Main Content -->
                <div class="col-md-12">
                    <div class="card shadow-sm">
                        <div class="card-header bg-white">
                            <div class="d-flex justify-content-between align-items-center">
                                <h5 class="mb-0">Danh sách Thể loại Sản phẩm</h5>
                                <button class="btn btn-primary" @click="showAddModal">
                                    ➕ Thêm danh mục
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <!-- Tìm kiếm và bộ lọc -->
                            <div class="row mb-4">
                                <div class="col-md-5">
                                    <input type="text" class="form-control" placeholder="🔍 Tìm kiếm danh mục..."
                                        v-model="searchTerm" />
                                </div>
                                <div class="col-md-3">
                                    <select class="form-control" v-model="filterStatus">
                                        <option value="all">Tất cả trạng thái</option>
                                        <option value="active">Đang hoạt động</option>
                                        <option value="inactive">Không hoạt động</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <select class="form-control" v-model="sortBy">
                                        <option value="name">Sắp xếp theo tên</option>
                                        <option value="count">Số sản phẩm</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <button class="btn btn-outline-secondary btn-block" @click="resetFilters">
                                        🔄 Làm mới
                                    </button>
                                </div>
                            </div>

                            <!-- Thống kê tổng quan -->
                            <div class="row mb-4">
                                <div class="col-md-4">
                                    <div class="alert alert-primary mb-0">
                                        <h4 class="mb-0">{{ filteredCategories.length }}</h4>
                                        <small>Tổng danh mục</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="alert alert-success mb-0">
                                        <h4 class="mb-0">{{ totalProducts }}</h4>
                                        <small>Tổng sản phẩm</small>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="alert alert-info mb-0">
                                        <h4 class="mb-0">{{ activeCategories }}</h4>
                                        <small>Đang hoạt động</small>
                                    </div>
                                </div>
                            </div>

                            <!-- Nút chuyển đổi view -->
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <h6 class="mb-0">{{ viewMode === 'cards' ? 'Chế độ xem thẻ' : 'Chế độ xem bảng' }}</h6>
                                <button class="btn btn-sm btn-outline-primary" @click="toggleView">
                                    {{ viewMode === 'cards' ? '📋 Xem dạng bảng' : '📇 Xem dạng thẻ' }}
                                </button>
                            </div>

                            <!-- Danh sách dạng Card -->
                            <div v-if="viewMode === 'cards'" class="row">
                                <div v-for="category in sortedCategories" :key="category.id"
                                    class="col-md-6 col-lg-4 mb-4">
                                    <div class="card h-100 border shadow-sm category-card">
                                        <div class="card-body">
                                            <div class="d-flex justify-content-between align-items-start mb-3">
                                                <div>
                                                    <h5 class="card-title mb-1">
                                                        <span style="font-size: 1.5rem; margin-right: 8px;">{{
                                                            category.icon }}</span>
                                                        {{ category.name }}
                                                    </h5>
                                                </div>
                                                <span
                                                    :class="category.status === 'active' ? 'badge badge-success' : 'badge badge-secondary'">
                                                    {{ category.status === 'active' ? 'Hoạt động' : 'Tắt' }}
                                                </span>
                                            </div>

                                            <p class="card-text text-muted mb-3" style="min-height: 45px;">
                                                {{ category.description }}
                                            </p>

                                            <div class="mb-3">
                                                <div class="d-flex justify-content-between mb-1">
                                                    <small class="text-muted">Số sản phẩm:</small>
                                                    <strong class="text-primary">{{ category.count }} sản phẩm</strong>
                                                </div>
                                                <div class="progress" style="height: 5px;">
                                                    <div class="progress-bar bg-primary"
                                                        :style="{ width: getProgressWidth(category.count) + '%' }">
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="d-flex justify-content-between align-items-center">
                                                <small class="text-muted">
                                                    Cập nhật: {{ category.updated }}
                                                </small>
                                                <div>
                                                    <button class="btn btn-sm btn-outline-info mr-1"
                                                        title="Xem sản phẩm" @click="viewProducts(category.id)">
                                                        👁️
                                                    </button>
                                                    <button class="btn btn-sm btn-outline-warning mr-1"
                                                        title="Chỉnh sửa" @click="editCategory(category.id)">
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
                                            <th width="80">Icon</th>
                                            <th>Tên danh mục</th>
                                            <th>Mô tả</th>
                                            <th width="120">Số sản phẩm</th>
                                            <th width="120">Trạng thái</th>
                                            <th width="150">Thao tác</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="category in sortedCategories" :key="category.id">
                                            <td>{{ category.id }}</td>
                                            <td style="font-size: 1.8rem; text-align: center;">{{ category.icon }}</td>
                                            <td><strong>{{ category.name }}</strong></td>
                                            <td><small class="text-muted">{{ category.description }}</small></td>
                                            <td class="text-center">
                                                <span class="badge badge-primary badge-pill">{{ category.count }}</span>
                                            </td>
                                            <td>
                                                <span
                                                    :class="category.status === 'active' ? 'badge badge-success' : 'badge badge-secondary'">
                                                    {{ category.status === 'active' ? 'Hoạt động' : 'Tắt' }}
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
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import Header from '@/components/admin/Header.vue';
import { ref, computed } from 'vue';

interface Category {
    id: number;
    name: string;
    icon: string;
    count: number;
    status: 'active' | 'inactive';
    description: string;
    updated: string;
}

type ViewMode = 'cards' | 'table';
type SortBy = 'name' | 'count';

// State
const searchTerm = ref<string>('');
const filterStatus = ref<string>('all');
const sortBy = ref<SortBy>('name');
const viewMode = ref<ViewMode>('cards');

const categories = ref<Category[]>([
    {
        id: 1,
        name: 'Áo sơ mi',
        icon: '👔',
        count: 45,
        status: 'active',
        description: 'Áo sơ mi nam nữ các loại, công sở và dự tiệc',
        updated: '10/12/2025'
    },
    {
        id: 2,
        name: 'Quần',
        icon: '👖',
        count: 120,
        status: 'active',
        description: 'Quần jean, kaki, tây, short các loại',
        updated: '08/12/2025'
    },
    {
        id: 3,
        name: 'Váy',
        icon: '👗',
        count: 78,
        status: 'active',
        description: 'Váy dạ hội, công sở, dự tiệc, váy midi',
        updated: '09/12/2025'
    },
    {
        id: 4,
        name: 'Áo thun',
        icon: '👕',
        count: 95,
        status: 'active',
        description: 'Áo thun, polo, ba lỗ, áo phông',
        updated: '11/12/2025'
    },
    {
        id: 5,
        name: 'Áo khoác',
        icon: '🧥',
        count: 62,
        status: 'active',
        description: 'Áo khoác, blazer, cardigan, jacket',
        updated: '07/12/2025'
    },
    {
        id: 6,
        name: 'Phụ kiện',
        icon: '👜',
        count: 150,
        status: 'active',
        description: 'Túi xách, mũ, thắt lưng, khăn choàng',
        updated: '10/12/2025'
    },
    {
        id: 7,
        name: 'Giày dép',
        icon: '👞',
        count: 88,
        status: 'active',
        description: 'Giày thể thao, giày cao gót, sandal',
        updated: '09/12/2025'
    },
    {
        id: 8,
        name: 'Đồ ngủ',
        icon: '🛌',
        count: 35,
        status: 'inactive',
        description: 'Đồ ngủ, đồ mặc nhà các loại',
        updated: '05/12/2025'
    },
]);

// Computed
const filteredCategories = computed(() => {
    return categories.value.filter(category => {
        const matchSearch = category.name.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
            category.description.toLowerCase().includes(searchTerm.value.toLowerCase());
        const matchStatus = filterStatus.value === 'all' || category.status === filterStatus.value;
        return matchSearch && matchStatus;
    });
});

const sortedCategories = computed(() => {
    const sorted = [...filteredCategories.value];
    if (sortBy.value === 'name') {
        return sorted.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortBy.value === 'count') {
        return sorted.sort((a, b) => b.count - a.count);
    }
    return sorted;
});

const totalProducts = computed(() => {
    return filteredCategories.value.reduce((sum, cat) => sum + cat.count, 0);
});

const activeCategories = computed(() => {
    return filteredCategories.value.filter(cat => cat.status === 'active').length;
});

// Methods
const getProgressWidth = (count: number): number => {
    const max = Math.max(...categories.value.map(c => c.count));
    return (count / max) * 100;
};

const resetFilters = (): void => {
    searchTerm.value = '';
    filterStatus.value = 'all';
    sortBy.value = 'name';
};

const toggleView = (): void => {
    viewMode.value = viewMode.value === 'cards' ? 'table' : 'cards';
};

const showAddModal = (): void => {
    alert('Mở form thêm danh mục mới');
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
</script>

<style scoped>
.category-card {
    transition: transform 0.2s, box-shadow 0.2s;
}

.category-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
}

.table td {
    vertical-align: middle;
}
</style>