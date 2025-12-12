// OrderList.vue
<template>
    <div class="min-vh-100" style="background-color: #f8f9fa;">
        <!-- Header -->
        <nav class="navbar navbar-dark bg-dark">
            <div class="container-fluid">
                <span class="navbar-brand mb-0 h1">
                    🛒 Fashion Admin - Quản lý Đơn hàng
                </span>
                <div class="text-white">
                    <span class="mr-3">👤 Admin</span>
                </div>
            </div>
        </nav>

        <div class="container-fluid mt-4">
            <div class="card shadow-sm">
                <div class="card-header bg-white">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Danh sách Đơn hàng</h5>
                        <div>
                            <button class="btn btn-success mr-2" @click="exportOrders">
                                📊 Xuất Excel
                            </button>
                            <button class="btn btn-primary" @click="showCreateModal">
                                ➕ Tạo đơn hàng
                            </button>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <!-- Bộ lọc -->
                    <div class="row mb-4">
                        <div class="col-md-3">
                            <input type="text" class="form-control" placeholder="🔍 Tìm mã đơn, khách hàng..."
                                v-model="filters.search" @input="debouncedSearch" />
                        </div>
                        <div class="col-md-2">
                            <select class="form-control" v-model="filters.status" @change="loadOrders">
                                <option value="">Tất cả trạng thái</option>
                                <option value="pending">Chờ xác nhận</option>
                                <option value="confirmed">Đã xác nhận</option>
                                <option value="processing">Đang xử lý</option>
                                <option value="shipping">Đang giao</option>
                                <option value="delivered">Đã giao</option>
                                <option value="cancelled">Đã hủy</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <select class="form-control" v-model="filters.paymentStatus" @change="loadOrders">
                                <option value="">Thanh toán</option>
                                <option value="unpaid">Chưa thanh toán</option>
                                <option value="paid">Đã thanh toán</option>
                                <option value="refunded">Đã hoàn tiền</option>
                            </select>
                        </div>
                        <div class="col-md-2">
                            <input type="date" class="form-control" v-model="filters.fromDate" @change="loadOrders" />
                        </div>
                        <div class="col-md-2">
                            <input type="date" class="form-control" v-model="filters.toDate" @change="loadOrders" />
                        </div>
                        <div class="col-md-1">
                            <button class="btn btn-outline-secondary btn-block" @click="resetFilters">
                                🔄
                            </button>
                        </div>
                    </div>

                    <!-- Thống kê nhanh -->
                    <div class="row mb-4">
                        <div class="col-md-2">
                            <div class="stat-card bg-info">
                                <div class="stat-value">{{ stats.total }}</div>
                                <div class="stat-label">Tổng đơn</div>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <div class="stat-card bg-warning">
                                <div class="stat-value">{{ stats.pending }}</div>
                                <div class="stat-label">Chờ xác nhận</div>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <div class="stat-card bg-primary">
                                <div class="stat-value">{{ stats.processing }}</div>
                                <div class="stat-label">Đang xử lý</div>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <div class="stat-card bg-success">
                                <div class="stat-value">{{ stats.delivered }}</div>
                                <div class="stat-label">Đã giao</div>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <div class="stat-card bg-danger">
                                <div class="stat-value">{{ stats.cancelled }}</div>
                                <div class="stat-label">Đã hủy</div>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <div class="stat-card bg-dark">
                                <div class="stat-value">{{ formatCurrency(stats.revenue) }}</div>
                                <div class="stat-label">Doanh thu</div>
                            </div>
                        </div>
                    </div>

                    <!-- Loading -->
                    <div v-if="loading" class="text-center py-5">
                        <div class="spinner-border text-primary" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>
                    </div>

                    <!-- Bảng đơn hàng -->
                    <div v-else class="table-responsive">
                        <table class="table table-hover table-bordered">
                            <thead class="thead-light">
                                <tr>
                                    <th width="100">Mã đơn</th>
                                    <th width="150">Khách hàng</th>
                                    <th width="120">Ngày đặt</th>
                                    <th width="80">SL</th>
                                    <th width="120">Tổng tiền</th>
                                    <th width="120">Thanh toán</th>
                                    <th width="150">Trạng thái</th>
                                    <th width="200">Thao tác</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="order in orders" :key="order.id">
                                    <td>
                                        <strong class="text-primary">#{{ order.code }}</strong>
                                    </td>
                                    <td>
                                        <div>
                                            <strong>{{ order.customerName }}</strong>
                                            <br>
                                            <small class="text-muted">{{ order.customerPhone }}</small>
                                        </div>
                                    </td>
                                    <td>
                                        <small>{{ formatDateTime(order.createdAt) }}</small>
                                    </td>
                                    <td class="text-center">
                                        <span class="badge badge-secondary badge-pill">{{ order.totalItems }}</span>
                                    </td>
                                    <td>
                                        <strong class="text-success">{{ formatCurrency(order.totalAmount) }}</strong>
                                    </td>
                                    <td>
                                        <span :class="getPaymentBadgeClass(order.paymentStatus)">
                                            {{ getPaymentLabel(order.paymentStatus) }}
                                        </span>
                                        <br>
                                        <small class="text-muted">{{ order.paymentMethod }}</small>
                                    </td>
                                    <td>
                                        <select class="form-control form-control-sm"
                                            :class="getStatusSelectClass(order.status)" v-model="order.status"
                                            @change="updateOrderStatus(order.id, order.status)">
                                            <option value="pending">Chờ xác nhận</option>
                                            <option value="confirmed">Đã xác nhận</option>
                                            <option value="processing">Đang xử lý</option>
                                            <option value="shipping">Đang giao</option>
                                            <option value="delivered">Đã giao</option>
                                            <option value="cancelled">Đã hủy</option>
                                        </select>
                                    </td>
                                    <td>
                                        <button class="btn btn-sm btn-info mr-1" title="Xem chi tiết"
                                            @click="viewOrderDetail(order.id)">
                                            👁️
                                        </button>
                                        <button class="btn btn-sm btn-primary mr-1" title="In hóa đơn"
                                            @click="printInvoice(order.id)">
                                            🖨️
                                        </button>
                                        <button class="btn btn-sm btn-danger" title="Xóa"
                                            @click="confirmDelete(order.id)" :disabled="order.status !== 'cancelled'">
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
                            <select class="form-control form-control-sm d-inline-block w-auto" v-model="perPage"
                                @change="loadOrders">
                                <option :value="10">10</option>
                                <option :value="20">20</option>
                                <option :value="50">50</option>
                                <option :value="100">100</option>
                            </select>
                            <span class="ml-2 text-muted">
                                Hiển thị {{ (pagination.page - 1) * perPage + 1 }} -
                                {{ Math.min(pagination.page * perPage, pagination.total) }} /
                                <strong>{{ pagination.total }}</strong> đơn hàng
                            </span>
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
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

