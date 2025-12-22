<template>
    <div class="col-lg-3">
        <aside class="filter-sidebar">
            <div class="filter-header">
                <h5>Bộ lọc</h5>
            </div>

            <!-- Size Filter -->
            <div class="filter-section">
                <h6 class="filter-title">Size</h6>
                <div class="filter-options">
                    <Tag v-for="size in filterOptions.sizes" :label="size" />
                </div>
            </div>

            <!-- Color Filter -->
            <div class="filter-section">
                <h6 class="filter-title">Màu sắc</h6>
                <div class="color-options">
                    <div v-for="color in filterOptions.colors" :key="color"
                        :class="['color-item', { selected: filters.colors.includes(color) }]"
                        @click="toggleColor(color)" :title="color">
                        <div class="color-box" :style="{
                            backgroundColor: colorMap[color],
                            border: color == 'Trắng' ? '1px solid black' : 'none'
                        }">
                            <i class="pi pi-check d-flex justify-content-center align-items-center h-100"
                                :class="color == 'Trắng' ? 'text-black' : 'text-white'" style="font-size: 0.7em"></i>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Discount Filter -->
            <div class="filter-section">
                <h6 class="filter-title">Mức chiết khấu</h6>
                <div class="filter-options">
                    <label v-for="disc in filterOptions.discounts" :key="disc.value" class="filter-checkbox">
                        <input type="radio" name="discount" :value="disc.value" v-model="filters.discount" />
                        <span>{{ disc.label }}</span>
                    </label>
                </div>
            </div>

            <!-- Material Filter -->
            <div class="filter-section">
                <h6 class="filter-title">Chất liệu</h6>
                <div class="filter-options">
                    <label v-for="mat in filterOptions.materials" :key="mat" class="filter-checkbox">
                        <input type="checkbox" :value="mat" v-model="filters.materials" />
                        <span>{{ mat }}</span>
                    </label>
                </div>
            </div>

            <div class="filter-actions">
                <button class="btn btn-outline-secondary btn-block" @click="clearFilters">
                    Bỏ lọc
                </button>
            </div>
        </aside>
    </div>
    <Teleport to="body">
        <div v-if="showMobileFilter" class="mobile-filter-overlay mt-5 d-lg-none">
            <div class="filter-header mt-1">
                <h5>Bộ lọc</h5>
                <button class="btn btn-sm btn-danger" @click="localShowMobileFilter = false">
                    ✕
                </button>
            </div>

            <!-- Size Filter -->
            <div class="filter-section">
                <h6 class="filter-title">Size</h6>
                <div class="filter-options">
                    <Tag v-for="size in filterOptions.sizes" :label="size" />
                </div>
            </div>

            <!-- Color Filter -->
            <div class="filter-section">
                <h6 class="filter-title">Màu sắc</h6>
                <div class="color-options">
                    <div v-for="color in filterOptions.colors" :key="color"
                        :class="['color-item', { selected: filters.colors.includes(color) }]"
                        @click="toggleColor(color)" :title="color">
                        <div class="color-box" :style="{
                            backgroundColor: colorMap[color],
                            border: color === 'Trắng' ? '1px solid #ddd' : 'none'
                        }" />
                    </div>
                </div>
            </div>

            <!-- Discount Filter -->
            <div class="filter-section">
                <h6 class="filter-title">Mức chiết khấu</h6>
                <div class="filter-options">
                    <label v-for="disc in filterOptions.discounts" :key="disc.value" class="filter-checkbox">
                        <input type="radio" name="discount-mobile" :value="disc.value" v-model="filters.discount" />
                        <span>{{ disc.label }}</span>
                    </label>
                </div>
            </div>

            <!-- Material Filter -->
            <div class="filter-section">
                <h6 class="filter-title">Chất liệu</h6>
                <div class="filter-options">
                    <label v-for="mat in filterOptions.materials" :key="mat" class="filter-checkbox">
                        <input type="checkbox" :value="mat" v-model="filters.materials" />
                        <span>{{ mat }}</span>
                    </label>
                </div>
            </div>

            <div class="filter-actions">
                <button class="btn btn-outline-secondary btn-block mb-2" @click="clearFilters">
                    Bỏ lọc
                </button>
                <button class="btn btn-dark btn-block" @click="localShowMobileFilter = false">
                    Áp dụng
                </button>
            </div>
        </div>
    </Teleport>
