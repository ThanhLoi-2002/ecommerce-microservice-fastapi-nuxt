// Navbar.vue
<template>
    <nav class="main-navbar">
        <!-- Top Bar -->
        <div class="top-bar">
            <div class="px-5">
                <div class="top-bar-content">
                    <div class="top-bar-left">
                        <span class="text-sm">🔥 BIG SALE THÁNG 12 - GIẢM ĐẾN 50%</span>
                    </div>
                    <div class="top-bar-right">
                        <a href="tel:0901234567" class="text-sm">📞 Hotline: 0901 234 567</a>
                    </div>
                </div>
            </div>
        </div>

        <!-- Main Navigation -->
        <div class="navbar-main">
            <div class="px-5">
                <div class="navbar-content">
                    <!-- Logo -->
                    <router-link class="navbar-brand" to="/">
                        <h1 class="logo">IVYmoda</h1>
                    </router-link>

                    <!-- Main Menu -->
                    <ul class="navbar-menu">
                        <li class="menu-item has-dropdown" @mouseenter="activeMenu = 'female'"
                            @mouseleave="activeMenu = null">
                            <a href="#" class="menu-link">
                                NỮ
                                <svg width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                                    <path
                                        d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z" />
                                </svg>
                            </a>

                            <!-- Mega Menu Female -->
                            <div class="mega-menu" v-show="activeMenu === 'female'">
                                <div class="mega-menu-content">
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">ÁO</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Áo sơ mi</a></li>
                                            <li><a href="#">Áo thun</a></li>
                                            <li><a href="#">Áo croptop</a></li>
                                            <li><a href="#">Áo len</a></li>
                                            <li><a href="#">Áo vest/ blazer</a></li>
                                            <li><a href="#">Áo phao</a></li>
                                            <li><a href="#" class="text-danger">ĐỔ LỘT 50K -150K</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">ÁO KHOÁC</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#" class="text-danger">DẠ LÔNG CỰU | SALE off 50%</a></li>
                                            <li><a href="#">Áo da/ măng tô</a></li>
                                            <li><a href="#">Áo Gile</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">SET BỘ</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Set bộ công sở</a></li>
                                            <li><a href="#">Set bộ co-ords</a></li>
                                            <li><a href="#">Set bộ thun/ len</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">QUẦN & JUMPSUIT</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Quần dài</a></li>
                                            <li><a href="#">Quần jeans</a></li>
                                            <li><a href="#">Quần lửng/ short</a></li>
                                            <li><a href="#">Jumpsuit</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">CHÂN VÁY</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Chân váy bút chì</a></li>
                                            <li><a href="#">Chân váy chữ A</a></li>
                                            <li><a href="#">Chân váy jeans</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">ĐẦM/ ÁO DÀI</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Đầm công sở</a></li>
                                            <li><a href="#">Đầm voan hoa/ maxi</a></li>
                                            <li><a href="#">Đầm thun</a></li>
                                            <li><a href="#">ÁO DÀI</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </li>

                        <li class="menu-item has-dropdown" @mouseenter="activeMenu = 'male'"
                            @mouseleave="activeMenu = null">
                            <a href="#" class="menu-link">
                                NAM
                                <svg width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                                    <path
                                        d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z" />
                                </svg>
                            </a>

                            <!-- Mega Menu Male -->
                            <div class="mega-menu" v-show="activeMenu === 'male'">
                                <div class="mega-menu-content">
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">ÁO</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Áo sơ mi</a></li>
                                            <li><a href="#">Áo thun</a></li>
                                            <li><a href="#">Áo polo</a></li>
                                            <li><a href="#">Áo len</a></li>
                                            <li><a href="#">Áo vest</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">ÁO KHOÁC</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Áo khoác jean</a></li>
                                            <li><a href="#">Áo khoác da</a></li>
                                            <li><a href="#">Áo hoodie</a></li>
                                            <li><a href="#">Áo blazer</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">QUẦN</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Quần jean</a></li>
                                            <li><a href="#">Quần kaki</a></li>
                                            <li><a href="#">Quần tây</a></li>
                                            <li><a href="#">Quần short</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">PHỤ KIỆN</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Cà vạt</a></li>
                                            <li><a href="#">Thắt lưng</a></li>
                                            <li><a href="#">Ví nam</a></li>
                                            <li><a href="#">Tất/ vớ</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </li>

                        <li class="menu-item">
                            <a href="#" class="menu-link text-danger font-weight-bold">BIG SALE THÁNG 12</a>
                        </li>

                        <li class="menu-item has-dropdown" @mouseenter="activeMenu = 'collection'"
                            @mouseleave="activeMenu = null">
                            <a href="#" class="menu-link">
                                BỘ SƯU TẬP
                                <svg width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                                    <path
                                        d="M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z" />
                                </svg>
                            </a>

                            <!-- Mega Menu Collection -->
                            <div class="mega-menu" v-show="activeMenu === 'collection'">
                                <div class="mega-menu-content">
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">THEO MÙA</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Xuân hè 2025</a></li>
                                            <li><a href="#">Thu đông 2024</a></li>
                                            <li><a href="#">Tết 2025</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">PHONG CÁCH</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Office wear</a></li>
                                            <li><a href="#">Street style</a></li>
                                            <li><a href="#">Vintage</a></li>
                                            <li><a href="#">Minimalist</a></li>
                                        </ul>
                                    </div>
                                    <div class="mega-menu-column">
                                        <h3 class="mega-menu-title">ĐẶC BIỆT</h3>
                                        <ul class="mega-menu-list">
                                            <li><a href="#">Limited Edition</a></li>
                                            <li><a href="#">Designer Collection</a></li>
                                            <li><a href="#">Exclusive</a></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </li>

                        <li class="menu-item">
                            <a href="#" class="menu-link">VỀ CHÚNG TÔI</a>
                        </li>
                    </ul>

                    <!-- Right Actions -->
                    <div class="navbar-actions">
                        <!-- Search -->
                        <div class="search-box" @mouseenter="showSearchSuggestions = true"
                            @mouseleave="showSearchSuggestions = false">
                            <input type="text" class="search-input" placeholder="Tìm kiếm sản phẩm..."
                                v-model="searchQuery" @focus="showSearchSuggestions = true" />
                            <button class="search-btn">
                                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"
                                    viewBox="0 0 24 24">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <path d="m21 21-4.35-4.35"></path>
                                </svg>
                            </button>

                            <!-- Search Suggestions -->
                            <div class="search-suggestions" v-show="showSearchSuggestions && searchQuery.length > 0">
                                <div class="suggestions-header">
                                    <h4>Tìm kiếm nhiều nhất</h4>
                                </div>
                                <div class="suggestions-tags">
                                    <span class="suggestion-tag" v-for="tag in popularSearches" :key="tag">
                                        {{ tag }}
                                    </span>
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

                        <!-- Hotline -->
                        <button class="icon-btn" title="Hotline">
                            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"
                                viewBox="0 0 24 24">
                                <path
                                    d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z">
                                </path>
                            </svg>
                        </button>

                        <!-- User Account -->
                        <div class="user-menu" v-if="isAuth">
                            <button class="icon-btn user-btn" @click="toggleUserMenu">
                                <img :src="user?.avatar?.url || DEFAULT_AVATAR" alt="avatar" class="user-avatar" />
                            </button>

                            <div class="user-dropdown" v-show="showUserMenu">
                                <div class="user-info">
                                    <img :src="user?.avatar?.url || DEFAULT_AVATAR" alt="avatar">
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
                                    <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"
                                        viewBox="0 0 24 24">
                                        <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                                        <polyline points="16 17 21 12 16 7"></polyline>
                                        <line x1="21" y1="12" x2="9" y2="12"></line>
                                    </svg>
                                    Đăng xuất
                                </button>
                            </div>
                        </div>
                        <button v-else class="btn-login" @click="$router.push('/auth/signin')">
                            Đăng nhập
                        </button>

                        <!-- Cart -->
                        <router-link to="/cart" class="icon-btn cart-btn">
                            <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"
                                viewBox="0 0 24 24">
                                <circle cx="9" cy="21" r="1"></circle>
                                <circle cx="20" cy="21" r="1"></circle>
                                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
                            </svg>
                            <span class="cart-badge" v-if="cartCount > 0">{{ cartCount }}</span>
                        </router-link>
                    </div>
                </div>
            </div>
        </div>
    </nav>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuth } from "@/composables/useAuth";
