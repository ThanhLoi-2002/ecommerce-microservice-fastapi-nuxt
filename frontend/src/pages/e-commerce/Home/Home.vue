// HomePage.vue
<template>
  <div class="home-page">
    <!-- Hero Slider -->
    <div class="hero-slider">
      <div class="slider-container">
        <div class="slider-track" :style="{ transform: `translateX(-${currentSlide * 100}%)` }">
          <div v-for="(slide, index) in sliders" :key="index" class="slide"
            :style="{ backgroundImage: `url(${slide.image})` }">
            <div class="slide-content">
              <h1 class="slide-title">{{ slide.title }}</h1>
              <p class="slide-subtitle">{{ slide.subtitle }}</p>
              <button class="btn-shop-now">{{ slide.btnText }}</button>
            </div>
          </div>
        </div>

        <!-- Navigation Dots -->
        <div class="slider-dots">
          <span v-for="(slide, index) in sliders" :key="index" class="dot" :class="{ active: currentSlide === index }"
            @click="goToSlide(index)"></span>
        </div>

        <!-- Navigation Arrows -->
        <button class="slider-arrow prev" @click="prevSlide">‹</button>
        <button class="slider-arrow next" @click="nextSlide">›</button>
      </div>
    </div>

    <!-- Categories Banner -->
    <section class="categories-banner">
      <div class="container">
        <div class="row g-3">
          <div class="col-md-4" v-for="cat in categoryBanners" :key="cat.id">
            <div class="category-card" @click="goToCategory(cat.slug)">
              <img :src="cat.image" :alt="cat.name">
              <div class="category-overlay">
                <h3>{{ cat.name }}</h3>
                <p>{{ cat.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Best Sellers with Gender Tabs -->
    <section class="best-sellers">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Sản phẩm bán chạy</h2>
          <div class="gender-tabs">
            <button v-for="tab in genderTabs" :key="tab.id" class="tab-btn" :class="{ active: activeTab === tab.id }"
              @click="activeTab = tab.id">
              {{ tab.label }}
            </button>
          </div>
        </div>

        <div class="products-grid">
          <div class="product-item" v-for="product in filteredProducts" :key="product.id"
            @click="viewProduct(product.id)">
            <div class="product-image">
              <img :src="product.image" :alt="product.name">
              <div class="product-badge" v-if="product.discount">
                -{{ product.discount }}%
              </div>
              <div class="product-actions">
                <button class="action-btn" title="Yêu thích">
                  <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path
                      d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                    </path>
                  </svg>
                </button>
                <button class="action-btn" title="Xem nhanh">
                  <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </button>
              </div>
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <div class="product-price">
                <span class="price-current">{{ formatPrice(product.price) }}</span>
                <span class="price-old" v-if="product.oldPrice">{{ formatPrice(product.oldPrice) }}</span>
              </div>
              <div class="product-colors">
                <span v-for="color in product.colors" :key="color" class="color-dot"
                  :style="{ backgroundColor: color }"></span>
              </div>
            </div>
          </div>
        </div>

        <div class="text-center mt-4">
          <button class="btn-view-more">Xem thêm sản phẩm</button>
        </div>
      </div>
    </section>

    <!-- New Arrivals -->
    <section class="new-arrivals bg-light">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Hàng mới về</h2>
          <a href="#" class="view-all-link">Xem tất cả →</a>
        </div>

        <div class="products-grid">
          <div class="product-item" v-for="product in newProducts.slice(0, 8)" :key="product.id"
            @click="viewProduct(product.id)">
            <div class="product-image">
              <img :src="product.image" :alt="product.name">
              <div class="product-badge new">NEW</div>
              <div class="product-actions">
                <button class="action-btn" title="Yêu thích">
                  <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path
                      d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z">
                    </path>
                  </svg>
                </button>
                <button class="action-btn" title="Xem nhanh">
                  <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                    <circle cx="12" cy="12" r="3"></circle>
                  </svg>
                </button>
              </div>
            </div>
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <div class="product-price">
                <span class="price-current">{{ formatPrice(product.price) }}</span>
              </div>
              <div class="product-colors">
                <span v-for="color in product.colors" :key="color" class="color-dot"
                  :style="{ backgroundColor: color }"></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Fashion Blog/Lookbook -->
    <section class="lookbook">
      <div class="container">
        <div class="section-header">
          <h2 class="section-title">Lookbook</h2>
        </div>
        <div class="lookbook-grid">
          <div class="lookbook-item large">
            <img src="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=800&h=1000&fit=crop"
              alt="Lookbook">
            <div class="lookbook-content">
              <h3>Summer Collection</h3>
              <button class="btn-explore">Khám phá</button>
            </div>
          </div>
          <div class="lookbook-item">
            <img src="https://images.unsplash.com/photo-1483985988355-763728e1935b?w=400&h=500&fit=crop" alt="Lookbook">
            <div class="lookbook-content">
              <h3>Street Style</h3>
              <button class="btn-explore">Khám phá</button>
            </div>
          </div>
          <div class="lookbook-item">
            <img src="https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400&h=500&fit=crop" alt="Lookbook">
            <div class="lookbook-content">
              <h3>Office Look</h3>
              <button class="btn-explore">Khám phá</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter -->
    <section class="newsletter">
      <div class="container">
        <div class="newsletter-box">
          <h2>Đăng ký nhận tin</h2>
          <p>Nhận thông tin về sản phẩm mới và ưu đãi độc quyền</p>
          <form class="newsletter-form" @submit.prevent="subscribe">
            <input type="email" placeholder="Nhập email của bạn" required>
            <button type="submit">Đăng ký</button>
          </form>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';

interface Product {
  id: number;
  name: string;
  price: number;
  oldPrice?: number;
  discount?: number;
  image: string;
  colors: string[];
  gender: 'male' | 'female' | 'unisex';
}

// Slider State
const currentSlide = ref(0);
const sliders = [
  {
    image: 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=1920&h=800&fit=crop',
    title: 'NEW COLLECTION 2025',
    subtitle: 'Khám phá phong cách thời trang mới nhất',
    btnText: 'Mua ngay'
  },
  {
    image: 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=1920&h=800&fit=crop',
    title: 'WINTER SALE 50%',
    subtitle: 'Giảm giá lên đến 50% toàn bộ bộ sưu tập',
    btnText: 'Khám phá'
  },
  {
    image: 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1920&h=800&fit=crop',
    title: 'TRENDY OUTFITS',
    subtitle: 'Phong cách hiện đại cho giới trẻ',
    btnText: 'Xem ngay'
  }
];

const categoryBanners = [
  {
    id: 1,
    name: 'Nam',
    slug: 'nam',
    description: 'Thời trang nam hiện đại',
    image: 'https://images.unsplash.com/photo-1617127365659-c47fa864d8bc?w=600&h=400&fit=crop'
  },
  {
    id: 2,
    name: 'Nữ',
    slug: 'nu',
    description: 'Thời trang nữ thanh lịch',
    image: 'https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=600&h=400&fit=crop'
  },
  {
    id: 3,
    name: 'Phụ kiện',
    slug: 'phu-kien',
    description: 'Hoàn thiện phong cách',
    image: 'https://images.unsplash.com/photo-1606760227091-3dd870d97f1d?w=600&h=400&fit=crop'
  }
];

// Gender Tabs
const activeTab = ref('all');
const genderTabs = [
  { id: 'all', label: 'Tất cả' },
  { id: 'male', label: 'Nam' },
  { id: 'female', label: 'Nữ' }
];

// Products Data
const products = ref<Product[]>([
  { id: 1, name: 'Áo sơ mi Oxford trắng', price: 450000, oldPrice: 650000, discount: 30, image: 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400&h=500&fit=crop', colors: ['#fff', '#000', '#1e90ff'], gender: 'male' },
  { id: 2, name: 'Váy midi hoa nhí', price: 550000, image: 'https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400&h=500&fit=crop', colors: ['#ff69b4', '#fff', '#000'], gender: 'female' },
  { id: 3, name: 'Quần jean slim fit', price: 680000, oldPrice: 850000, discount: 20, image: 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=500&fit=crop', colors: ['#1e90ff', '#000'], gender: 'male' },
  { id: 4, name: 'Áo blazer nữ', price: 890000, image: 'https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=400&h=500&fit=crop', colors: ['#000', '#c0c0c0', '#fff'], gender: 'female' },
  { id: 5, name: 'Hoodie oversize', price: 420000, image: 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400&h=500&fit=crop', colors: ['#000', '#808080', '#fff'], gender: 'unisex' },
  { id: 6, name: 'Chân váy xếp ly', price: 380000, oldPrice: 500000, discount: 24, image: 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400&h=500&fit=crop', colors: ['#000', '#ff1493'], gender: 'female' },
  { id: 7, name: 'Áo polo nam', price: 320000, image: 'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400&h=500&fit=crop', colors: ['#000', '#fff', '#1e90ff'], gender: 'male' },
  { id: 8, name: 'Đầm maxi dự tiệc', price: 1200000, image: 'https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=400&h=500&fit=crop', colors: ['#ff0000', '#000', '#0000ff'], gender: 'female' },
]);

const newProducts = ref<Product[]>([
  { id: 9, name: 'Áo thun basic', price: 180000, image: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=500&fit=crop', colors: ['#fff', '#000', '#808080'], gender: 'unisex' },
  { id: 10, name: 'Quần tây ống rộng', price: 590000, image: 'https://images.unsplash.com/photo-1594633313593-bab3825d0caf?w=400&h=500&fit=crop', colors: ['#000', '#c0c0c0'], gender: 'female' },
  { id: 11, name: 'Áo khoác denim', price: 750000, image: 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&h=500&fit=crop', colors: ['#1e90ff', '#000'], gender: 'unisex' },
  { id: 12, name: 'Set đồ công sở', price: 950000, image: 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400&h=500&fit=crop', colors: ['#000', '#fff', '#808080'], gender: 'female' },
  { id: 13, name: 'Quần short kaki', price: 280000, image: 'https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=400&h=500&fit=crop', colors: ['#8b4513', '#000', '#808080'], gender: 'male' },
  { id: 14, name: 'Áo cardigan len', price: 480000, image: 'https://images.unsplash.com/photo-1434389677669-e08b4cac3105?w=400&h=500&fit=crop', colors: ['#f5deb3', '#000', '#ff69b4'], gender: 'female' },
  { id: 15, name: 'Quần jogger', price: 390000, image: 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400&h=500&fit=crop', colors: ['#000', '#808080', '#1e90ff'], gender: 'unisex' },
  { id: 16, name: 'Áo croptop', price: 220000, image: 'https://images.unsplash.com/photo-1564859228273-274232fdb516?w=400&h=500&fit=crop', colors: ['#fff', '#000', '#ff1493'], gender: 'female' },
]);

// Computed
const filteredProducts = computed(() => {
  if (activeTab.value === 'all') return products.value;
  if (activeTab.value === 'male') return products.value.filter(p => p.gender === 'male' || p.gender === 'unisex');
  if (activeTab.value === 'female') return products.value.filter(p => p.gender === 'female' || p.gender === 'unisex');
  return products.value;
});

// Methods
const formatPrice = (price: number): string => {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(price);
};

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % sliders.length;
};

const prevSlide = () => {
  currentSlide.value = currentSlide.value === 0 ? sliders.length - 1 : currentSlide.value - 1;
};

const goToSlide = (index: number) => {
  currentSlide.value = index;
};

const viewProduct = (id: number) => {
  console.log('View product:', id);
  // Router navigation
};

const goToCategory = (slug: string) => {
  console.log('Go to category:', slug);
};

const subscribe = () => {
  alert('Đăng ký thành công!');
};

// Auto slider
let sliderInterval: any;
onMounted(() => {
  sliderInterval = setInterval(nextSlide, 5000);
});

onUnmounted(() => {
  clearInterval(sliderInterval);
});
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.home-page {
  width: 100%;
  overflow-x: hidden;
}

/* Hero Slider */
.hero-slider {
  width: 100%;
  height: 600px;
  position: relative;
  overflow: hidden;
  margin-bottom: 50px;
}

.slider-container {
  width: 100%;
  height: 100%;
  position: relative;
}

.slider-track {
  display: flex;
  height: 100%;
  transition: transform 0.5s ease-in-out;
}

.slide {
  min-width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slide::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
}

.slide-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
  max-width: 600px;
  padding: 20px;
}

.slide-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.slide-subtitle {
  font-size: 1.5rem;
  margin-bottom: 30px;
}

.btn-shop-now {
  padding: 15px 50px;
  font-size: 1.1rem;
  font-weight: 600;
  background: white;
  color: #000;
  border: none;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-shop-now:hover {
  background: #000;
  color: white;
  transform: translateY(-2px);
}

.slider-dots {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
  z-index: 2;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  transition: all 0.3s;
}

.dot.active {
  background: white;
  width: 30px;
  border-radius: 6px;
}

.slider-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.8);
  border: none;
  width: 50px;
  height: 50px;
  font-size: 2rem;
  cursor: pointer;
  z-index: 2;
  transition: all 0.3s;
}

.slider-arrow:hover {
  background: white;
}

.slider-arrow.prev {
  left: 20px;
}

.slider-arrow.next {
  right: 20px;
}

/* Categories Banner */
.categories-banner {
  padding: 50px 0;
}

.category-card {
  position: relative;
  height: 300px;
  overflow: hidden;
  cursor: pointer;
  border-radius: 8px;
}

.category-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.category-card:hover img {
  transform: scale(1.1);
}

.category-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 30px;
  color: white;
}

.category-overlay h3 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.category-overlay p {
  font-size: 1.1rem;
}

/* Best Sellers Section */
.best-sellers {
  padding: 80px 0;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.gender-tabs {
  display: flex;
  gap: 10px;
}

.tab-btn {
  padding: 10px 30px;
  border: 2px solid #ddd;
  background: white;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
}

.tab-btn:hover {
  border-color: #000;
}

.tab-btn.active {
  background: #000;
  color: white;
  border-color: #000;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.product-item {
  cursor: pointer;
  transition: transform 0.3s;
}

.product-item:hover {
  transform: translateY(-5px);
}

.product-image {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  margin-bottom: 15px;
  aspect-ratio: 3/4;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.product-item:hover .product-image img {
  transform: scale(1.05);
}

.product-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #ff0000;
  color: white;
  padding: 5px 15px;
  font-weight: 700;
  font-size: 0.9rem;
  border-radius: 4px;
}

.product-badge.new {
  background: #28a745;
}

.product-actions {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  gap: 10px;
  opacity: 0;
  transition: opacity 0.3s;
}

.product-item:hover .product-actions {
  opacity: 1;
}

.action-btn {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  background: #000;
  color: white;
}

.product-info {
  padding: 0 5px;
}

.product-name {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 10px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.price-current {
  font-size: 1.2rem;
  font-weight: 700;
  color: #000;
}

.price-old {
  font-size: 1rem;
  color: #999;
  text-decoration: line-through;
}

.product-colors {
  display: flex;
  gap: 8px;
}

.color-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #ddd;
  cursor: pointer;
}

.btn-view-more {
  padding: 12px 40px;
  background: #000;
  color: white;
  border: 2px solid #000;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-view-more:hover {
  background: white;
  color: #000;
}

/* New Arrivals */
.new-arrivals {
  padding: 80px 0;
}

.view-all-link {
  color: #000;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.view-all-link:hover {
  text-decoration: underline;
}

/* Lookbook */
.lookbook {
  padding: 80px 0;
}

.lookbook-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.lookbook-item {
  position: relative;
  height: 400px;
  overflow: hidden;
  border-radius: 8px;
  cursor: pointer;
}

.lookbook-item.large {
  grid-row: span 2;
  height: 820px;
}

.lookbook-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s;
}

.lookbook-item:hover img {
  transform: scale(1.1);
}

.lookbook-content {
  position: absolute;
  bottom: 30px;
  left: 30px;
  color: white;
}

.lookbook-content h3 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.btn-explore {
  padding: 10px 30px;
  background: white;
  color: #000;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-explore:hover {
  background: #000;
  color: white;
}

/* Newsletter */
.newsletter {
  padding: 80px 0;
  background: #f8f9fa;
}

.newsletter-box {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.newsletter-box h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.newsletter-box p {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 30px;
}

.newsletter-form {
  display: flex;
  gap: 10px;
  max-width: 500px;
  margin: 0 auto;
}

.newsletter-form input {
  flex: 1;
  padding: 15px 20px;
  border: 2px solid #ddd;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.3s;
}

.newsletter-form input:focus {
  border-color: #000;
}

.newsletter-form button {
  padding: 15px 35px;
  background: #000;
  color: white;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.newsletter-form button:hover {
  background: #333;
}

/* Container */
.container {
  max-width: 1320px;
  margin: 0 auto;
  padding: 0 20px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -15px;
}

.g-3>* {
  padding: 15px;
}

.col-md-4 {
  flex: 0 0 33.333%;
  max-width: 33.333%;
}

/* Responsive */
@media (max-width: 992px) {
  .slide-title {
    font-size: 2.5rem;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }

  .lookbook-grid {
    grid-template-columns: 1fr;
  }

  .lookbook-item.large {
    grid-row: span 1;
    height: 400px;
  }
}

@media (max-width: 768px) {
  .col-md-4 {
    flex: 0 0 100%;
    max-width: 100%;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .hero-slider {
    height: 400px;
  }

  .slide-title {
    font-size: 2rem;
  }

  .slider-arrow {
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }

  .newsletter-form {
    flex-direction: column;
  }
}
</style>