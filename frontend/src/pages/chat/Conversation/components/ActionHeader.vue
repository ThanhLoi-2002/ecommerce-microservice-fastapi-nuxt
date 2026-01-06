<template>
    <div class="container-fluid p-0">
        <div class="p-3 border-bottom bg-white">
            <h4 class="text-primary font-weight-bold mb-2">Chat</h4>

            <!-- Search Bar -->
            <div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text bg-light border-0">
                        <i class="pi pi-search text-muted small mt-1"></i>
                    </span>
                </div>
                <input type="text" v-model="searchQuery" class="form-control border-0 bg-light p-0"
                    placeholder="Tìm kiếm" />
                <div class="d-flex" style="cursor: pointer; margin-left: 5px;">
                    <span class="rounded-5 py-1 px-2 hover-bg-light" @click="showAddFriend = true">
                        <i class="pi pi-user-plus small"></i>
                    </span>
                    <span class="rounded-5 py-1 px-2 hover-bg-light" @click="showCreateGroup = true">
                        <i class="pi pi-users small"></i>
                    </span>
                </div>
            </div>
        </div>
        <!-- <FileMessage/> -->

        <!-- Add Friend Modal -->
        <Modal title="Thêm bạn" :open="showAddFriend" :closeModal="() => showAddFriend = false">
            <div class="form-group">
                <div class="input-group">
                    <div class="input-group-prepend">
                        <select class="custom-select border-0 bg-light" v-model="countryCode" style="max-width: 100px;">
                            <option value="+84">🇻🇳 (+84)</option>
                            <option value="+1">🇺🇸 (+1)</option>
                            <option value="+44">🇬🇧 (+44)</option>
                        </select>
                    </div>
                    <input type="tel" class="form-control border-0 bg-light" placeholder="Số điện thoại"
                        v-model="phoneNumber" />
                </div>
            </div>

            <template v-if="recentContacts.length > 0">
                <h6 class="text-muted small mb-2">Kết quả gần nhất</h6>
                <div v-for="contact in recentContacts" :key="contact.id"
                    class="d-flex align-items-center p-2 hover-bg-light rounded cursor-pointer"
                    @click="openProfile(contact)">
                    <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center"
                        style="width: 40px; height: 40px;">
                        <span>{{ contact.avatar }}</span>
                    </div>
                    <div class="ml-3">
                        <div class="font-weight-bold">{{ contact.name }}</div>
                        <div class="text-muted small">{{ contact.phone }}</div>
                    </div>
                </div>
            </template>

            <div class="modal-footer border-0">
                <button type="button" class="btn btn-secondary" @click="showAddFriend = false">
                    Hủy
                </button>
                <button type="button" class="btn btn-primary">
                    Tìm kiếm
                </button>
            </div>
        </Modal>

        <!-- Create Group Modal -->
        <Modal title="Tạo nhóm" :open="showCreateGroup" :closeModal="() => showCreateGroup = false">
            <!-- Group Name Input -->
            <div class="form-group">
                <div class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text bg-light border-0">
                            <i class="pi pi-camera"></i>
                        </span>
                    </div>
                    <input type="text" class="form-control border-0 bg-light" placeholder="Nhập tên nhóm..."
                        v-model="groupName" />
                </div>
            </div>

            <!-- Member Search -->
            <div class="form-group">
                <div class="input-group">
                    <div class="input-group-prepend">
                        <span class="input-group-text bg-light border-0">
                            <i class="pi pi-search"></i>
                        </span>
                    </div>
                    <input type="text" class="form-control border-0 bg-light"
                        placeholder="Nhập tên, số điện thoại, hoặc danh sách số điện thoại" v-model="memberSearch" />
                </div>
            </div>

            <!-- Category Pills -->
            <div ref="catScroll" class="d-flex flex-nowrap mb-3" style="gap: 8px; overflow-x: hidden;">
                <span v-for="(cat, idx) in categories" :key="idx"
                    :class="['badge', idx === 0 ? 'badge-primary' : 'badge-light text-dark', 'px-3 py-2']"
                    style="cursor: pointer; font-size: 14px; white-space: nowrap;">
                    {{ cat }}
                </span>
            </div>

            <!-- Contacts List -->
            <div style="max-height: 300px; overflow-y: auto;">
                <h6 class="text-muted small mb-2">Trò chuyện gần đây</h6>
                <div v-for="contact in allContacts.filter(c => c.section === 'Trò chuyện gần đây')" :key="contact.id"
                    class="d-flex align-items-center p-2 hover-bg-light rounded" style="cursor: pointer;"
                    @click="toggleMember(contact.id)">
                    <input type="checkbox" :checked="selectedMembers.includes(contact.id)"
                        @change="toggleMember(contact.id)" class="mr-3" />
                    <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center"
                        style="width: 40px; height: 40px;">
                        <span>{{ contact.avatar }}</span>
                    </div>
                    <div class="ml-3">
                        <div class="font-weight-bold">{{ contact.name }}</div>
                    </div>
                </div>

                <h6 class="text-muted small mb-2 mt-3">B</h6>
                <div v-for="contact in allContacts.filter(c => c.section === 'B')" :key="contact.id"
                    class="d-flex align-items-center p-2 hover-bg-light rounded" style="cursor: pointer;"
                    @click="toggleMember(contact.id)">
                    <input type="checkbox" :checked="selectedMembers.includes(contact.id)"
                        @change="toggleMember(contact.id)" class="mr-3" />
                    <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center"
                        style="width: 40px; height: 40px;">
                        <span>{{ contact.avatar }}</span>
                    </div>
                    <div class="ml-3">
                        <div class="font-weight-bold">{{ contact.name }}</div>
                    </div>
                </div>

                <h6 class="text-muted small mb-2 mt-3">D</h6>
                <div v-for="contact in allContacts.filter(c => c.section === 'D')" :key="contact.id"
                    class="d-flex align-items-center p-2 hover-bg-light rounded" style="cursor: pointer;"
                    @click="toggleMember(contact.id)">
                    <input type="checkbox" :checked="selectedMembers.includes(contact.id)"
                        @change="toggleMember(contact.id)" class="mr-3" />
                    <div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center"
                        style="width: 40px; height: 40px;">
                        <span>{{ contact.avatar }}</span>
                    </div>
                    <div class="ml-3">
                        <div class="font-weight-bold">{{ contact.name }}</div>
                    </div>
                </div>
            </div>
            <div class="modal-footer border-0">
                <button type="button" class="btn btn-secondary" @click="showCreateGroup = false">
                    Hủy
                </button>
                <button type="button" class="btn btn-primary" :disabled="selectedMembers.length === 0">
                    Tạo nhóm
                </button>
            </div>
        </Modal>

        <!-- Profile Modal -->
        <FriendProfileModal :isOpen="showProfile" :profile="selectedProfile" :close="() => showProfile = false"/>
    </div>
