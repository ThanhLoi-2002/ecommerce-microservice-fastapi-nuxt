<template>
  <div>
    <h3 class="mb-4">Overview</h3>

    <div class="row">
      <div class="col-md-3 mb-4" v-for="card in cards" :key="card.title">
        <div class="card stat-card">
          <div class="card-body">
            <h6 class="text-muted">{{ card.title }}</h6>
            <h3 class="font-weight-bold">{{ card.value }}</h3>
          </div>
        </div>
      </div>
    </div>

    <div class="card p-4 mt-4">
      <h5 class="mb-3">Top Selling Products</h5>

      <table class="table table-hover">
        <thead>
          <tr>
            <th>Product</th>
            <th>Sold</th>
            <th>Revenue</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.name">
            <td>{{ p.name }}</td>
            <td>{{ p.sold }}</td>
            <td>${{ p.revenue }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
const cards = [
  { title: "Total Sales", value: "$24,300" },
  { title: "Orders", value: "1,240" },
  { title: "Customers", value: "320" },
  { title: "Stock", value: "8,560" },
];

const products = [
  { name: "T-Shirt Basic", sold: 120, revenue: 2400 },
  { name: "Hoodie Trendy", sold: 80, revenue: 3200 },
  { name: "Jeans Slim", sold: 65, revenue: 3900 },
];
</script>

<style scoped>
.stat-card {
  border-left: 5px solid #d14a6c;
  border-radius: 12px;
}
</style>
