<!-- Navbar.vue -->
<template>
    <nav class="sticky-top bg-white shadow">
        <!-- Top Bar - Hidden on mobile -->
        <div class="bg-dark text-white py-2 small d-none d-lg-block">
            <div class="px-5">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="d-flex">
                        <span class="text-sm">🔥 BIG SALE THÁNG 12 - GIẢM ĐẾN 50%</span>
                    </div>
                    <div class="d-flex">
                        📞 <a href="tel:0901234567" class="text-sm text-white">Hotline: 0901 234 567</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Desktop Navigation -->
        <div class="navbar-expand-lg navbar-light bg-light py-3 d-none d-lg-block">
            <div class="px-5">
                <div class="d-flex align-items-center">
                    <!-- Main Menu -->
                    <ul class="navbar-nav d-flex list-unstyled m-0 p-0 flex-fill">
                        <li class="nav-item position-relative mr-3 has-dropdown" @mouseenter="activeMenu = 'female'"
                            @mouseleave="activeMenu = null">
                            <a href="#"
                                class="nav-link text-dark text-decoration-none font-weight-bold d-flex align-items-center py-2 menu-link">
                                NỮ
                            </a>

                            <!-- Mega Menu Female -->
                            <div class="position-absolute bg-white shadow-lg p-4 mt-2 mega-menu-wrapper"
                                v-show="activeMenu === 'female'">
                                <div class="mega-menu-content d-flex flex-wrap">
                                    <div class="text-nowrap" v-for="c in femaleCategories" :key="c.id">
                                        <h3 class="small font-weight-bold mb-3 text-dark text-uppercase">
                                            <router-link :to="{ name: 'products', params: { slug: c.slug } }"
                                                class="text-dark menu-link">{{ c.name
                                                }}</router-link>
                                        </h3>
                                        <ul class="mega-menu-list">
                                            <li v-for="child in c.children" :key="child.id">
                                                <router-link :to="{ name: 'products', params: { slug: child.slug } }"
                                                    class="text-dark menu-link">{{ child.name
                                                    }}</router-link>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </li>

                        <li class="nav-item position-relative mr-3 has-dropdown" @mouseenter="activeMenu = 'male'"
                            @mouseleave="activeMenu = null">
                            <a href="#"
                                class="nav-link text-dark text-decoration-none font-weight-bold d-flex align-items-center py-2 menu-link">
                                NAM
                            </a>

                            <!-- Mega Menu Male -->
                            <div class="position-absolute bg-white shadow-lg p-4 mt-2 mega-menu-wrapper"
                                v-show="activeMenu === 'male'">
                                <div class="mega-menu-content d-flex flex-wrap">
                                    <div class="text-nowrap" v-for="c in maleCategories" :key="c.id">
                                        <h3 class="small font-weight-bold mb-3 text-dark text-uppercase">
                                            <router-link :to="{ name: 'products', params: { slug: c.slug } }"
                                                class="text-dark menu-link">{{ c.name
                                                }}</router-link>
                                        </h3>
                                        <ul class="mega-menu-list">
                                            <li v-for="child in c.children" :key="child.id">
                                                <router-link :to="{ name: 'products', params: { slug: child.slug } }"
                                                    class="text-dark menu-link">{{ child.name
                                                    }}</router-link>
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </li>

                        <li class="nav-item position-relative mr-3">
                            <a href="#"
                                class="nav-link text-dark text-decoration-none font-weight-bold d-flex align-items-center py-2 menu-link text-danger font-weight-bold">
                                BIG SALE THÁNG 12
                            </a>
                        </li>

                        <li class="nav-item position-relative mr-3 has-dropdown" @mouseenter="activeMenu = 'collection'"
                            @mouseleave="activeMenu = null">
                            <a href="#"
                                class="nav-link text-dark text-decoration-none font-weight-bold d-flex align-items-center py-2 menu-link">
                                BỘ SƯU TẬP
                            </a>

                            <!-- Mega Menu Collection -->
                            <div class="position-absolute bg-white shadow-lg p-4 mt-2"
                                style="min-width: 900px; z-index: 1;" v-show="activeMenu === 'collection'">
                                <div class="mega-menu-content">
                                    <div class="mega-menu-column">
                                        <h3 class="small font-weight-bold mb-3 text-dark text-uppercase">THEO MÙA</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Xuân hè 2025</a></li>
                                            <li><a href="#">Thu đông 2024</a></li>
                                            <li><a href="#">Tết 2025</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="small font-weight-bold mb-3 text-dark text-uppercase">PHONG CÁCH</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Office wear</a></li>
                                            <li><a href="#">Street style</a></li>
                                            <li><a href="#">Vintage</a></li>
                                            <li><a href="#">Minimalist</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="small font-weight-bold mb-3 text-dark text-uppercase">ĐẶC BIỆT</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Limited Edition</a></li>
                                            <li><a href="#">Designer Collection</a></li>
                                            <li><a href="#">Exclusive</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </li>
                    </ul>

                    <!-- Logo -->
                    <router-link class="h3 font-weight-bold text-dark m-0 flex-grow-1" to="/">
                        <h3 class="text-black">IVYmoda</h3>
                    </router-link>

                    <!-- Right Actions -->
                    <div class="navbar-actions">
                        <!-- Search -->
                        <div class="position-relative" @focusin="showSearchSuggestions = true"
                            @focusout="showSearchSuggestions = false" tabindex="-1">
                            <input type="text" class="form-control rounded-pill cursor-pointer"
                                placeholder="Tìm kiếm sản phẩm..." v-model="searchQuery"
                                @focus="showSearchSuggestions = true" />
                            <button class="btn btn-link position-absolute bg-transparent border-0 text-muted"
                                style="right: 10px; top: 50%; transform: translateY(-50%);">
                                <i class="pi pi-search" />
                            </button>

                            <!-- Search Suggestions -->
                            <div class="position-absolute bg-white shadow-lg rounded p-3 mt-2"
                                style="top: calc(100% + 10px); max-height: 300px; min-width: 350px; overflow-y: auto;"
                                v-show="showSearchSuggestions">
                                <div class="suggestions-header">
                                    <h4>Tìm kiếm nhiều nhất</h4>
                                </div>
                                <div class="suggestions-tags">
                                    <Tag v-for="tag in popularSearches" :label="tag" />
                                </div>
                                <div class="suggestions-divider"></div>
                                <ul class="suggestions-list">
                                    <li v-for="product in filteredProducts" :key="product.id">
                                        <img :src="product.image" :alt="product.name">
                                        <div class="suggestion-info">
                                            <p class="suggestion-name">{{ product.name }}</p>
                                            <p class="suggestion-price">{{ formatPrice(product.price) }}</p>
                                        </div>
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <div class="dropdown" v-if="isAuth">
                            <a class="d-flex align-items-center dropdown-toggle" href="#" role="button"
                                id="avatarDropdown" data-toggle="dropdown">
                                <img :src="user?.avatar?.url || DEFAULT_AVATAR" alt="avatar"
                                    class="rounded-circle border"
                                    style="width: 38px; height: 38px; object-fit: cover;" />
                            </a>

                            <div class="dropdown-menu dropdown-menu-right mt-2 px-2" aria-labelledby="avatarDropdown">
                                <div class="user-info">
                                    <img :src="user?.avatar?.url || DEFAULT_AVATAR" alt="avatar"
                                        class="rounded-circle border">
                                    <div>
                                        <p class="user-name">{{ user?.name }}</p>
                                        <p class="user-email">{{ user?.email }}</p>
                                    </div>
                                </div>
                                <div class="dropdown-divider"></div>
                                <router-link to="/profile" class="dropdown-item">
                                    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"
                                        viewBox="0 0 24 24">
                                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                                        <circle cx="12" cy="7" r="4"></circle>
                                    </svg>
                                    Tài khoản của tôi
                                </router-link>
                                <router-link to="/orders" class="dropdown-item">
                                    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"
                                        viewBox="0 0 24 24">
                                        <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"></path>
                                        <line x1="3" y1="6" x2="21" y2="6"></line>
                                        <path d="M16 10a4 4 0 0 1-8 0"></path>
                                    </svg>
                                    Đơn hàng của tôi
                                </router-link>
                                <div class="dropdown-divider"></div>
                                <button class="dropdown-item" @click="logout">
                                    <i class="pi pi-sign-out"></i>
                                    Đăng xuất
                                </button>
                            </div>
                        </div>

                        <button v-else class="btn btn-primary" @click="$router.push('/auth/signin')">
                            Đăng nhập
                        </button>

                        <!-- Cart -->
                        <!-- <router-link to="/cart" class="position-relative rounded-circle border p-2 d-flex">
                            <i class="pi pi-shopping-cart" style="font-size: 20px;" />
                            <span class="cart-badge" v-if="cartCount > 0">{{ cartCount }}</span>
                        </router-link> -->
                        <CartDrawerButton/>
                    </div>
                </div>
            </div>
        </div>

        <!-- Mobile Navigation -->
        <div class="mobile-navbar d-lg-none py-3 px-3">
            <div class="d-flex align-items-center justify-content-between">
                <!-- Menu Button -->
                <button class="btn btn-link p-0 text-dark" @click="showMobileMenu = true">
                    <i class="pi pi-bars" style="font-size: 24px;"></i>
                </button>

                <!-- Logo -->
                <router-link class="mobile-logo font-weight-bold text-dark text-decoration-none" to="/">
                    <h4 class="m-0">IVYmoda</h4>
                </router-link>

                <!-- Right Actions -->
                <div class="d-flex align-items-center gap-3">
                    <button class="btn btn-link p-0 text-dark" @click="showMobileSearch = true">
                        <i class="pi pi-search" style="font-size: 20px;"></i>
                    </button>
                    <CartDrawerButton/>
                </div>
            </div>
        </div>

        <!-- Mobile Search Overlay -->
        <Teleport to="body">
            <div v-if="showMobileSearch" class="mobile-search-overlay" @click.self="showMobileSearch = false">
                <div class="mobile-search-content">
                    <div class="d-flex align-items-center p-3 border-bottom">
                        <button class="btn btn-link p-0 text-dark mr-3" @click="showMobileSearch = false">
                            <i class="pi pi-arrow-left" style="font-size: 20px;"></i>
                        </button>
                        <input type="text" class="form-control border-0" placeholder="Tìm kiếm sản phẩm..."
                            v-model="searchQuery" autofocus />
                    </div>

                    <div class="p-3">
                        <div class="mb-3">
                            <h6 class="text-muted mb-2">Tìm kiếm nhiều nhất</h6>
                            <div class="d-flex flex-wrap gap-2">
                                <Tag v-for="tag in popularSearches" :label="tag" />
                            </div>
                        </div>

                        <div v-if="filteredProducts.length > 0">
                            <h6 class="text-muted mb-2">Gợi ý sản phẩm</h6>
                            <div class="suggested-products">
                                <div class="suggested-product" v-for="product in filteredProducts" :key="product.id">
                                    <img :src="product.image" :alt="product.name">
                                    <div class="flex-grow-1">
                                        <p class="mb-1 font-weight-medium">{{ product.name }}</p>
                                        <p class="text-danger font-weight-bold mb-0">{{ formatPrice(product.price) }}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </Teleport>

        <!-- Mobile Menu Sidebar -->
        <Teleport to="body">
            <div v-if="showMobileMenu" class="mobile-menu-overlay" @click.self="showMobileMenu = false">
                <div class="mobile-menu-sidebar">
                    <!-- Header -->
                    <div class="mobile-menu-header">
                        <router-link to="/" class="font-weight-bold text-dark text-decoration-none">
                            <h4 class="m-0">IVYmoda</h4>
                        </router-link>
                        <button class="btn btn-link p-0 text-dark" @click="showMobileMenu = false">
                            <i class="pi pi-times" style="font-size: 20px;"></i>
                        </button>
                    </div>

                    <!-- User Section -->
                    <div class="mobile-menu-user" v-if="isAuth">
                        <img :src="user?.avatar?.url || DEFAULT_AVATAR" alt="avatar">
                        <div>
                            <p class="font-weight-bold mb-0">{{ user?.name }}</p>
                            <p class="text-muted small mb-0">{{ user?.email }}</p>
                        </div>
                    </div>
                    <div v-else class="mobile-menu-user">
                        <button class="btn btn-primary btn-block" @click="$router.push('/auth/signin')">
                            Đăng nhập
                        </button>
                    </div>

                    <!-- Menu Items -->
                    <div class="mobile-menu-items">
                        <!-- Female Category -->
                        <div class="mobile-menu-item">
                            <button class="mobile-menu-title" @click="toggleMobileSubmenu('female')">
                                <span>NỮ</span>
                                <i
                                    :class="['pi', mobileCategoryOpen === 'female' ? 'pi-chevron-up' : 'pi-chevron-down']"></i>
                            </button>
                            <div v-show="mobileCategoryOpen === 'female'" class="mobile-submenu">
                                <div v-for="c in femaleCategories" :key="c.id" class="mobile-submenu-group">
                                    <h6 class="mobile-submenu-title"><router-link
                                            :to="{ name: 'products', params: { slug: c.slug } }"
                                            class="text-dark menu-link">{{ c.name
                                            }}</router-link></h6>
                                    <router-link :to="{ name: 'products', params: { slug: child.slug } }"
                                        class="text-dark menu-link mobile-submenu-link" v-for="child in c.children"
                                        :key="child.id">{{ child.name
                                        }}</router-link>
                                </div>
                            </div>
                        </div>

                        <!-- Male Category -->
                        <div class="mobile-menu-item">
                            <button class="mobile-menu-title" @click="toggleMobileSubmenu('male')">
                                <span>NAM</span>
                                <i
                                    :class="['pi', mobileCategoryOpen === 'male' ? 'pi-chevron-up' : 'pi-chevron-down']"></i>
                            </button>
                            <div v-show="mobileCategoryOpen === 'male'" class="mobile-submenu">
                                <div v-for="c in maleCategories" :key="c.id" class="mobile-submenu-group">
                                    <h6 class="mobile-submenu-title">{{ c.name }}</h6>
                                    <a v-for="child in c.children" :key="child.id" href="#" class="mobile-submenu-link">
                                        {{ child.name }}
                                    </a>
                                </div>
                            </div>
                        </div>

                        <!-- Sale -->
                        <div class="mobile-menu-item">
                            <a href="#" class="mobile-menu-title text-danger">
                                <span>🔥 BIG SALE THÁNG 12</span>
                            </a>
                        </div>

                        <!-- Collection -->
                        <div class="mobile-menu-item">
                            <button class="mobile-menu-title" @click="toggleMobileSubmenu('collection')">
                                <span>BỘ SƯU TẬP</span>
                                <i
                                    :class="['pi', mobileCategoryOpen === 'collection' ? 'pi-chevron-up' : 'pi-chevron-down']"></i>
                            </button>
                            <div v-show="mobileCategoryOpen === 'collection'" class="mobile-submenu px-3">
                                <a href="#" class="mobile-submenu-link menu-link">Xuân hè 2025</a>
                                <a href="#" class="mobile-submenu-link menu-link">Thu đông 2024</a>
                                <a href="#" class="mobile-submenu-link menu-link">Tết 2025</a>
                            </div>
                        </div>
                    </div>

                    <!-- Footer Actions -->
                    <div class="py-2" v-if="isAuth">
                        <router-link to="/profile" class="dropdown-item py-2">
                            <i class="pi pi-user"></i>
                            Tài khoản của tôi
                        </router-link>
                        <router-link to="/orders" class="dropdown-item py-2">
                            <i class="pi pi-shopping-bag"></i>
                            Đơn hàng của tôi
                        </router-link>
                        <button class="dropdown-item py-2" @click="logout">
                            <i class="pi pi-sign-out"></i>
                            Đăng xuất
                        </button>
                    </div>

                    <!-- Contact Info -->
                    <div class="mobile-menu-contact">
                        <a href="tel:0901234567" class="d-flex align-items-center text-dark text-decoration-none">
                            <i class="pi pi-phone mr-2"></i>
                            <span>Hotline: 0901 234 567</span>
                        </a>
                    </div>
                </div>
            </div>
        </Teleport>
    </nav>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuth } from "@/composables/useAuth";
