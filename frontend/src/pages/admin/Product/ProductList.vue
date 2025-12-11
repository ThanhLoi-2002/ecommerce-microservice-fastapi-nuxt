// ProductList.vue
<template>
    <div class="min-vh-100" style="background-color: #f8f9fa;">
        <!-- Header -->
        <Header label="Products" />

        <div class="container-fluid mt-4">
            <div class="row">

                <!-- Main Content -->
                <div class="col-md-12">
                    <div class="card shadow-sm">
                        <div class="card-header bg-white">
                            <div class="d-flex justify-content-between align-items-center">
                                <h5 class="mb-0">Danh sách Sản phẩm Thời trang</h5>
                                <button class="btn btn-primary" @click="showAddModal">
                                    ➕ Thêm sản phẩm
                                </button>
                            </div>
                        </div>
                        <div class="card-body">
                            <!-- Bộ lọc -->
                            <div class="row mb-4">
                                <div class="col-md-4">
                                    <input type="text" class="form-control" placeholder="🔍 Tìm kiếm sản phẩm..."
                                        v-model="searchTerm" />
                                </div>
                                <div class="col-md-3">
                                    <select class="form-control" v-model="filterCategory">
                                        <option value="all">Tất cả danh mục</option>
                                        <option v-for="cat in categories" :key="cat" :value="cat">
                                            {{ cat }}
                                        </option>
                                    </select>
                                </div>
                                <div class="col-md-3">
                                    <select class="form-control" v-model="filterStatus">
                                        <option value="all">Tất cả trạng thái</option>
                                        <option value="active">Đang bán</option>
                                        <option value="inactive">Ngừng bán</option>
                                        <option value="out_of_stock">Hết hàng</option>
                                    </select>
                                </div>
                                <div class="col-md-2">
                                    <button class="btn btn-outline-secondary btn-block" @click="resetFilters">
                                        🔄 Làm mới
                                    </button>
                                </div>
                            </div>

                            <!-- Thống kê nhanh -->
                            <div class="row mb-3">
                                <div class="col-md-3">
                                    <div class="alert alert-info mb-0">
                                        <strong>{{ filteredProducts.length }}</strong> sản phẩm
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="alert alert-success mb-0">
                                        <strong>{{ activeProducts }}</strong> đang bán
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="alert alert-warning mb-0">
                                        <strong>{{ totalStock }}</strong> tồn kho
                                    </div>
                                </div>
                                <div class="col-md-3">
                                    <div class="alert alert-danger mb-0">
                                        <strong>{{ outOfStockProducts }}</strong> hết hàng
                                    </div>
                                </div>
                            </div>

                            <!-- Bảng sản phẩm -->
                            <div class="table-responsive">
                                <table class="table table-hover table-bordered">
                                    <thead class="thead-light">
                                        <tr>
                                            <th width="50">#</th>
                                            <th width="100">Hình ảnh</th>
                                            <th>Tên sản phẩm</th>
                                            <th>Danh mục</th>
                                            <th>Giá bán</th>
                                            <th>Tồn kho</th>
                                            <th>Trạng thái</th>
                                            <th width="180">Thao tác</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="product in paginatedProducts" :key="product.id">
                                            <td>{{ product.id }}</td>
                                            <td>
                                                <div style="font-size: 2.5rem; text-align: center;">
                                                    {{ product.image }}
                                                </div>
                                            </td>
                                            <td><strong>{{ product.name }}</strong></td>
                                            <td>
                                                <span class="badge badge-secondary">{{ product.category }}</span>
                                            </td>
                                            <td class="text-primary">
                                                <strong>{{ formatPrice(product.price) }}</strong>
                                            </td>
                                            <td>
                                                <span :class="product.stock === 0 ? 'text-danger' : 'text-success'">
                                                    <strong>{{ product.stock }}</strong>
                                                </span>
                                            </td>
                                            <td>
                                                <span :class="getStatusClass(product.status)">
                                                    {{ getStatusLabel(product.status) }}
                                                </span>
                                            </td>
                                            <td>
                                                <button class="btn btn-sm btn-info mr-1" title="Xem chi tiết"
                                                    @click="viewProduct(product.id)">
                                                    👁️
                                                </button>
                                                <button class="btn btn-sm btn-warning mr-1" title="Chỉnh sửa"
                                                    @click="editProduct(product.id)">
                                                    ✏️
                                                </button>
                                                <button class="btn btn-sm btn-danger" title="Xóa"
                                                    @click="deleteProduct(product.id)">
                                                    🗑️
                                                </button>
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>

                            <!-- Phân trang -->
                            <div class="d-flex justify-content-between align-items-center mt-3">
                                <div>
                                    <span class="text-muted">
                                        Hiển thị <strong>{{ (currentPage - 1) * itemsPerPage + 1 }}</strong> -
                                        <strong>{{ Math.min(currentPage * itemsPerPage, filteredProducts.length)
                                            }}</strong> /
                                        <strong>{{ filteredProducts.length }}</strong> sản phẩm
                                    </span>
                                </div>
                                <nav>
                                    <ul class="pagination mb-0">
                                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                                            <a class="page-link" href="#" @click.prevent="changePage(currentPage - 1)">‹
                                                Trước</a>
                                        </li>
                                        <li v-for="page in totalPages" :key="page" class="page-item"
                                            :class="{ active: page === currentPage }">
                                            <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page
                                                }}</a>
                                        </li>
                                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                                            <a class="page-link" href="#"
                                                @click.prevent="changePage(currentPage + 1)">Sau ›</a>
                                        </li>
                                    </ul>
                                </nav>
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

