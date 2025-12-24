<template>
    <div :key="product.id" class="product-card">
        <router-link :to="`/product/${product.id}`" class="">
            <div class="product-image">
                <div v-if="product.isNew" class="product-badge new">
                    NEW
                </div>
                <div v-if="product.discount > 0" class="product-badge discount">
                    -{{ product.discount }}%
                </div>
                <img :src="product.image" :alt="product.name" loading="lazy" />
            </div>
        </router-link>

        <div class="product-info">
            <div class="product-colors">
                <div v-for="(color, idx) in product.colors" :key="idx" class="product-color-dot"
                    :style="{ backgroundColor: colorMap[color] }" :title="color" />
            </div>

            <div class="product-name">{{ product.name }}</div>

            <div class="product-prices">
                <div><span class="product-price">
                        {{ formatPrice(product.price) }}
                    </span>
                    <span class="product-old-price">
                        {{ formatPrice(product.oldPrice) }}
                    </span>
                </div>

                <div class="position-relative d-inline-block">
                    <button class="btn btn-outline-dark" @click.stop="toggleSize">
                        <i class="pi pi-shopping-cart"></i>
                    </button>

                    <transition name="slide-fade">
                        <ul v-if="openSize" class="size-box shadow bg-white rounded">
                            <li v-for="size in sizes" :key="size.name" @click="size.quantity > 0 && selectSize(size)"
                                :class="[
                                    'size-item',
                                    size.quantity > 0 ? 'active' : 'disabled'
                                ]">
                                {{ size.name }}
                            </li>
                        </ul>
                    </transition>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { formatPrice } from '@/utils/format';
import { ref } from 'vue';


const props = defineProps<{
    product: any
    colorMap: any
}>()

const openSize = ref(false)
const sizes = [{ name: 'S', quantity: 0 }, { name: 'M', quantity: 10 }, { name: 'L', quantity: 5 }, { name: 'XL', quantity: 0 }, { name: 'XXL', quantity: 0 }]

const addCart = (size: string, quantity: number) => {

}

const toggleSize = () => {
    openSize.value = !openSize.value;
};

const selectSize = (size: { name: string; quantity: number }) => {
    addCart(size.name, 1);
    openSize.value = false;
};
</script>

<style>
.product-card {
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: all 0.3s;
    cursor: pointer;
}

.product-card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    transform: translateY(-4px);
}

.product-image {
    position: relative;
    padding-top: 90%;
    overflow: hidden;
    background: #f5f5f5;
}

.product-image img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s;
}

.product-card:hover .product-image img {
    transform: scale(1.05);
}

.product-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: #000;
    color: white;
    padding: 5px 10px;
    font-size: 12px;
    font-weight: 600;
    border-radius: 3px;
    z-index: 1;
}

.product-badge.new {
    background: #FF4444;
}

.product-badge.discount {
    background: #FF6B35;
    top: 10px;
    right: 10px;
    left: auto;
}

.product-info {
    padding: 15px;
}

.product-colors {
    display: flex;
    gap: 6px;
    margin-bottom: 10px;
}

.product-color-dot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 1px solid #ddd;
}

.product-name {
    font-size: 15px;
    font-weight: 500;
    margin-bottom: 10px;
    color: #333;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.4;
    min-height: 42px;
}

.product-prices {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
}

.product-price {
    font-size: 18px;
    font-weight: 700;
    color: #FF4444;
    margin-right: 8px;
}

.product-old-price {
    font-size: 14px;
    color: #999;
    text-decoration: line-through;
}

.btn-outline-dark i {
    color: black;
}

.btn-outline-dark:hover i {
    color: white;
}

/* BOX */
.size-box {
  position: absolute;
  bottom: 55px;       /* nằm trên icon */
  right: 0;
  min-width: 100px;
  padding: 6px 0;
  margin: 0;          /* ❗ fix lệch */
  list-style: none;  /* ❗ fix lệch */
  text-align: center;
  z-index: 1000;
}

/* ITEM */
.size-item {
  padding: 8px 0;
  font-weight: 600;
  cursor: pointer;
}

.size-item:hover {
  background: #f1f1f1;
}

.size-item.disabled {
  color: #adb5bd;
  cursor: not-allowed;
}

/* =========================
   ANIMATION SLIDE + FADE
========================= */
.slide-fade-enter-active {
  transition: all 0.4s ease;
}

.slide-fade-leave-active {
  transition: all 0.4s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(100px); /* từ dưới lên */
}

.slide-fade-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-50px); /* lên trên khi đóng */
}
</style>