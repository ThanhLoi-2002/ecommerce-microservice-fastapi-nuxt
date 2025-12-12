// UserList.vue
<template>
  <div class="min-vh-100" style="background-color: #f8f9fa;">
    <!-- Header -->
    <nav class="navbar navbar-dark bg-dark">
      <div class="container-fluid">
        <span class="navbar-brand mb-0 h1">
          👥 Fashion Admin - Quản lý Người dùng
        </span>
        <div class="text-white">
          <span class="mr-3">👤 Admin</span>
        </div>
      </div>
    </nav>

    <div class="container-fluid mt-4">
      <div class="card shadow-sm">
        <div class="card-header bg-white">
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="mb-0">Danh sách Người dùng</h5>
            <div>
              <button class="btn btn-success mr-2" @click="exportUsers">
                📊 Xuất Excel
              </button>
              <button class="btn btn-primary" @click="showModal('create')">
                ➕ Thêm người dùng
              </button>
            </div>
          </div>
        </div>
        <div class="card-body">
          <!-- Bộ lọc -->
          <div class="row mb-4">
            <div class="col-md-3">
              <input
                type="text"
                class="form-control"
                placeholder="🔍 Tìm tên, email, SĐT..."
                v-model="filters.search"
                @input="debouncedSearch"
              />
            </div>
            <div class="col-md-2">
              <select class="form-control" v-model="filters.role" @change="loadUsers">
                <option value="">Tất cả vai trò</option>
                <option value="admin">Admin</option>
                <option value="staff">Nhân viên</option>
                <option value="customer">Khách hàng</option>
              </select>
            </div>
            <div class="col-md-2">
              <select class="form-control" v-model="filters.status" @change="loadUsers">
                <option value="">Tất cả trạng thái</option>
                <option value="active">Đang hoạt động</option>
                <option value="inactive">Không hoạt động</option>
                <option value="banned">Đã khóa</option>
              </select>
            </div>
            <div class="col-md-2">
              <select class="form-control" v-model="filters.verified" @change="loadUsers">
                <option value="">Xác thực</option>
                <option value="true">Đã xác thực</option>
                <option value="false">Chưa xác thực</option>
              </select>
            </div>
            <div class="col-md-2">
              <select class="form-control" v-model="sortBy" @change="loadUsers">
                <option value="-created">Mới nhất</option>
                <option value="created">Cũ nhất</option>
                <option value="name">Tên A-Z</option>
                <option value="-name">Tên Z-A</option>
              </select>
            </div>
            <div class="col-md-1">
              <button class="btn btn-outline-secondary btn-block" @click="resetFilters">
                🔄
              </button>
            </div>
          </div>

          <!-- Thống kê nhanh -->
          <div class="row mb-4">
            <div class="col-md-3">
              <div class="stat-card bg-primary">
                <div class="stat-value">{{ stats.total }}</div>
                <div class="stat-label">Tổng người dùng</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card bg-success">
                <div class="stat-value">{{ stats.active }}</div>
                <div class="stat-label">Đang hoạt động</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card bg-info">
                <div class="stat-value">{{ stats.verified }}</div>
                <div class="stat-label">Đã xác thực</div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card bg-warning">
                <div class="stat-value">{{ stats.newThisMonth }}</div>
                <div class="stat-label">Mới tháng này</div>
              </div>
            </div>
          </div>

          <!-- Loading -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="sr-only">Loading...</span>
            </div>
          </div>

          <!-- Bảng người dùng -->
          <div v-else class="table-responsive">
            <table class="table table-hover table-bordered">
              <thead class="thead-light">
                <tr>
                  <th width="50">#</th>
                  <th width="80">Avatar</th>
                  <th>Họ tên</th>
                  <th>Email</th>
                  <th width="120">SĐT</th>
                  <th width="100">Vai trò</th>
                  <th width="120">Trạng thái</th>
                  <th width="100">Xác thực</th>
                  <th width="120">Ngày tạo</th>
                  <th width="200">Thao tác</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>
                    <img 
                      :src="user.avatar || 'https://via.placeholder.com/50'" 
                      :alt="user.name"
                      class="user-avatar"
                    />
                  </td>
                  <td>
                    <strong>{{ user.name }}</strong>
                  </td>
                  <td>
                    <small>{{ user.email }}</small>
                  </td>
                  <td>{{ user.phone }}</td>
                  <td>
                    <span :class="getRoleBadgeClass(user.role)">
                      {{ getRoleLabel(user.role) }}
                    </span>
                  </td>
                  <td>
                    <select 
                      class="form-control form-control-sm"
                      :class="getStatusSelectClass(user.status)"
                      v-model="user.status"
                      @change="updateUserStatus(user.id, user.status)"
                    >
                      <option value="active">Hoạt động</option>
                      <option value="inactive">Không hoạt động</option>
                      <option value="banned">Đã khóa</option>
                    </select>
                  </td>
                  <td class="text-center">
                    <span v-if="user.verified" class="badge badge-success">✓ Đã xác thực</span>
                    <span v-else class="badge badge-warning">⚠ Chưa xác thực</span>
                  </td>
                  <td>
                    <small>{{ formatDate(user.createdAt) }}</small>
                  </td>
                  <td>
                    <button 
                      class="btn btn-sm btn-info mr-1" 
                      title="Xem chi tiết"
                      @click="viewUserDetail(user.id)"
                    >
                      👁️
                    </button>
                    <button 
                      class="btn btn-sm btn-warning mr-1" 
                      title="Chỉnh sửa"
                      @click="showModal('edit', user)"
                    >
                      ✏️
                    </button>
                    <button 
                      class="btn btn-sm btn-danger" 
                      title="Xóa"
                      @click="confirmDelete(user.id)"
                      :disabled="user.role === 'admin'"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Phân trang -->
          <div class="d-flex justify-content-between align-items-center mt-3">
            <div>
              <select class="form-control form-control-sm d-inline-block w-auto" v-model="perPage" @change="loadUsers">
                <option :value="10">10</option>
                <option :value="20">20</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
              <span class="ml-2 text-muted">
                Hiển thị {{ (pagination.page - 1) * perPage + 1 }} - 
                {{ Math.min(pagination.page * perPage, pagination.total) }} / 
                <strong>{{ pagination.total }}</strong> người dùng
              </span>
            </div>
            <nav>
              <ul class="pagination mb-0">
                <li class="page-item" :class="{ disabled: pagination.page === 1 }">
                  <a class="page-link" href="#" @click.prevent="changePage(pagination.page - 1)">‹</a>
                </li>
                <li 
                  v-for="page in displayPages" 
                  :key="page" 
                  class="page-item" 
                  :class="{ active: page === pagination.page }"
                >
                  <a class="page-link" href="#" @click.prevent="changePage(page)">{{ page }}</a>
                </li>
                <li class="page-item" :class="{ disabled: pagination.page === pagination.totalPages }">
                  <a class="page-link" href="#" @click.prevent="changePage(pagination.page + 1)">›</a>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Create/Edit -->
    <div v-if="modalVisible" class="modal-backdrop" @click="closeModal">
      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              {{ modalMode === 'create' ? '➕ Thêm người dùng' : '✏️ Chỉnh sửa người dùng' }}
            </h5>
            <button type="button" class="close" @click="closeModal">
              <span>&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="form-row">
                <div class="form-group col-md-6">
                  <label>Họ tên <span class="text-danger">*</span></label>
                  <input 
                    type="text" 
                    class="form-control" 
                    v-model="formData.name"
                    required
                  />
                </div>
                <div class="form-group col-md-6">
                  <label>Email <span class="text-danger">*</span></label>
                  <input 
                    type="email" 
                    class="form-control" 
                    v-model="formData.email"
                    required
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group col-md-6">
                  <label>Số điện thoại <span class="text-danger">*</span></label>
                  <input 
                    type="tel" 
                    class="form-control" 
                    v-model="formData.phone"
                    required
                  />
                </div>
                <div class="form-group col-md-6">
                  <label>Mật khẩu {{ modalMode === 'edit' ? '(để trống nếu không đổi)' : '*' }}</label>
                  <input 
                    type="password" 
                    class="form-control" 
                    v-model="formData.password"
                    :required="modalMode === 'create'"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group col-md-6">
                  <label>Vai trò <span class="text-danger">*</span></label>
                  <select class="form-control" v-model="formData.role" required>
                    <option value="customer">Khách hàng</option>
                    <option value="staff">Nhân viên</option>
                    <option value="admin">Admin</option>
                  </select>
                </div>
                <div class="form-group col-md-6">
                  <label>Trạng thái</label>
                  <select class="form-control" v-model="formData.status">
                    <option value="active">Hoạt động</option>
                    <option value="inactive">Không hoạt động</option>
                    <option value="banned">Đã khóa</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label>Avatar URL</label>
                <input 
                  type="url" 
                  class="form-control" 
                  v-model="formData.avatar"
                  placeholder="https://example.com/avatar.jpg"
                />
                <img 
                  v-if="formData.avatar" 
                  :src="formData.avatar" 
                  alt="Preview"
                  class="mt-2 img-thumbnail"
                  style="max-height: 100px;"
                />
              </div>

              <div class="form-group">
                <label>Địa chỉ</label>
                <textarea 
                  class="form-control" 
                  v-model="formData.address"
                  rows="2"
                ></textarea>
              </div>

              <div class="form-group">
                <div class="custom-control custom-checkbox">
                  <input 
                    type="checkbox" 
                    class="custom-control-input" 
                    id="verifiedCheck"
                    v-model="formData.verified"
                  />
                  <label class="custom-control-label" for="verifiedCheck">
                    Đã xác thực email
                  </label>
                </div>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" @click="closeModal">
                  Hủy
                </button>
                <button type="submit" class="btn btn-primary" :disabled="submitting">
                  {{ submitting ? 'Đang xử lý...' : (modalMode === 'create' ? 'Thêm mới' : 'Cập nhật') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';

interface User {
  id: number;
  name: string;
  email: string;
  phone: string;
  avatar: string | null;
  role: 'admin' | 'staff' | 'customer';
  status: 'active' | 'inactive' | 'banned';
  verified: boolean;
  address: string;
  createdAt: string;
}

// State
const loading = ref(false);
const submitting = ref(false);
const modalVisible = ref(false);
const modalMode = ref<'create' | 'edit'>('create');
const users = ref<User[]>([]);
const perPage = ref(20);
const sortBy = ref('-created');

const filters = ref({
  search: '',
  role: '',
  status: '',
  verified: ''
});

const pagination = ref({
  page: 1,
  total: 0,
  totalPages: 0
});

const stats = ref({
  total: 245,
  active: 198,
  verified: 210,
  newThisMonth: 23
});

const formData = ref({
  id: null as number | null,
  name: '',
  email: '',
  phone: '',
  password: '',
  role: 'customer' as 'admin' | 'staff' | 'customer',
  status: 'active' as 'active' | 'inactive' | 'banned',
  avatar: '',
  address: '',
  verified: false
});

// Mock data
const mockUsers: User[] = [
  { id: 1, name: 'Nguyễn Văn A', email: 'nguyenvana@gmail.com', phone: '0901234567', avatar: 'https://i.pravatar.cc/150?img=1', role: 'admin', status: 'active', verified: true, address: 'Hà Nội', createdAt: '2024-01-15T10:00:00' },
  { id: 2, name: 'Trần Thị B', email: 'tranthib@gmail.com', phone: '0912345678', avatar: 'https://i.pravatar.cc/150?img=2', role: 'staff', status: 'active', verified: true, address: 'Hồ Chí Minh', createdAt: '2024-02-20T14:30:00' },
  { id: 3, name: 'Lê Văn C', email: 'levanc@gmail.com', phone: '0923456789', avatar: 'https://i.pravatar.cc/150?img=3', role: 'customer', status: 'active', verified: true, address: 'Đà Nẵng', createdAt: '2024-03-10T09:15:00' },
  { id: 4, name: 'Phạm Thị D', email: 'phamthid@gmail.com', phone: '0934567890', avatar: 'https://i.pravatar.cc/150?img=4', role: 'customer', status: 'active', verified: false, address: 'Cần Thơ', createdAt: '2024-11-05T16:45:00' },
  { id: 5, name: 'Hoàng Văn E', email: 'hoangvane@gmail.com', phone: '0945678901', avatar: null, role: 'customer', status: 'inactive', verified: true, address: 'Hải Phòng', createdAt: '2024-12-01T11:20:00' },
];

// Computed
const displayPages = computed(() => {
  const pages: number[] = [];
  const total = pagination.value.totalPages;
  const current = pagination.value.page;
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i);
  } else {
    pages.push(1);
    if (current > 3) pages.push(-1);
    for (let i = Math.max(2, current - 1); i <= Math.min(total - 1, current + 1); i++) {
      pages.push(i);
    }
    if (current < total - 2) pages.push(-1);
    pages.push(total);
  }
  return pages;
});

