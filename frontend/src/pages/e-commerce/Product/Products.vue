<template>
    <div class="ivymoda-container">
        <div class="px-lg-5 px-4">
            <!-- Breadcrumb -->
            <nav class="breadcrumb-custom">
                <a href="#">Trang chủ</a>
                <span class="mx-2">/</span>
                <a href="#">ÁO</a>
                <span class="mx-2">/</span>
                <span>Áo sơ mi</span>
            </nav>

            <!-- Page Header -->
            <div class="page-header">
                <h2>Áo Sơ Mi Nữ</h2>
            </div>

            <div class="row">
                <!-- Filter Sidebar - Desktop -->
                <Filter v-model:filters="filters" v-model:showMobileFilter="showMobileFilter"
                    :currentPage="currentPage" />

                <!-- Main Content -->
                <div class="col-lg-9">
                    <!-- Toolbar -->
                    <div class="toolbar">
                        <div class="toolbar-left">
                            <button class="filter-toggle d-lg-none d-block" @click="showMobileFilter = true">
                                ☰ Bộ lọc
                            </button>
                            <div class="result-count">
                                Hiển thị {{ paginatedProducts.length }} / {{ filteredProducts.length }} sản phẩm
                            </div>
                        </div>

                        <select class="sort-select" v-model="sortBy">
                            <option value="default">Sắp xếp: Mặc định</option>
                            <option value="newest">Mới nhất</option>
                            <option value="price-asc">Giá: Thấp đến cao</option>
                            <option value="price-desc">Giá: Cao đến thấp</option>
                            <option value="name">Tên A-Z</option>
                        </select>
                    </div>

                    <!-- Products Grid -->
                    <div class="products-grid">
                        <div v-for="product in paginatedProducts" :key="product.id" class="product-card">
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
                                    <span class="product-price">
                                        {{ formatPrice(product.price) }}
                                    </span>
                                    <span class="product-old-price">
                                        {{ formatPrice(product.oldPrice) }}
                                    </span>
                                </div>

                                <div class="product-sizes">
                                    <span v-for="size in product.sizes" :key="size" class="size-badge">
                                        {{ size }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Pagination -->
                    <div v-if="totalPages > 1" class="pagination-wrapper">
                        <ul class="pagination-custom">
                            <li :class="['page-item-custom', { disabled: currentPage === 1 }]"
                                @click="changePage(currentPage - 1)">
                                ‹
                            </li>

                            <li v-for="page in visiblePages" :key="page"
                                :class="['page-item-custom', { active: currentPage === page }]"
                                @click="changePage(page)">
                                {{ page }}
                            </li>

                            <li :class="['page-item-custom', { disabled: currentPage === totalPages }]"
                                @click="changePage(currentPage + 1)">
                                ›
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from "vue-router"
import Filter from './components/Filter.vue'

// Types
interface Product {
    id: number
    name: string
    code: string
    price: number
    oldPrice: number
    discount: number
    image: string
    colors: string[]
    sizes: string[]
    material: string
    isNew: boolean
    rating: number
}

interface Filters {
    sizes: string[]
    colors: string[]
    discount: string
    materials: string[]
}

const route = useRoute()
const slug = route.params.slug

const colorMap: Record<string, string> = {
    'Đen': '#000000',
    'Trắng': '#FFFFFF',
    'Xanh dương': '#0066CC',
    'Vàng': '#FFD700',
    'Hồng': '#FF69B4',
    'Đỏ': '#DC143C',
    'Xám': '#808080',
    'Be': '#F5F5DC',
    'Nâu': '#8B4513',
    'Xanh lá': '#228B22',
    'Cam': '#FF8C00',
    'Tím': '#9370DB'
}

// State
const allProducts = ref<Product[]>([])
const filters = ref<Filters>({
    sizes: [],
    colors: [],
    discount: '',
    materials: []
})
const sortBy = ref<string>('default')
const currentPage = ref<number>(1)
const itemsPerPage = ref<number>(24)
const showMobileFilter = ref<boolean>(false)

// Computed
const filteredProducts = computed<Product[]>(() => {
    let result = [...allProducts.value]

    if (filters.value.sizes.length > 0) {
        result = result.filter(p =>
            filters.value.sizes.some(s => p.sizes.includes(s))
        )
    }

    if (filters.value.colors.length > 0) {
        result = result.filter(p =>
            filters.value.colors.some(c => p.colors.includes(c))
        )
    }

    if (filters.value.materials.length > 0) {
        result = result.filter(p =>
            filters.value.materials.includes(p.material)
        )
    }

    if (filters.value.discount) {
        const [min, max] = filters.value.discount.split('-').map(Number)
        result = result.filter(p =>
            p.discount >= min! && p.discount <= (max || 100)
        )
    }

    // Sorting
    switch (sortBy.value) {
        case 'price-asc':
            result.sort((a, b) => a.price - b.price)
            break
        case 'price-desc':
            result.sort((a, b) => b.price - a.price)
            break
        case 'name':
            result.sort((a, b) => a.name.localeCompare(b.name, 'vi'))
            break
        case 'newest':
            result.sort((a, b) => b.id - a.id)
            break
        default:
            break
    }

    return result
})

const totalPages = computed<number>(() => {
    return Math.ceil(filteredProducts.value.length / itemsPerPage.value)
})

const paginatedProducts = computed<Product[]>(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    return filteredProducts.value.slice(start, end)
})