import { useAuthStore } from "@/stores/auth.store";
import { useUserStore } from "@/stores/user.store";
import { DEFAULT_AVATAR } from "@/utils/constants";
import { storeToRefs } from "pinia";
import { formatPrice } from '@/utils/format';
import { useCategory } from '@/composables/useCategory';
import { useCategoryStore } from '@/stores/category.store';
import { GenderEnum } from '@/types/common';
import Tag from './Tag.vue';
import CartDrawerButton from './CartDrawerButton.vue';

// Stores
const userStore = useUserStore();
const { user } = storeToRefs(userStore);
const authStore = useAuthStore();
const { isAuth } = storeToRefs(authStore);
const { getCategories } = useCategory()
const categoryStore = useCategoryStore()
const { logout } = useAuth();

// State
const activeMenu = ref<string | null>(null);
const showSearchSuggestions = ref(false);
const searchQuery = ref('');
const showMobileMenu = ref(false);
const showMobileSearch = ref(false);
const mobileCategoryOpen = ref<string | null>(null);

// Search suggestions data
const popularSearches = ref([
    'Đầm', 'trẻ vai', 'Áo khoác', 'Quần', 'Áo sơ mi',
    'Vest', 'parka', 'tweed', 'croptop', 'Chân váy', 'lông cừu'
]);

