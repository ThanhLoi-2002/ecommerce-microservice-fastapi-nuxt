<template>
  <div>
    <!-- Banner -->
    <div class="jumbotron text-center bg-light py-5 mb-4">
      <h1 class="display-4 font-weight-bold">Fashion Sale 50%</h1>
      <p class="lead">Trendy outfits. Best prices.</p>
      <button class="btn btn-dark btn-lg">Shop Now</button>
    </div>

    <div class="container">
      <h3 class="mb-4 font-weight-bold">New Arrivals</h3>

      <div class="row">
        <div
          class="col-6 col-md-4 col-lg-3 mb-4"
          v-for="(p, i) in products"
          :key="i"
        >
          <ProductCard
            :name="p.name"
            :price="p.price"
            :image="p.image"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import ProductCard from "../../../components/user/product/ProductCard.vue";

const products = [
  { name: "Hoodie Black", price: 320000, image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAPnWpPy1giBToNFv9rak78IZfSmzGyxHvqw&s" },
  { name: "T-shirt Oversize", price: 190000, image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAPnWpPy1giBToNFv9rak78IZfSmzGyxHvqw&s" },
  { name: "Jeans Slimfit", price: 450000, image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAPnWpPy1giBToNFv9rak78IZfSmzGyxHvqw&s" },
  { name: "Street Jacket", price: 599000, image: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSAPnWpPy1giBToNFv9rak78IZfSmzGyxHvqw&s" },
];
</script>