import { useAuthStore } from "@/stores/auth.store";
import { useUserStore } from "@/stores/user.store";
import { DEFAULT_AVATAR } from "@/utils/constants";
import { storeToRefs } from "pinia";

// Stores
const userStore = useUserStore();
const { user, isLoading } = storeToRefs(userStore);
const authStore = useAuthStore();
const { isAuth } = storeToRefs(authStore);
const { logout } = useAuth();

// State
const activeMenu = ref<string | null>(null);
const showSearchSuggestions = ref(false);
const showUserMenu = ref(false);
const searchQuery = ref('');
const cartCount = ref(3);

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

// Methods
const formatPrice = (price: number): string => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
};

const toggleUserMenu = () => {
    showUserMenu.value = !showUserMenu.value;
};
</script>

<style scoped>
.main-navbar {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Top Bar */
.top-bar {
    background: #000;
    color: white;
    padding: 8px 0;
    font-size: 0.85rem;
}

.top-bar-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.top-bar-left,
.top-bar-right {
    display: flex;
    gap: 20px;
}

.top-bar a {
    color: white;
    text-decoration: none;
}

.top-bar a:hover {
    text-decoration: underline;
}

/* Main Navbar */
.navbar-main {
    padding: 15px 0;
}

.navbar-content {
    display: flex;
    align-items: center;
    gap: 40px;
}

.navbar-brand {
    text-decoration: none;
}

.logo {
    font-size: 1.8rem;
    font-weight: 700;
    color: #000;
    margin: 0;
}

/* Menu */
.navbar-menu {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 35px;
    flex: 1;
}

.menu-item {
    position: relative;
}

.menu-link {
    color: #000;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
    display: flex;
    align-items: center;
    gap: 5px;
    padding: 8px 0;
    transition: color 0.3s;
}

.menu-link:hover {
    color: #e63946;
}

/* Mega Menu */
.mega-menu {
    position: absolute;
    top: 100%;
    left: -50px;
    background: white;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    padding: 30px;
    min-width: 900px;
    margin-top: 10px;
    z-index: 100;
}

.mega-menu-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 30px;
}