</template>

<script setup lang="ts">
import Modal from '@/components/common/modal/Modal.vue';
import { onBeforeUnmount, onMounted, ref } from 'vue';
import FriendProfileModal from './Modal/FriendProfileModal.vue';
import type { Contact } from '@/types/common';
import FileMessage from './Message/FileMessage.vue';

// Search
const searchQuery = ref('');

// Add Friend Modal
const showAddFriend = ref(false);
const phoneNumber = ref('');
const countryCode = ref('+84');

const recentContacts = ref<Contact[]>([
    { id: 1, name: 'Thùy Vy', phone: '(+84) 0332 871178', avatar: '👤' },
]);

// Create Group Modal
const showCreateGroup = ref(false);
const groupName = ref('');
const memberSearch = ref('');
const selectedMembers = ref<number[]>([]);

const categories = ['Tất cả', 'Khách hàng', 'Gia đình', 'Công việc', 'Bạn bè', 'Trả lời sau'];

// Profile Modal
const showProfile = ref(false);
const selectedProfile = ref<Contact | undefined>(undefined);

const openProfile = (contact: Contact) => {
    selectedProfile.value = contact;
    showProfile.value = true;
};

const allContacts = ref<Contact[]>([
    { id: 2, name: 'John Kt', avatar: '👤', section: 'Trò chuyện gần đây' },
    { id: 3, name: 'Doantbphuong', avatar: '👤', section: 'Trò chuyện gần đây' },
    { id: 4, name: 'Linh Huynh', avatar: '👤', section: 'Trò chuyện gần đây' },
    { id: 5, name: 'Buubuu Au', avatar: '👤', section: 'Trò chuyện gần đây' },
    { id: 6, name: 'Huỳnh Thị Kim Hoa', avatar: '👤', section: 'Trò chuyện gần đây' },
    { id: 7, name: 'Bảo Ngọc', avatar: '👤', section: 'B' },
    { id: 8, name: 'Buubuu Au', avatar: '👤', section: 'B' },
    { id: 9, name: 'Doan Nguyet', avatar: '👤', section: 'D' },
]);

const toggleMember = (memberId: number) => {
    const index = selectedMembers.value.indexOf(memberId);
    if (index > -1) {
        selectedMembers.value.splice(index, 1);
    } else {
        selectedMembers.value.push(memberId);
    }
};

const catScroll = ref<HTMLElement | null>(null)

// ====== CUỘN CHUỘT ======
const handleWheel = (e: WheelEvent) => {
  const el = catScroll.value
  if (!el) return

  if (el.scrollWidth <= el.clientWidth) return

  e.preventDefault()
  el.scrollLeft += e.deltaY
}

onMounted(() => {
  const el = catScroll.value
  if (!el) return

  el.addEventListener('wheel', handleWheel, { passive: false })
})

onBeforeUnmount(() => {
  const el = catScroll.value
  if (!el) return

  el.removeEventListener('wheel', handleWheel)
})
</script>