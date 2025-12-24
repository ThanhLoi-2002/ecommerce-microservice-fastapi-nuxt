<template>
  <div style="background-color: #f8f9fa; min-height: 100vh; padding: 20px;">
    <div class="px-5" >
      <!-- Progress Bar -->
      <div class="mb-4">
        <div class="d-flex justify-content-between align-items-center" style="position: relative;">
          <div style="position: absolute; top: 12px; left: 0; right: 0; height: 2px; background-color: #dee2e6; z-index: 0;">
            <div style="width: 0%; height: 100%; background-color: #dc3545;"></div>
          </div>
          <div v-for="(step, idx) in steps" :key="idx" class="text-center" style="position: relative; z-index: 1; flex: 1;">
            <div
              class="mx-auto mb-2"
              :style="{
                width: '24px',
                height: '24px',
                borderRadius: '50%',
                backgroundColor: idx === 0 ? '#000' : '#fff',
                border: '2px solid #dee2e6',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }"
            >
              <div v-if="idx === 0" style="width: 12px; height: 12px; border-radius: 50%; background-color: #000;"></div>
            </div>
            <small :style="{ fontSize: '12px', color: idx === 0 ? '#000' : '#6c757d' }">{{ step }}</small>
          </div>
        </div>
      </div>

      <div class="row">
        <!-- Cart Items -->
        <div class="col-lg-8">
          <div class="bg-white rounded shadow-sm p-4 mb-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h5 class="mb-0">
                Giỏ hàng của bạn <span style="color: #dc3545;">{{ cartItems.length }} Sản Phẩm</span>
              </h5>
              <div class="form-check">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  :checked="isAllSelected"
                  @change="toggleSelectAll"
                  id="selectAll"
                  style="cursor: pointer;"
                >
                <label class="form-check-label" for="selectAll" style="cursor: pointer; user-select: none;">
                  Chọn tất cả ({{ selectedCount }})
                </label>
              </div>
            </div>

            <!-- Table Header -->
            <div class="d-none d-md-flex border-bottom pb-2 mb-3" style="font-size: 14px; color: #6c757d; font-weight: 500;">
              <div style="width: 40%;">TÊN SẢN PHẨM</div>
              <div style="width: 20%;">CHIẾT KHẤU</div>
              <div style="width: 20%;">SỐ LƯỢNG</div>
              <div style="width: 20%;">TỔNG TIỀN</div>
            </div>

            <!-- Cart Items -->
            <div v-for="item in cartItems" :key="item.id" class="d-flex flex-column flex-md-row align-items-start align-items-md-center border-bottom py-3 gap-2">
              <!-- Checkbox -->
              <div class="d-flex align-items-center" style="margin-left: 10px">
                <input 
                  class="form-check-input" 
                  type="checkbox" 
                  :checked="item.selected"
                  @change="toggleSelectItem(item.id)"
                  :id="'item-' + item.id"
                  style="cursor: pointer; width: 20px; height: 20px;"
                >
              </div>

              <div class="d-flex align-items-start gap-2" style="width: 100%; max-width: 40%;">
                <img
                  :src="item.image"
                  :alt="item.name"
                  style="width: 100px; height: 130px; object-fit: cover; border-radius: 8px;"
                  class="me-3"
                />
                <div>
                  <h6 class="mb-2" style="font-size: 15px; font-weight: 500;">{{ item.name }}</h6>
                  <p class="mb-1" style="font-size: 13px; color: #6c757d;">
                    Màu sắc: {{ item.color }}
                  </p>
                  <p class="mb-0" style="font-size: 13px; color: #6c757d;">
                    Size: {{ item.size }}
                  </p>
                </div>
              </div>

              <div class="mt-2 mt-md-0" style="width: 20%; min-width: 120px;">
                <div style="font-size: 14px; color: #6c757d;">
                  {{ formatPrice(item.discount) }}
                </div>
                <div style="font-size: 13px; color: #dc3545;">
                  ( {{ item.discountPercent }}% )
                </div>
              </div>

              <div class="mt-2 mt-md-0 d-flex align-items-center" style="width: 20%; min-width: 120px;">
                <div class="d-flex align-items-center border rounded">
                  <button
                    class="btn btn-sm"
                    @click="updateQuantity(item.id, -1)"
                    style="border: none; padding: 4px 12px;"
                  >
                    -
                  </button>
                  <input
                    type="text"
                    :value="item.quantity"
                    readonly
                    class="text-center"
                    style="width: 40px; border: none; outline: none;"
                  />
                  <button
                    class="btn btn-sm"
                    @click="updateQuantity(item.id, 1)"
                    style="border: none; padding: 4px 12px;"
                  >
                    +
                  </button>
                </div>
              </div>

              <div class="mt-2 mt-md-0 d-flex align-items-center justify-content-between" style="width: 20%; min-width: 150px;">
                <strong style="font-size: 16px;">{{ formatPrice(item.price * item.quantity) }}</strong>
                <button
                  class="btn btn-danger text-danger"
                  @click="removeItem(item.id)"
                >
                  <i class="pi pi-trash text-white"/>
                </button>
              </div>
            </div>

            <!-- Continue Shopping Button -->
            <button class="btn btn-outline-secondary mt-4" style="border-radius: 8px; padding: 10px 24px;">
              ← Tiếp tục mua hàng
            </button>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="col-lg-4">
          <div class="bg-white rounded shadow-sm p-4">
            <h5 class="mb-4">Tổng tiền giỏ hàng</h5>

            <div class="d-flex justify-content-between mb-3">
              <span style="color: #6c757d;">Tổng sản phẩm</span>
              <span>{{ totalProducts }}</span>
            </div>

            <div class="d-flex justify-content-between mb-3">
              <span style="color: #6c757d;">Tổng tiền hàng</span>
              <span>{{ formatPrice(subtotal) }}</span>
            </div>

            <div class="d-flex justify-content-between mb-3 pb-3 border-bottom">
              <span style="color: #6c757d;">Thanh tiền</span>
              <strong style="color: #dc3545; font-size: 18px;">{{ formatPrice(payment) }}</strong>
            </div>

            <div class="d-flex justify-content-between mb-4">
              <span style="color: #6c757d;">Tạm tính</span>
              <strong style="font-size: 18px;">{{ formatPrice(provisional) }}</strong>
            </div>

            <!-- Notice -->
            <div class="alert alert-warning d-flex align-items-start" style="font-size: 13px; background-color: #fff3cd; border: none;">
              <span class="me-2">ℹ️</span>
              <span>
                Sản phẩm nằm trong CTKM giảm giá trên 50% không hỗ trợ đổi trả, KHÔNG THANH TOÁN cho shipper khi CHƯA NHẬN HÀNG!!
              </span>
            </div>

            <!-- Order Button -->
            <button class="btn btn-dark w-100" style="border-radius: 8px; padding: 12px; font-size: 15px; font-weight: 500;">
              ĐÁT HÀNG
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { formatPrice } from '@/utils/format';
import { ref, computed } from 'vue';