.mega-menu-title {
    font-size: 0.9rem;
    font-weight: 700;
    margin-bottom: 15px;
    color: #000;
    text-transform: uppercase;
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

/* Right Actions */
.navbar-actions {
    display: flex;
    align-items: center;
    gap: 15px;
}

/* Search Box */
.search-box {
    position: relative;
}

.search-input {
    width: 300px;
    padding: 10px 40px 10px 15px;
    border: 1px solid #ddd;
    border-radius: 25px;
    font-size: 0.9rem;
    outline: none;
    transition: border-color 0.3s;
}

.search-input:focus {
    border-color: #000;
}

.search-btn {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    color: #666;
}

/* Search Suggestions */
.search-suggestions {
    position: absolute;
    top: calc(100% + 10px);
    left: 0;
    right: 0;
    background: white;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
    border-radius: 8px;
    padding: 20px;
    max-height: 400px;
    overflow-y: auto;
    z-index: 100;
}

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

.suggestion-tag {
    padding: 6px 12px;
    background: #f0f0f0;
    border-radius: 15px;
    font-size: 0.85rem;
    cursor: pointer;
    transition: background 0.3s;
}

.suggestion-tag:hover {
    background: #e0e0e0;
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

/* Icon Buttons */
.icon-btn {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background: #f8f8f8;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    position: relative;
}

.icon-btn:hover {
    background: #e8e8e8;
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

/* User Dropdown */
.user-menu {
    position: relative;
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

.dropdown-divider {
    height: 1px;
    background: #eee;
    margin: 10px 0;
}

.dropdown-item {
    display: flex
}
</style>