// Methods
const loadUsers = () => {
  loading.value = true;
  setTimeout(() => {
    users.value = mockUsers;
    pagination.value.total = mockUsers.length;
    pagination.value.totalPages = Math.ceil(mockUsers.length / perPage.value);
    loading.value = false;
  }, 500);
};

let searchTimeout: any;
const debouncedSearch = () => {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(loadUsers, 500);
};

const changePage = (page: number) => {
  if (page >= 1 && page <= pagination.value.totalPages) {
    pagination.value.page = page;
    loadUsers();
  }
};

const resetFilters = () => {
  filters.value = { search: '', role: '', status: '', verified: '' };
  sortBy.value = '-created';
  loadUsers();
};

const showModal = (mode: 'create' | 'edit', user?: User) => {
  modalMode.value = mode;
  
  if (mode === 'edit' && user) {
    formData.value = {
      id: user.id,
      name: user.name,
      email: user.email,
      phone: user.phone,
      password: '',
      role: user.role,
      status: user.status,
      avatar: user.avatar || '',
      address: user.address,
      verified: user.verified
    };
  } else {
    formData.value = {
      id: null,
      name: '',
      email: '',
      phone: '',
      password: '',
      role: 'customer',
      status: 'active',
      avatar: '',
      address: '',
      verified: false
    };
  }
  
  modalVisible.value = true;
};