</template>
<script setup lang="ts">
import Tag from '@/components/user/Tag.vue';
import { computed, ref } from 'vue';

const props = defineProps<{
    filters: Filters,
    currentPage: number
    showMobileFilter: boolean
}>()

const emit = defineEmits<{
    (e: 'update:filters', value: Filters): void
    (e: 'update:showMobileFilter', value: boolean): void
}>()

const localFilters = computed({
    get: () => props.filters,
    set: (val) => emit('update:filters', val)
})

const localShowMobileFilter = computed({
    get: () => props.showMobileFilter,
    set: (val) => emit('update:showMobileFilter', val)
})

interface Filters {
    sizes: string[]
    colors: string[]
    discount: string
    materials: string[]
}

interface DiscountOption {
    label: string
    value: string
}

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

const filterOptions = {
    sizes: ['S', 'M', 'L', 'XL', 'XXL', 'XXXL'],
    colors: ['Đen', 'Trắng', 'Xanh dương', 'Vàng', 'Hồng', 'Đỏ', 'Xám', 'Be', 'Nâu', 'Xanh lá', 'Cam', 'Tím'],
    discounts: [
        { label: 'Dưới 30%', value: '0-30' },
        { label: 'Từ 30% - 50%', value: '30-50' },
        { label: 'Từ 50% - 70%', value: '50-70' },
        { label: 'Từ 70%', value: '70-100' },
        { label: 'Giá đặc biệt', value: 'special' }
    ] as DiscountOption[],
    materials: ['Cotton', 'Lụa', 'Tencel', 'Chiffon', 'Linen', 'Denim', 'Khaki', 'Voan']
}

const toggleColor = (color: string) => {
    const colors = [...localFilters.value.colors]

    const index = colors.indexOf(color)
    if (index > -1) {
        colors.splice(index, 1)
    } else {
        colors.push(color)
    }

    localFilters.value = {
        ...localFilters.value,
        colors
    }
}

const clearFilters = () => {
    localFilters.value = {
        sizes: [],
        colors: [],
        discount: '',
        materials: []
    }

    localShowMobileFilter.value = false
}

</script>
<style>
.filter-sidebar {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    position: sticky;
    top: 20px;
    max-height: calc(100vh - 40px);
    overflow-y: auto;
}

.filter-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.filter-header h5 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
}

.filter-section {
    margin-bottom: 25px;
    padding-bottom: 20px;
    border-bottom: 1px solid #f0f0f0;
}

.filter-section:last-of-type {
    border-bottom: none;
}

.filter-title {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 15px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.filter-options {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.filter-checkbox {
    display: flex;
    align-items: center;
    cursor: pointer;
    font-size: 14px;
    margin: 0;
}

.filter-checkbox input {
    cursor: pointer;
    margin-right: 10px;
}

.color-options {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
}

.color-item {
    cursor: pointer;
    padding: 4px;
    border: 2px solid transparent;
    border-radius: 4px;
    transition: all 0.3s;
}

.color-item.selected {
    border-color: #000;
}

.color-box {
    width: 20px;
    height: 20px;
    border-radius: 50%;
}

.filter-actions {
    margin-top: 20px;
}

.mobile-filter-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: white;
    z-index: 1000;
    overflow-y: auto;
    padding: 20px;
}

@media (max-width: 991px) {
    .filter-sidebar:not(.mobile-filter-overlay) {
        display: none;
    }
}
</style>