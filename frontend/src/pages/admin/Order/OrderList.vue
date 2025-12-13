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
                        <div class="col-md-2" v-for="(v, key) in statBlocks" :key="key">
                            <div class="stat-card text-white text-center py-3 rounded"
                                :class="v.bg">
                                <div class="stat-value">{{ v.value }}</div>
                                <div class="stat-label">{{ v.label }}</div>
                            </div>
                        </div>
                    </div>

                    <!-- Loading -->
                    <div v-if="loading" class="text-center py-5">
                        <div class="spinner-border text-primary"></div>
                    </div>

                    <!-- Table -->
                    <div v-else class="table-responsive">
                        <table class="table table-hover table-bordered">
                            <thead class="thead-light">
                                <tr>
                                    <th>Mã đơn</th>
                                    <th>Khách hàng</th>
                                    <th>Ngày đặt</th>
                                    <th>SL</th>
                                    <th>Tổng tiền</th>
                                    <th>Thanh toán</th>
                                    <th>Trạng thái</th>
                                    <th>Thao tác</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="order in orders" :key="order.id">
                                    <td><strong class="text-primary">#{{ order.code }}</strong></td>

                                    <td>
                                        <strong>{{ order.customerName }}</strong><br>
                                        <small class="text-muted">{{ order.customerPhone }}</small>
                                    </td>

                                    <td><small>{{ formatDateTime(order.createdAt) }}</small></td>

                                    <td class="text-center">
                                        <span class="badge badge-secondary badge-pill">{{ order.totalItems }}</span>
                                    </td>

                                    <td><strong class="text-success">{{ formatCurrency(order.totalAmount) }}</strong></td>

                                    <td>
                                        <span :class="getPaymentBadgeClass(order.paymentStatus)">
                                            {{ getPaymentLabel(order.paymentStatus) }}
                                        </span>
                                        <br>
                                        <small class="text-muted">{{ order.paymentMethod }}</small>
                                    </td>

                                    <td>
                                        <select class="form-control form-control-sm"
                                            :class="getStatusSelectClass(order.status)"
                                            v-model="order.status"
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
                                        <button class="btn btn-sm btn-info mr-1" @click="viewOrderDetail(order.id)">👁️</button>
                                        <button class="btn btn-sm btn-primary mr-1" @click="printInvoice(order.id)">🖨️</button>
                                        <button class="btn btn-sm btn-danger" @click="confirmDelete(order.id)"
                                            :disabled="order.status !== 'cancelled'">🗑️</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Pagination -->
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
                                Hiển thị {{ startIndex }} - {{ endIndex }} /
                                <strong>{{ pagination.total }}</strong> đơn hàng
                            </span>
                        </div>

                        <ul class="pagination mb-0">
                            <li class="page-item" :class="{ disabled: pagination.page === 1 }">
                                <a class="page-link" href="#" @click.prevent="changePage(pagination.page - 1)">‹</a>
                            </li>

                            <li v-for="p in displayPages" :key="p"
                                class="page-item" :class="{ active: p === pagination.page }">
                                <a class="page-link" href="#" @click.prevent="changePage(p)">{{ p }}</a>
                            </li>

                            <li class="page-item" :class="{ disabled: pagination.page === pagination.totalPages }">
                                <a class="page-link" href="#" @click.prevent="changePage(pagination.page + 1)">›</a>
                            </li>
                        </ul>
                    </div>

                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from "vue";

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

/* ----------------------------- STATE ----------------------------- */
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

/* ----------------------------- MOCK DATA ----------------------------- */
const mockOrders: Order[] = [
    { id: 1, code: 'ORD001', customerName: 'Nguyễn Văn A', customerPhone: '0901234567', totalItems: 3, totalAmount: 1250000, paymentStatus: 'paid', paymentMethod: 'COD', status: 'delivered', createdAt: '2025-12-10T10:30:00' },
    { id: 2, code: 'ORD002', customerName: 'Trần Thị B', customerPhone: '0912345678', totalItems: 2, totalAmount: 850000, paymentStatus: 'unpaid', paymentMethod: 'Banking', status: 'pending', createdAt: '2025-12-11T14:20:00' },
    { id: 3, code: 'ORD003', customerName: 'Lê Văn C', customerPhone: '0923456789', totalItems: 5, totalAmount: 2300000, paymentStatus: 'paid', paymentMethod: 'VNPay', status: 'shipping', createdAt: '2025-12-11T16:45:00' },
    { id: 4, code: 'ORD004', customerName: 'Phạm Thị D', customerPhone: '0934567890', totalItems: 1, totalAmount: 450000, paymentStatus: 'paid', paymentMethod: 'MoMo', status: 'processing', createdAt: '2025-12-12T09:15:00' },
    { id: 5, code: 'ORD005', customerName: 'Hoàng Văn E', customerPhone: '0945678901', totalItems: 4, totalAmount: 1800000, paymentStatus: 'unpaid', paymentMethod: 'COD', status: 'confirmed', createdAt: '2025-12-12T11:00:00' },
];