interface CartItem {
  id: number;
  name: string;
  image: string;
  color: string;
  size: string;
  discount: number;
  discountPercent: number;
  price: number;
  quantity: number;
  selected: boolean;
}

const steps = ['Giỏ hàng', 'Đặt hàng', 'Thanh toán', 'Hoàn thành đơn'];

const cartItems = ref<CartItem[]>([
  {
    id: 1,
    name: 'Chân váy Ruby Tweed Midi',
    image: 'https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=300&h=400&fit=crop',
    color: 'Tím đậm',
    size: 'XL',
    discount: -218000,
    discountPercent: -20,
    price: 872000,
    quantity: 1,
    selected: false
  },
  {
    id: 2,
    name: 'Áo Blazer Ruby Signature',
    image: 'https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=300&h=400&fit=crop',
    color: 'Tím đậm',
    size: 'XXL',
    discount: -498000,
    discountPercent: -20,
    price: 1992000,
    quantity: 1,
    selected: false
  }
]);

const totalProducts = computed(() => {
  return cartItems.value.filter(item => item.selected).reduce((sum, item) => sum + item.quantity, 0);
});

const subtotal = computed(() => {
  return cartItems.value.filter(item => item.selected).reduce((sum, item) => sum + item.price * item.quantity, 0);
});

const payment = computed(() => subtotal.value);
const provisional = computed(() => subtotal.value);

const isAllSelected = computed(() => {
  return cartItems.value.length > 0 && cartItems.value.every(item => item.selected);
});

const selectedCount = computed(() => {
  return cartItems.value.filter(item => item.selected).length;
});

const toggleSelectAll = () => {
  const selectAll = !isAllSelected.value;
  cartItems.value.forEach(item => {
    item.selected = selectAll;
  });
};

const toggleSelectItem = (id: number) => {
  const item = cartItems.value.find(item => item.id === id);
  if (item) {
    item.selected = !item.selected;
  }
};

const updateQuantity = (id: number, delta: number) => {
  const item = cartItems.value.find(item => item.id === id);
  if (item) {
    item.quantity = Math.max(1, item.quantity + delta);
  }
};

const removeItem = (id: number) => {
  cartItems.value = cartItems.value.filter(item => item.id !== id);
};
</script>