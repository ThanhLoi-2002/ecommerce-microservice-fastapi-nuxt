<template>
  <div>
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="mb-0">📊 Dashboard Thống kê</h3>

      <!-- Bộ lọc -->
      <div class="d-flex">
        <select class="form-control mr-2" v-model="filters.range" @change="loadStats">
          <option value="7">7 ngày</option>
          <option value="30">30 ngày</option>
          <option value="90">90 ngày</option>
          <option value="365">1 năm</option>
        </select>

        <input
          type="date"
          class="form-control mr-2"
          v-model="filters.from"
          @change="loadStats"
        />

        <input
          type="date"
          class="form-control"
          v-model="filters.to"
          @change="loadStats"
        />
      </div>
    </div>

    <!-- Stat Cards -->
    <div class="row">
      <div class="col-md-3 mb-4" v-for="card in statCards" :key="card.title">
        <div class="card stat-card shadow-sm">
          <div class="card-body">
            <h6 class="text-muted mb-1">{{ card.title }}</h6>
            <h3 class="font-weight-bold">{{ card.value }}</h3>
            <small :class="card.growth >= 0 ? 'text-success' : 'text-danger'">
              {{ card.growth >= 0 ? "▲" : "▼" }} {{ card.growth }}%
            </small>
          </div>
        </div>
      </div>
    </div>

    <!-- Chart -->
    <div class="card p-4 shadow-sm mb-4">
      <h5 class="mb-3">📈 Doanh thu theo ngày</h5>
      <canvas ref="revenueChart"></canvas>
    </div>

    <!-- Top Selling Products -->
    <div class="card p-4 shadow-sm mb-4">
      <h5 class="mb-3">🔥 Top sản phẩm bán chạy</h5>

      <table class="table table-hover">
        <thead>
          <tr>
            <th>Sản phẩm</th>
            <th>Đã bán</th>
            <th>Doanh thu</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.name">
            <td>{{ p.name }}</td>
            <td>{{ p.sold }}</td>
            <td>{{ formatCurrency(p.revenue) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Recent Orders -->
    <div class="card p-4 shadow-sm">
      <h5 class="mb-3">🧾 Đơn hàng mới nhất</h5>

      <table class="table table-bordered table-sm">
        <thead class="thead-light">
          <tr>
            <th>Mã</th>
            <th>Khách hàng</th>
            <th>Tổng tiền</th>
            <th>Trạng thái</th>
            <th>Ngày</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="o in recentOrders" :key="o.code">
            <td><strong>#{{ o.code }}</strong></td>
            <td>{{ o.customer }}</td>
            <td class="text-success">{{ formatCurrency(o.total) }}</td>
            <td>
              <span class="badge badge-pill" :class="getStatusClass(o.status)">
                {{ o.status }}
              </span>
            </td>
            <td>{{ o.date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import Chart from "chart.js/auto";

/* ---------------------------
  STATE
----------------------------*/
const filters = ref({
  range: "7",
  from: "",
  to: "",
});

const statCards = ref([
  { title: "Doanh thu", value: "₫24,300,000", growth: 12 },
  { title: "Đơn hàng", value: "1,240", growth: 5 },
  { title: "Khách hàng mới", value: "320", growth: -3 },
  { title: "Tồn kho", value: "8,560", growth: 0 },
]);

const products = ref([
  { name: "T-Shirt Basic", sold: 120, revenue: 2400000 },
  { name: "Hoodie Trendy", sold: 80, revenue: 3200000 },
  { name: "Jeans Slim", sold: 65, revenue: 3900000 },
]);

const recentOrders = ref([
  { code: "ORD123", customer: "Nguyễn Văn A", total: 750000, status: "pending", date: "2025-12-11" },
  { code: "ORD124", customer: "Lê Thị B", total: 1250000, status: "shipping", date: "2025-12-11" },
  { code: "ORD125", customer: "Phạm Văn C", total: 560000, status: "delivered", date: "2025-12-12" },
]);

/* ---------------------------
  CHART
----------------------------*/
const revenueChart = ref<HTMLCanvasElement | null>(null);
let chart: Chart | null = null;

const loadChart = () => {
  const ctx = revenueChart.value!;
  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
      datasets: [
        {
          label: "Revenue",
          data: [120, 200, 150, 300, 250, 400, 350],
          borderWidth: 3,
          tension: 0.3,
        },
      ],
    },
    options: {
      responsive: true,
    },
  });
};

/* ---------------------------
  HELPERS
----------------------------*/
const formatCurrency = (v: number) =>
  v.toLocaleString("vi-VN", { style: "currency", currency: "VND" });

const getStatusClass = (s: string) => {
  switch (s) {
    case "pending":
      return "badge-warning";
    case "shipping":
      return "badge-info";
    case "delivered":
      return "badge-success";
    default:
      return "badge-secondary";
  }
};

/* ---------------------------
  LOAD DATA
----------------------------*/
const loadStats = () => {
  console.log("Reload dashboard with filter:", filters.value);
  // TODO: Gọi API load dữ liệu theo bộ lọc
};

onMounted(() => {
  loadChart();
  loadStats();
});
</script>

<style scoped>
.stat-card {
  border-left: 6px solid #d6336c;
  border-radius: 12px;
}
</style>