interface Order {
    id: number;
    code: string;
    customerName: string;
    customerPhone: string;
    totalItems: number;
    totalAmount: number;
    paymentStatus: 'unpaid' | 'paid' | 'refunded';
    paymentMethod: string;
    status: 'pending' | 'confirmed' | 'processing' | 'shipping' | 'delivered' | 'cancelled';
    createdAt: string;
}

// State
const loading = ref(false);
const orders = ref<Order[]>([]);
const perPage = ref(20);

const filters = ref({
    search: '',
    status: '',
    paymentStatus: '',
    fromDate: '',
    toDate: ''
});

const pagination = ref({
    page: 1,
    total: 0,
    totalPages: 0
});

const stats = ref({
    total: 156,
    pending: 23,
    processing: 45,
    delivered: 78,
    cancelled: 10,
    revenue: 456780000
});

// // Mock data
const mockOrders: Order[] = [
    { id: 1, code: 'ORD001', customerName: 'Nguyễn Văn A', customerPhone: '0901234567', totalItems: 3, totalAmount: 1250000, paymentStatus: 'paid', paymentMethod: 'COD', status: 'delivered', createdAt: '2025-12-10T10:30:00' },
    { id: 2, code: 'ORD002', customerName: 'Trần Thị B', customerPhone: '0912345678', totalItems: 2, totalAmount: 850000, paymentStatus: 'unpaid', paymentMethod: 'Banking', status: 'pending', createdAt: '2025-12-11T14:20:00' },
    { id: 3, code: 'ORD003', customerName: 'Lê Văn C', customerPhone: '0923456789', totalItems: 5, totalAmount: 2300000, paymentStatus: 'paid', paymentMethod: 'VNPay', status: 'shipping', createdAt: '2025-12-11T16:45:00' },
    { id: 4, code: 'ORD004', customerName: 'Phạm Thị D', customerPhone: '0934567890', totalItems: 1, totalAmount: 450000, paymentStatus: 'paid', paymentMethod: 'MoMo', status: 'processing', createdAt: '2025-12-12T09:15:00' },
    { id: 5, code: 'ORD005', customerName: 'Hoàng Văn E', customerPhone: '0945678901', totalItems: 4, totalAmount: 1800000, paymentStatus: 'unpaid', paymentMethod: 'COD', status: 'confirmed', createdAt: '2025-12-12T11:00:00' },
];

// // Computed
const displayPages = computed(() => {
    const pages: number[] = [];
    const total = pagination.value.totalPages;
    const current = pagination.value.page;

    if (total <= 7) {
        for (let i = 1; i <= total; i++) pages.push(i);
    } else {
        pages.push(1);
        if (current > 3) pages.push(-1);
        for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
            pages.push(i);
        }
        if (current < total - 2) pages.push(-1);
        pages.push(total);
    }
    return pages;
});

// Methods
const loadOrders = () => {

}

const exportOrders = () => {

}

const changePage = (page: number) => {

}

const confirmDelete = (id: number) => {

}

const printInvoice = (id: number) => { }

const viewOrderDetail = (id: number) => { }

const updateOrderStatus = (id: number, status: string) => { }
const getStatusSelectClass = (status: string) => { }
const getPaymentLabel = (paymentStatus: string) => { }
const getPaymentBadgeClass = (paymentStatus: string) => {

}
const formatCurrency = (price: number)=>{}
const formatDateTime = (date: string) => {}

const resetFilters =() => {}
const showCreateModal = () => {}
const debouncedSearch = () => {}
</script>