/* ----------------------------- STAT DISPLAY ----------------------------- */
const stats = ref({
    total: 156,
    pending: 23,
    processing: 45,
    delivered: 78,
    cancelled: 10,
    revenue: 456780000
});

const statBlocks = computed(() => ({
    total: { label: "Tổng đơn", value: stats.value.total, bg: "bg-info" },
    pending: { label: "Chờ xác nhận", value: stats.value.pending, bg: "bg-warning" },
    processing: { label: "Đang xử lý", value: stats.value.processing, bg: "bg-primary" },
    delivered: { label: "Đã giao", value: stats.value.delivered, bg: "bg-success" },
    cancelled: { label: "Đã hủy", value: stats.value.cancelled, bg: "bg-danger" },
    revenue: { label: "Doanh thu", value: formatCurrency(stats.value.revenue), bg: "bg-dark" },
}));

/* ----------------------------- PAGINATION COMPUTE ----------------------------- */

const displayPages = computed(() => {
    const pages: number[] = [];
    const total = pagination.value.totalPages;
    const current = pagination.value.page;

    for (let i = 1; i <= total; i++) pages.push(i);
    return pages;
});

const startIndex = computed(() =>
    (pagination.value.page - 1) * perPage.value + 1
);

const endIndex = computed(() =>
    Math.min(pagination.value.page * perPage.value, pagination.value.total)
);

/* ----------------------------- METHODS ----------------------------- */

const loadOrders = () => {
    loading.value = true;

    setTimeout(() => {
        let data = [...mockOrders];

        if (filters.value.search) {
            data = data.filter(o =>
                o.code.toLowerCase().includes(filters.value.search.toLowerCase()) ||
                o.customerName.toLowerCase().includes(filters.value.search.toLowerCase())
            );
        }

        if (filters.value.status)
            data = data.filter(o => o.status === filters.value.status);

        if (filters.value.paymentStatus)
            data = data.filter(o => o.paymentStatus === filters.value.paymentStatus);

        pagination.value.total = data.length;
        pagination.value.totalPages = Math.ceil(data.length / perPage.value);

        const start = (pagination.value.page - 1) * perPage.value;
        const end = start + perPage.value;

        orders.value = data.slice(start, end);
        loading.value = false;
    }, 300);
};

const changePage = (page: number) => {
    if (page < 1 || page > pagination.value.totalPages) return;
    pagination.value.page = page;
    loadOrders();
};

const exportOrders = () => alert("Export Excel (demo)");

const confirmDelete = (id: number) => alert("Xóa đơn: " + id);

const printInvoice = (id: number) => alert("In hóa đơn: " + id);

const viewOrderDetail = (id: number) => alert("Chi tiết đơn: " + id);

const updateOrderStatus = (id: number, status: string) => {
    alert(`Cập nhật Đơn #${id} → ${status}`);
};

const getStatusSelectClass = (status: string) => {
    return {
        "border-warning": status === "pending",
        "border-primary": status === "processing",
        "border-success": status === "delivered",
        "border-danger": status === "cancelled"
    };
};

const getPaymentLabel = (paymentStatus: string) => {
    return {
        unpaid: "Chưa thanh toán",
        paid: "Đã thanh toán",
        refunded: "Đã hoàn tiền"
    }[paymentStatus];
};

const getPaymentBadgeClass = (paymentStatus: string) => {
    return {
        unpaid: "badge badge-warning",
        paid: "badge badge-success",
        refunded: "badge badge-info"
    }[paymentStatus];
};

const formatCurrency = (price: number) =>
    price.toLocaleString("vi-VN") + "₫";

const formatDateTime = (date: string) => {
    const d = new Date(date);
    return d.toLocaleDateString("vi-VN") + " " + d.toLocaleTimeString("vi-VN");
};

let timer: any = null;
const debouncedSearch = () => {
    clearTimeout(timer);
    timer = setTimeout(() => {
        loadOrders();
    }, 300);
};

const resetFilters = () => {
    filters.value = {
        search: "",
        status: "",
        paymentStatus: "",
        fromDate: "",
        toDate: ""
    };
    loadOrders();
};

const showCreateModal = () => alert("Tạo đơn hàng (demo)");

onMounted(() => loadOrders());
</script>

<style scoped>
.stat-card {
    color: #fff;
    border-radius: 10px;
}
.stat-value {
    font-size: 20px;
    font-weight: bold;
}
.stat-label {
    font-size: 13px;
}
</style>