const visiblePages = computed<number[]>(() => {
    const pages: number[] = []
    const maxVisible = 5

    if (totalPages.value <= maxVisible) {
        for (let i = 1; i <= totalPages.value; i++) {
            pages.push(i)
        }
    } else if (currentPage.value <= 3) {
        for (let i = 1; i <= maxVisible; i++) {
            pages.push(i)
        }
    } else if (currentPage.value >= totalPages.value - 2) {
        for (let i = totalPages.value - maxVisible + 1; i <= totalPages.value; i++) {
            pages.push(i)
        }
    } else {
        for (let i = currentPage.value - 2; i <= currentPage.value + 2; i++) {
            pages.push(i)
        }
    }

    return pages
})

// Methods
const generateProducts = (): void => {
    const names = [
        'Áo sơ mi Ruby Drape',
        'Áo sơ mi Long Sleeves Tencel',
        'Áo sơ mi lụa trắng',
        'Áo sơ mi Stripe Tencel',
        'Áo sơ mi Tencel Petals',
        'Áo sơ mi Tencel cổ đức',
        'Áo sơ mi phối nơ cách điệu',
        'Áo sơ mi nơ Caramel',
        'Polka Dot Blouse - Áo sơ mi lụa',
        'Áo blouse kẻ họa tiết'
    ]

    const colors = ['Đen', 'Trắng', 'Xanh dương', 'Vàng', 'Hồng', 'Đỏ', 'Xám', 'Be', 'Nâu', 'Xanh lá']
    const sizes = ['S', 'M', 'L', 'XL', 'XXL']
    const materials = ['Cotton', 'Lụa', 'Tencel', 'Chiffon', 'Linen']

    allProducts.value = Array.from({ length: 48 }, (_, i) => ({
        id: i + 1,
        name: names[i % names.length]!,
        code: `MS-17B0${String(i + 100).padStart(3, '0')}`,
        price: Math.floor(Math.random() * 1000000) + 500000,
        oldPrice: Math.floor(Math.random() * 1500000) + 1000000,
        discount: Math.floor(Math.random() * 50) + 10,
        image: `https://picsum.photos/seed/${i + 1}/300/400`,
        colors: [
            colors[Math.floor(Math.random() * colors.length)]!,
            colors[Math.floor(Math.random() * colors.length)]!
        ],
        sizes: sizes.slice(0, Math.floor(Math.random() * 3) + 3),
        material: materials[Math.floor(Math.random() * materials.length)]!,
        isNew: i < 6,
        rating: Math.floor(Math.random() * 2) + 4
    }))
}

const changePage = (page: number): void => {
    if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
        window.scrollTo({ top: 0, behavior: 'smooth' })
    }
}

const formatPrice = (price: number): string => {
    return price.toLocaleString('vi-VN') + 'đ'
}

// Watchers
watch(filters, () => {
    currentPage.value = 1
}, { deep: true })

// Lifecycle
onMounted(() => {
    generateProducts()
})
</script>

<style scoped>
.ivymoda-container {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: #f8f9fa;
    min-height: 100vh;
    padding: 20px 0;
}

.breadcrumb-custom {
    background: transparent;
    padding: 10px 0;
    margin-bottom: 20px;
    font-size: 14px;
}

.breadcrumb-custom a {
    color: #666;
    text-decoration: none;
}

.breadcrumb-custom a:hover {
    color: #000;
}

.page-header h1 {
    font-size: 28px;
    font-weight: 600;
    margin-bottom: 30px;
}

.toolbar {
    background: white;
    padding: 15px 20px;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.toolbar-left {
    display: flex;
    align-items: center;
    gap: 15px;
}

.result-count {
    font-size: 14px;
    color: #666;
}

.sort-select {
    padding: 8px 15px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    background: white;
    min-width: 200px;
}

.filter-toggle {
    /* display: none; */
    padding: 8px 15px;
    background: #000;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.products-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

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
    gap: 10px;
}

.product-price {
    font-size: 18px;
    font-weight: 700;
    color: #FF4444;
}

.product-old-price {
    font-size: 14px;
    color: #999;
    text-decoration: line-through;
}

.product-sizes {
    display: flex;
    gap: 5px;
    margin-top: 10px;
    flex-wrap: wrap;
}

.size-badge {
    padding: 3px 8px;
    border: 1px solid #ddd;
    border-radius: 3px;
    font-size: 11px;
    color: #666;
}

.pagination-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 40px;
}

.pagination-custom {
    display: flex;
    gap: 5px;
    list-style: none;
    padding: 0;
    margin: 0;
}

.page-item-custom {
    cursor: pointer;
    padding: 8px 12px;
    border: 1px solid #ddd;
    background: white;
    color: #333;
    border-radius: 4px;
    transition: all 0.3s;
    font-size: 14px;
    user-select: none;
}

.page-item-custom:hover:not(.disabled):not(.active) {
    background: #f5f5f5;
}

.page-item-custom.active {
    background: #000;
    color: white;
    border-color: #000;
}

.page-item-custom.disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

@media (max-width: 768px) {
    .products-grid {
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
    }

    .product-name {
        font-size: 13px;
        min-height: 36px;
    }

    .product-price {
        font-size: 15px;
    }

    .toolbar {
        flex-direction: column;
        align-items: stretch;
    }

    .toolbar-left {
        width: 100%;
        flex-direction: column;
        align-items: stretch;
    }

    .sort-select {
        width: 100%;
    }
}

@media (max-width: 576px) {
    .ivymoda-container {
        padding: 10px 0;
    }

    .products-grid {
        grid-template-columns: 1fr;
    }
}
</style>