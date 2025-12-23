<template>
    <div class="col-lg-3">
        <aside class="filter-sidebar">
            <div class="filter-header">
                <h5>Bộ lọc</h5>
            </div>

            <!-- Size Filter -->
            <div class="filter-section">
                <div class="d-flex justify-content-between">
                    <h6 class="filter-title">Size</h6>
                    <i class="pi" :class="showItems.size ? 'pi-minus' : 'pi-plus'"
                        @click="showItems.size = !showItems.size" />
                </div>
                <transition name="collapse">
                    <div class="filter-options pb-3" v-show="showItems.size">
                        <Tag v-for="size in filterOptions.sizes" :label="size" :onClick="() => toggleSize(size)"
                            :class="filters.sizes.includes(size) ? 'active' : ''" />
                    </div>
                </transition>
            </div>

            <!-- Color Filter -->
            <div class="filter-section">
                <div class="d-flex justify-content-between">
                    <h6 class="filter-title">Màu sắc</h6>
                    <i class="pi" :class="showItems.color ? 'pi-minus' : 'pi-plus'"
                        @click="showItems.color = !showItems.color" />
                </div>
                <transition name="collapse">
                    <div class="color-options pb-3" v-show="showItems.color">
                        <div v-for="color in filterOptions.colors" :key="color" :class="'color-item'"
                            @click="toggleColor(color)" :title="color">
                            <div class="color-box" :style="{
                                backgroundColor: colorMap[color],
                                border: color == 'Trắng' ? '1px solid black' : 'none'
                            }">
                                <i v-if="filters.colors.includes(color)"
                                    class="pi pi-check d-flex justify-content-center align-items-center h-100"
                                    :class="color == 'Trắng' ? 'text-black' : 'text-white'"
                                    style="font-size: 0.7em"></i>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>

            <!-- Price Filter -->
            <div class="filter-section">
                <div class="d-flex justify-content-between">
                    <h6 class="filter-title">Mức giá</h6>
                    <i class="pi" :class="showItems.price ? 'pi-minus' : 'pi-plus'"
                        @click="showItems.price = !showItems.price" />
                </div>

                <transition name="collapse">
                    <div v-show="showItems.price" class="">
                        <!-- Range slider container -->
                        <div class="range-slider">
                            <div class="slider-track"></div>
                            <div class="slider-range" :style="rangeStyle"></div>

                            <input type="range" :min="PRICE_MIN" :max="PRICE_MAX" :step="step"
                                v-model.number="filters.price[0]!" @input="handleMinChange" class="slider-input" />
                            <input type="range" :min="PRICE_MIN" :max="PRICE_MAX" :step="step"
                                v-model.number="filters.price[1]!" @input="handleMaxChange" class="slider-input" />

                            <!-- Price labels below thumbs -->
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="mt-3">
                                    {{ formatPrice(filters.price[0]!) }}
                                </div>
                                <div class="mt-3">
                                    {{ formatPrice(filters.price[1]!) }}
                                </div>
                            </div>

                        </div>
                    </div>
                </transition>
            </div>


            <!-- Discount Filter -->
            <div class="filter-section">
                <div class="d-flex justify-content-between">
                    <h6 class="filter-title">Mức chiết khấu</h6>
                    <i class="pi" :class="showItems.discount ? 'pi-minus' : 'pi-plus'"
                        @click="showItems.discount = !showItems.discount" />
                </div>

                <transition name="collapse">
                    <div class="pb-3" v-show="showItems.discount" style="gap: 8px">
                        <label v-for="disc in filterOptions.discounts" :key="disc.value"
                            class="filter-checkbox custom-radio">
                            <input type="checkbox" :checked="filters.discount === disc.value"
                                @change="toggleDiscount(disc.value)" />
                            <span class="radio-ui"></span>
                            <span class="label-text">{{ disc.label }}</span>
                        </label>
                    </div>
                </transition>
            </div>

            <div class="filter-actions">
                <button class="btn btn-outline-secondary btn-block" @click="clearFilters">
                    Bỏ lọc
                </button>
            </div>
        </aside>
    </div>

    <!-- Mobile -->
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
                <div class="d-flex justify-content-between">
                    <h6 class="filter-title">Size</h6>
                    <i class="pi" :class="showItems.size ? 'pi-minus' : 'pi-plus'"
                        @click="showItems.size = !showItems.size" />
                </div>
                <transition name="collapse">
                    <div class="filter-options pb-3" v-show="showItems.size">
                        <Tag v-for="size in filterOptions.sizes" :label="size" :onClick="() => toggleSize(size)"
                            :class="filters.sizes.includes(size) ? 'active' : ''" />
                    </div>
                </transition>
            </div>

            <!-- Color Filter -->
            <div class="filter-section">
                <div class="d-flex justify-content-between">
                    <h6 class="filter-title">Màu sắc</h6>
                    <i class="pi" :class="showItems.color ? 'pi-minus' : 'pi-plus'"
                        @click="showItems.color = !showItems.color" />
                </div>
                <transition name="collapse">
                    <div class="color-options pb-3" v-show="showItems.color">
                        <div v-for="color in filterOptions.colors" :key="color" :class="'color-item'"
                            @click="toggleColor(color)" :title="color">
                            <div class="color-box" :style="{
                                backgroundColor: colorMap[color],
                                border: color == 'Trắng' ? '1px solid black' : 'none'
                            }">
                                <i v-if="filters.colors.includes(color)"
                                    class="pi pi-check d-flex justify-content-center align-items-center h-100"
                                    :class="color == 'Trắng' ? 'text-black' : 'text-white'"
                                    style="font-size: 0.7em"></i>
                            </div>
                        </div>
                    </div>
                </transition>
            </div>

            <!-- Price Filter -->
            <div class="filter-section">
                <div class="d-flex justify-content-between">
                    <h6 class="filter-title">Mức giá</h6>
                    <i class="pi" :class="showItems.price ? 'pi-minus' : 'pi-plus'"
                        @click="showItems.price = !showItems.price" />
                </div>

                <transition name="collapse">
                    <div v-show="showItems.price" class="">
                        <!-- Range slider container -->
                        <div class="range-slider">
                            <div class="slider-track"></div>
                            <div class="slider-range" :style="rangeStyle"></div>

                            <input type="range" :min="PRICE_MIN" :max="PRICE_MAX" :step="step"
                                v-model.number="filters.price[0]!" @input="handleMinChange" class="slider-input" />
                            <input type="range" :min="PRICE_MIN" :max="PRICE_MAX" :step="step"
                                v-model.number="filters.price[1]!" @input="handleMaxChange" class="slider-input" />

                            <!-- Price labels below thumbs -->
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="mt-3">
                                    {{ formatPrice(filters.price[0]!) }}
                                </div>
                                <div class="mt-3">
                                    {{ formatPrice(filters.price[1]!) }}
                                </div>
                            </div>

                        </div>
                    </div>
                </transition>
            </div>

            <!-- Discount Filter -->
            <div class="filter-section">
                <div class="d-flex justify-content-between">
                    <h6 class="filter-title">Mức chiết khấu</h6>
                    <i class="pi" :class="showItems.discount ? 'pi-minus' : 'pi-plus'"
                        @click="showItems.discount = !showItems.discount" />
                </div>

                <transition name="collapse">
                    <div class="pb-3" v-show="showItems.discount" style="gap: 8px">
                        <label v-for="disc in filterOptions.discounts" :key="disc.value"
                            class="filter-checkbox custom-radio">
                            <input type="checkbox" :checked="filters.discount === disc.value"
                                @change="toggleDiscount(disc.value)" />
                            <span class="radio-ui"></span>
                            <span class="label-text">{{ disc.label }}</span>
                        </label>
                    </div>
                </transition>
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
import { useSize } from '@/composables/useSize';
import { useSizeStore } from '@/stores/size.store';
import { PRICE_MAX, PRICE_MIN, productFilterDefault } from '@/utils/constants';
import { formatPrice } from '@/utils/format';
import { storeToRefs } from 'pinia';
import { computed, ref, watch } from 'vue';