const closeModal = () => {
  modalVisible.value = false;
};

const submitForm = () => {
  submitting.value = true;
  setTimeout(() => {
    alert(modalMode.value === 'create' ? 'Thêm người dùng thành công!' : 'Cập nhật thành công!');
    closeModal();
    loadUsers();
    submitting.value = false;
  }, 1000);
};

const updateUserStatus = (id: number, status: string) => {
  console.log(`Update user ${id} to status: ${status}`);
  alert(`Đã cập nhật trạng thái người dùng #${id}`);
};

const viewUserDetail = (id: number) => {
  alert(`Xem chi tiết người dùng #${id}`);
};

const confirmDelete = (id: number) => {
  if (confirm('Bạn có chắc muốn xóa người dùng này?')) {
    alert(`Đã xóa người dùng #${id}`);
    loadUsers();
  }
};

const exportUsers = () => {
  alert('Xuất danh sách người dùng ra Excel');
};

const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('vi-VN');
};

const getRoleBadgeClass = (role: string): string => {
  const classes = {
    admin: 'badge badge-danger',
    staff: 'badge badge-warning',
    customer: 'badge badge-info'
  };
  return classes[role as keyof typeof classes] || 'badge badge-secondary';
};

const getRoleLabel = (role: string): string => {
  const labels = {
    admin: 'Admin',
    staff: 'Nhân viên',
    customer: 'Khách hàng'
  };
  return labels[role as keyof typeof labels] || role;
};

const getStatusSelectClass = (status: string): string => {
  const classes = {
    active: 'status-active',
    inactive: 'status-inactive',
    banned: 'status-banned'
  };
  return classes[status as keyof typeof classes] || '';
};

onMounted(() => {
  loadUsers();
});
</script>

<style scoped>
.stat-card {
  padding: 20px;
  border-radius: 8px;
  color: white;
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
}

.stat-label {
  font-size: 0.9rem;
  margin-top: 5px;
}

.table td {
  vertical-align: middle;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
}

.status-active { background-color: #d4edda; color: #155724; border-color: #28a745; }
.status-inactive { background-color: #fff3cd; color: #856404; border-color: #ffc107; }
.status-banned { background-color: #f8d7da; color: #721c24; border-color: #dc3545; }

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-dialog {
  background: white;
  border-radius: 8px;
  max-width: 700px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #dee2e6;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}

.close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}
</style>