interface Product {
    id: number;
    name: string;
    category: string;
    price: number;
    stock: number;
    status: 'active' | 'inactive' | 'out_of_stock';
    image: string;
}

// State
const searchTerm = ref<string>('');
const filterCategory = ref<string>('all');
const filterStatus = ref<string>('all');
const currentPage = ref<number>(1);
const itemsPerPage = ref<number>(5);

const products = ref<Product[]>([
    { id: 1, name: 'Áo sơ mi trắng cao cấp', category: 'Áo sơ mi', price: 350000, stock: 45, status: 'active', image: '👔' },
    { id: 2, name: 'Quần jean xanh skinny', category: 'Quần', price: 550000, stock: 30, status: 'active', image: '👖' },
    { id: 3, name: 'Váy dạ hội đỏ sang trọng', category: 'Váy', price: 1200000, stock: 15, status: 'active', image: '👗' },
    { id: 4, name: 'Áo thun polo nam', category: 'Áo thun', price: 250000, stock: 60, status: 'active', image: '👕' },
    { id: 5, name: 'Áo khoác da thời trang', category: 'Áo khoác', price: 1500000, stock: 8, status: 'inactive', image: '🧥' },
    { id: 6, name: 'Quần tây đen công sở', category: 'Quần', price: 450000, stock: 25, status: 'active', image: '👔' },
    { id: 7, name: 'Váy midi hoa cúc', category: 'Váy', price: 680000, stock: 20, status: 'active', image: '👗' },
    { id: 8, name: 'Áo blazer nữ form đẹp', category: 'Áo khoác', price: 890000, stock: 0, status: 'out_of_stock', image: '🧥' },
    { id: 9, name: 'Áo sơ mi họa tiết kẻ sọc', category: 'Áo sơ mi', price: 380000, stock: 35, status: 'active', image: '👔' },
    { id: 10, name: 'Quần short jean nữ', category: 'Quần', price: 320000, stock: 42, status: 'active', image: '👖' },
]);

const categories = ref<string[]>(['Áo sơ mi', 'Quần', 'Váy', 'Áo thun', 'Áo khoác']);

// Computed
const filteredProducts = computed(() => {
    return products.value.filter(product => {
        const matchSearch = product.name.toLowerCase().includes(searchTerm.value.toLowerCase());
        const matchCategory = filterCategory.value === 'all' || product.category === filterCategory.value;
        const matchStatus = filterStatus.value === 'all' || product.status === filterStatus.value;
        return matchSearch && matchCategory && matchStatus;
    });
});

const paginatedProducts = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return filteredProducts.value.slice(start, end);
});

const totalPages = computed(() => {
    return Math.ceil(filteredProducts.value.length / itemsPerPage.value);
});

const activeProducts = computed(() => {
    return filteredProducts.value.filter(p => p.status === 'active').length;
});

const outOfStockProducts = computed(() => {
    return filteredProducts.value.filter(p => p.status === 'out_of_stock').length;
});

const totalStock = computed(() => {
    return filteredProducts.value.reduce((sum, p) => sum + p.stock, 0);
});

// Methods
const formatPrice = (price: number): string => {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(price);
};

const getStatusClass = (status: string): string => {
    const classes: Record<string, string> = {
        active: 'badge badge-success',
        inactive: 'badge badge-secondary',
        out_of_stock: 'badge badge-danger'
    };
    return classes[status] || '';
};

const getStatusLabel = (status: string): string => {
    const labels: Record<string, string> = {
        active: 'Đang bán',
        inactive: 'Ngừng bán',
        out_of_stock: 'Hết hàng'
    };
    return labels[status] || '';
};

const resetFilters = (): void => {
    searchTerm.value = '';
    filterCategory.value = 'all';
    filterStatus.value = 'all';
    currentPage.value = 1;
};

const changePage = (page: number): void => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
    }
};

const showAddModal = (): void => {
    alert('Mở form thêm sản phẩm mới');
};

const viewProduct = (id: number): void => {
    console.log('Xem sản phẩm:', id);
};

const editProduct = (id: number): void => {
    console.log('Sửa sản phẩm:', id);
};

const deleteProduct = (id: number): void => {
    if (confirm('Bạn có chắc muốn xóa sản phẩm này?')) {
        const index = products.value.findIndex(p => p.id === id);
        if (index !== -1) {
            products.value.splice(index, 1);
        }
    }
};
</script>

<style scoped>
.table td {
    vertical-align: middle;
}
</style>