const suggestedProducts = ref([
    { id: 1, name: 'Áo sơ mi trắng Oxford', price: 450000, image: 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=100&h=100&fit=crop' },
    { id: 2, name: 'Váy midi hoa nhí', price: 550000, image: 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=100&h=100&fit=crop' },
    { id: 3, name: 'Quần jean slim fit', price: 680000, image: 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=100&h=100&fit=crop' },
]);

// Computed
const filteredProducts = computed(() => {
    if (!searchQuery.value) return suggestedProducts.value;
    return suggestedProducts.value.filter(p =>
        p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

const maleCategories = computed(() =>
    categoryStore.categoriesByGender(GenderEnum.MALE)
)

const femaleCategories = computed(() => categoryStore.categoriesByGender(GenderEnum.FEMALE))

// Methods
const toggleMobileSubmenu = (category: string) => {
    mobileCategoryOpen.value = mobileCategoryOpen.value === category ? null : category;
};

const init = async () => {
    await getCategories({
        page: 1,
        limit: 100,
        parent_only: true
    })
}

init()
</script>

<style scoped>
/* Desktop Menu */
.menu-link:hover {
    color: #e63946 !important;
}

.mega-menu-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 30px;
}

.mega-menu-wrapper {
    min-width: 700px;
    z-index: 1;
}

@media (max-width: 768px) {
    .mega-menu-wrapper {
        min-width: 350px;
    }
}

.mega-menu-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.mega-menu-list li {
    margin-bottom: 10px;
}

.mega-menu-list a {
    color: #666;
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.3s;
}

.mega-menu-list a:hover {
    color: #e63946;
}

.has-dropdown::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    height: 10px;
}

.navbar-actions {
    display: flex;
    align-items: center;
    gap: 15px;
}

/* Search Suggestions */
.suggestions-header h4 {
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: #666;
}

.suggestions-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 15px;
}

.suggestions-divider {
    height: 1px;
    background: #eee;
    margin: 15px 0;
}

.suggestions-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.suggestions-list li {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
    cursor: pointer;
    border-radius: 6px;
    transition: background 0.3s;
}

.suggestions-list li:hover {
    background: #f8f8f8;
}

.suggestions-list img {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 6px;
}

.suggestion-info {
    flex: 1;
}

.suggestion-name {
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 4px;
}

.suggestion-price {
    font-size: 0.85rem;
    color: #e63946;
    font-weight: 600;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.cart-badge {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #e63946;
    color: white;
    font-size: 0.7rem;
    font-weight: 600;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.user-dropdown {
    position: absolute;
    top: calc(100% + 10px);
    right: 0;
    background: white;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    border-radius: 8px;
    padding: 15px;
    min-width: 280px;
    z-index: 100;
}

.user-info {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px;
}

.user-info img {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
}

.user-name {
    font-weight: 600;
    margin-bottom: 4px;
}

.user-email {
    font-size: 0.85rem;
    color: #666;
}

/* ========== MOBILE NAVBAR ========== */
.mobile-navbar {
    position: sticky;
    top: 0;
    z-index: 1030;
    background: #fff;
    border-bottom: 1px solid #eee;
}

.mobile-logo h4 {
    font-weight: 700;
    letter-spacing: 1px;
}

/* ========== SEARCH OVERLAY ========== */
.mobile-search-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 2000;
}

.mobile-search-content {
    background: #fff;
    height: 100%;
    overflow-y: auto;
}

/* Suggested products */
.suggested-products {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.suggested-product {
    display: flex;
    gap: 12px;
    align-items: center;
}

.suggested-product img {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 6px;
}

/* ========== MENU OVERLAY ========== */
.mobile-menu-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 2000;
}

/* Sidebar */
.mobile-menu-sidebar {
    width: 85%;
    max-width: 320px;
    height: 100%;
    background: #fff;
    overflow-y: auto;
    animation: slideInLeft 0.3s ease;
}

/* Slide animation */
@keyframes slideInLeft {
    from {
        transform: translateX(-100%);
    }

    to {
        transform: translateX(0);
    }
}

/* Header */
.mobile-menu-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px;
    border-bottom: 1px solid #eee;
}

/* User section */
.mobile-menu-user {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    border-bottom: 1px solid #eee;
}

.mobile-menu-user img {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    object-fit: cover;
}

/* ========== MENU ITEMS ========== */
.mobile-menu-items {
    padding: 8px 0;
}

.mobile-menu-item {
    border-bottom: 1px solid #f1f1f1;
}

.mobile-menu-title {
    width: 100%;
    background: none;
    border: none;
    padding: 12px 16px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
    font-size: 15px;
    cursor: pointer;
}

/* Submenu */
.mobile-submenu {
    background: #fafafa;
    padding: 8px 0;
}

.mobile-submenu-group {
    padding: 8px 16px;
}

.mobile-submenu-title {
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 6px;
    text-transform: uppercase;
}

.mobile-submenu-link {
    display: block;
    padding: 6px 0;
    font-size: 14px;
    color: #333;
    text-decoration: none;
}

/* Hover / active */
.mobile-submenu-link:active {
    color: #000;
}

/* ========== CONTACT ========== */
.mobile-menu-contact {
    padding: 16px;
    border-top: 1px solid #eee;
    font-size: 14px;
}
</style>