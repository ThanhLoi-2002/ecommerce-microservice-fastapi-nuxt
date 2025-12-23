<template>
    <div :key="product.id" class="product-card">
        <div class="product-image">
            <div v-if="product.isNew" class="product-badge new">
                NEW
            </div>
            <div v-if="product.discount > 0" class="product-badge discount">
                -{{ product.discount }}%
            </div>
            <img :src="product.image" :alt="product.name" />
        </div>

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

                <router-link :to="`/product/${product.id}`" class="btn btn-cart"><i
                        class="pi pi-shopping-cart text-white" /></router-link>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { formatPrice } from '@/utils/format';


const props = defineProps<{
    product: any
    colorMap: any
}>()
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
    padding-top: 133%;
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

.btn-cart {
    background-color: rgba(0, 0, 0);
}

.btn-cart:hover {
    background-color: rgba(0, 0, 0, 0.8);
}
</style>