const props = defineProps<{
    filters: Filters
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
    price: number[]
    discount: string
    page: number
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

const filterOptions = ref<any>({
    sizes: [],
    colors: ['Đen', 'Trắng', 'Xanh dương', 'Vàng', 'Hồng', 'Đỏ', 'Xám', 'Be', 'Nâu', 'Xanh lá', 'Cam', 'Tím'],
    discounts: [
        { label: 'Dưới 30%', value: '0-30' },
        { label: 'Từ 30% - 50%', value: '30-50' },
        { label: 'Từ 50% - 70%', value: '50-70' },
        { label: 'Từ 70%', value: '70-100' },
        { label: 'Giá đặc biệt', value: 'special' }
    ] as DiscountOption[],
})

const showItems = ref<any>({
    size: false,
    clolor: false,
    price: false,
    discount: false
})

const sizeStore = useSizeStore()
const { sizes } = storeToRefs(sizeStore)
const { getSizes } = useSize()

// Theo dõi sự thay đổi trong sizes
watch(sizes, (newSizes) => {
    filterOptions.value.sizes = newSizes.map(s => s.name);
}, { immediate: true }); // Chạy ngay khi component được khởi tạo

getSizes();

const toggleSize = (size: string) => {
    const sizes = [...localFilters.value.sizes]

    const index = sizes.indexOf(size)
    if (index > -1) {
        sizes.splice(index, 1)
    } else {
        sizes.push(size)
    }

    localFilters.value = {
        ...localFilters.value,
        sizes
    }
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

const toggleDiscount = (value: string) => {
    if (localFilters.value.discount === value) {
        // click lại → bỏ chọn
        localFilters.value.discount = ''
    } else {
        // chọn mới → tự động bỏ cái cũ
        localFilters.value.discount = value
    }
}

const step = ref(100000);

const handleMinChange = (e: any) => {
    localFilters.value.price[0] = e.target.value
};

const handleMaxChange = (e: any) => {
    localFilters.value.price[1] = e.target.value
};

const getPercent = (value: number): number => {
    return ((value - PRICE_MIN) / (PRICE_MAX - PRICE_MIN)) * 100;
};

const rangeStyle = computed(() => {
    const minPercent = getPercent(localFilters.value.price[0]!);
    const maxPercent = getPercent(localFilters.value.price[1]!);

    return {
        left: `${minPercent}%`,
        width: `${maxPercent - minPercent}%`
    };
});

const clearFilters = () => {
    localFilters.value = {
        sizes: [],
        colors: [],
        price: [PRICE_MIN, PRICE_MAX],
        discount: '',
        page: 1
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

/* Collapse animation */
.collapse-enter-active,
.collapse-leave-active {
    transition: all 0.5s ease;
}

.collapse-enter-from,
.collapse-leave-to {
    opacity: 0;
    max-height: 0;
    transform: translateY(-4px);
}

.collapse-enter-to,
.collapse-leave-from {
    opacity: 1;
    max-height: 200px;
    /* chỉnh lớn hơn nội dung */
    transform: translateY(0);
}

.range-slider {
    position: relative;
    height: 50px;
    margin-top: 15px;
}

.slider-track {
    position: absolute;
    top: 0;
    width: 100%;
    height: 4px;
    background: #e0e0e0;
    border-radius: 4px;
}

.slider-range {
    position: absolute;
    top: 0;
    height: 4px;
    background: #333;
    border-radius: 4px;
    z-index: 1;
}

.slider-input {
    position: absolute;
    width: 100%;
    height: 4px;
    background: none;
    pointer-events: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    appearance: none;
    z-index: 2;
}

.slider-input::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 20px;
    height: 20px;
    background: #333;
    border: 3px solid #fff;
    border-radius: 50%;
    cursor: pointer;
    pointer-events: all;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.slider-input::-moz-range-thumb {
    width: 20px;
    height: 20px;
    background: #333;
    border: 3px solid #fff;
    border-radius: 50%;
    cursor: pointer;
    pointer-events: all;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.slider-input::-webkit-slider-thumb:hover {
    background: #000;
    transform: scale(1.15);
}

.slider-input::-moz-range-thumb:hover {
    background: #000;
    transform: scale(1.15);
}

.pi {
    cursor: pointer;
}

.filter-checkbox {
    display: flex;
    align-items: center;
    cursor: pointer;
    gap: 8px;
    user-select: none;
}

/* Ẩn checkbox gốc */
.filter-checkbox input {
    display: none;
}

/* Vòng tròn */
.radio-ui {
    width: 16px;
    height: 16px;
    border: 1px solid #000;
    border-radius: 50%;
    position: relative;
}

/* Chấm đen khi active */
.filter-checkbox input:checked+.radio-ui::after {
    content: '';
    width: 8px;
    height: 8px;
    background: #000;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>