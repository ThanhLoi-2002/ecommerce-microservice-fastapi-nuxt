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
                <Filter v-model:filters="filters" v-model:showMobileFilter="showMobileFilter" />

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
                        <ProductCart v-for="product in paginatedProducts" :product="product" :colorMap="colorMap" />
                    </div>

                    <!-- Pagination -->
                    <Pagination/>
                </div>
            </div>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from "vue-router"
import Filter from './components/Filter.vue'
import { productFilterDefault } from '@/utils/constants'
import ProductCart from './components/ProductCart.vue'
import Pagination from '@/components/user/Pagination.vue'

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
    price: number[]
    discount: string
    page: number
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
const filters = ref<Filters>(productFilterDefault)
const sortBy = ref<string>('default')
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

const paginatedProducts = computed<Product[]>(() => {
    const start = (filters.value.page - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    return filteredProducts.value.slice(start, end)
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

// Watchers
// watch(filters, () => {
//     currentPage.value = 1
// }, { deep: true })

// Lifecycle
onMounted(() => {
    generateProducts()
})
</script>

<style scoped>
.ivymoda-container {
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