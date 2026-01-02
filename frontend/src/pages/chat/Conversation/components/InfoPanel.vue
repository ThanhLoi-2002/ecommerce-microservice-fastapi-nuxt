<template>
    <div class="chat-info border-left">
        <div class="info-header text-center py-4 border-bottom">
            <div class="info-avatar mx-auto mb-3">
                <img :src="selectedConversation?.avatar || 'https://via.placeholder.com/80'" class="rounded-circle"
                    width="80" height="80" alt="Avatar">
            </div>
            <h6 class="mb-1 font-weight-bold">{{ selectedConversation?.name }}</h6>
            <button class="btn btn-link text-secondary btn-sm p-0">
                <i class="pi pi-pencil"></i>
            </button>
        </div>

        <div class="info-actions d-flex justify-content-around py-3 border-bottom">
            <button class="btn btn-sm btn-link text-center text-secondary">
                <i class="pi pi-bell d-block mb-1"></i>
                <small>Tắt thông báo</small>
            </button>
            <button class="btn btn-sm btn-link text-center text-secondary">
                <i class="pi pi-thumbtack d-block mb-1"></i>
                <small>Ghim hội thoại</small>
            </button>
            <button class="btn btn-sm btn-link text-center text-secondary">
                <i class="pi pi-users d-block mb-1"></i>
                <small>Tạo nhóm trò chuyện</small>
            </button>
        </div>

        <div class="info-content">
            <!-- Scheduled Reminders -->
            <div class="info-section border-bottom">
                <div class="d-flex align-items-center px-3 py-2">
                    <i class="pi pi-clock mr-2"></i>
                    <span>Danh sách nhắc hẹn</span>
                </div>
            </div>

            <!-- Group Info -->
            <div class="info-section border-bottom">
                <div class="d-flex align-items-center px-3 py-2">
                    <i class="pi pi-users mr-2"></i>
                    <span>4 nhóm chung</span>
                </div>
            </div>

            <!-- Media Section -->
            <div class="info-section border-bottom">
                <button @click="toggleSection('media')"
                    class="section-toggle w-100 d-flex align-items-center justify-content-between px-3 py-2">
                    <span>Ảnh/Video</span>
                    <i :class="['pi', expandedSections.media ? 'pi-chevron-up' : 'pi-chevron-down']"></i>
                </button>
                <div v-if="expandedSections.media" class="section-content p-3">
                    <div class="media-grid">
                        <div v-for="i in 6" :key="i" class="media-item">
                            <img :src="`https://via.placeholder.com/100?text=Image${i}`" alt="Media">
                        </div>
                    </div>
                    <button class="btn btn-light btn-block mt-2">Xem tất cả</button>
                </div>
            </div>

            <!-- Files Section -->
            <div class="info-section border-bottom">
                <button @click="toggleSection('files')"
                    class="section-toggle w-100 d-flex align-items-center justify-content-between px-3 py-2">
                    <span>File</span>
                    <i :class="['pi', expandedSections.files ? 'pi-chevron-up' : 'pi-chevron-down']"></i>
                </button>
                <div v-if="expandedSections.files" class="section-content px-3 py-2">
                    <div v-for="file in fileList" :key="file.id" class="file-item d-flex align-items-center py-2">
                        <div class="file-icon mr-2">
                            <i class="pi pi-file text-primary"></i>
                        </div>
                        <div class="flex-grow-1 min-width-0">
                            <div class="file-name text-truncate">{{ file.name }}</div>
                            <small class="text-muted">{{ file.size }} • {{ file.date }}</small>
                        </div>
                    </div>
                    <button class="btn btn-light btn-block mt-2">Xem tất cả</button>
                </div>
            </div>

            <!-- Links Section -->
            <div class="info-section border-bottom">
                <button @click="toggleSection('links')"
                    class="section-toggle w-100 d-flex align-items-center justify-content-between px-3 py-2">
                    <span>Link</span>
                    <i :class="['pi', expandedSections.links ? 'pi-chevron-up' : 'pi-chevron-down']"></i>
                </button>
                <div v-if="expandedSections.links" class="section-content px-3 py-2">
                    <div v-for="link in linkList" :key="link.id" class="link-item d-flex align-items-center py-2">
                        <div class="link-icon mr-2">
                            <i class="pi pi-link"></i>
                        </div>
                        <div class="flex-grow-1 min-width-0">
                            <div class="link-url text-truncate small">{{ link.url }}</div>
                            <small class="text-muted">{{ link.source }} • {{ link.date }}</small>
                        </div>
                    </div>
                    <button class="btn btn-light btn-block mt-2">Xem tất cả</button>
                </div>
            </div>

            <!-- Settings Section -->
            <div class="info-section">
                <button @click="toggleSection('settings')"
                    class="section-toggle w-100 d-flex align-items-center justify-content-between px-3 py-2">
                    <span>Thiết lập bảo mật</span>
                    <i :class="['pi', expandedSections.settings ? 'pi-chevron-up' : 'pi-chevron-down']"></i>
                </button>
                <div v-if="expandedSections.settings" class="section-content px-3 py-2">
                    <div class="setting-item d-flex align-items-center justify-content-between p-2">
                        <div class="d-flex align-items-center">
                            <i class="pi pi-clock mr-2"></i>
                            <div>
                                <div>Tin nhắn tự xóa</div>
                                <small class="text-muted">Không bao giờ</small>
                            </div>
                        </div>
                    </div>
                    <div class="setting-item d-flex align-items-center justify-content-between p-2">
                        <div class="d-flex align-items-center">
                            <i class="pi pi-eye-slash mr-2"></i>
                            <div>Ẩn trò chuyện</div>
                        </div>
                        <label class="switch mb-0">
                            <input type="checkbox" v-model="hideConversation">
                            <span class="slider"></span>
                        </label>
                    </div>
                    <div class="setting-item d-flex align-items-center p-2">
                        <i class="pi pi-exclamation-triangle mr-2"></i>
                        <span>Báo xấu</span>
                    </div>
                    <div class="setting-item d-flex align-items-center p-2 text-danger">
                        <i class="pi pi-trash mr-2"></i>
                        <span>Xóa lịch sử trò chuyện</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useConversationStore } from '@/stores/conversation.store';
import { storeToRefs } from 'pinia';
import { ref, reactive } from 'vue';

// Interfaces
interface Conversation {
    id: number;
    name: string;
    avatar: string;
}

interface FileItem {
    id: number;
    name: string;
    size: string;
    date: string;
}

interface LinkItem {
    id: number;
    url: string;
    source: string;
    date: string;
}

const conversationStore = useConversationStore()
const { selectedConversation } = storeToRefs(conversationStore)

// State
const hideConversation = ref(false);

const expandedSections = reactive({
    media: false,
    files: false,
    links: false,
    settings: false
});

// Sample data
const fileList = ref<FileItem[]>([
    { id: 1, name: 'Document.pdf', size: '2.5 MB', date: '12/12/2024' },
    { id: 2, name: 'Presentation.pptx', size: '5.1 MB', date: '11/12/2024' },
    { id: 3, name: 'Report.docx', size: '1.2 MB', date: '10/12/2024' }
]);

const linkList = ref<LinkItem[]>([
    { id: 1, url: 'https://example.com/article', source: 'Example', date: '12/12/2024' },
    { id: 2, url: 'https://github.com/repo', source: 'GitHub', date: '11/12/2024' },
    { id: 3, url: 'https://docs.site.com', source: 'Documentation', date: '10/12/2024' }
]);

// Methods
const toggleSection = (section: keyof typeof expandedSections) => {
    expandedSections[section] = !expandedSections[section];
};
</script>

<style>
/* Info Panel */
.chat-info {
  width: 320px;
  background: #fff;
  height: 100%;
  overflow-y: auto;
  flex-shrink: 0;
}

.border-left {
  border-left: 1px solid #dee2e6;
}

.border-bottom {
  border-bottom: 1px solid #dee2e6;
}

/* Info Header */
.info-header {
  background: #f8f9fa;
}

.info-avatar {
  width: 80px;
  height: 80px;
}

.info-avatar img {
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.info-header h6 {
  font-size: 1.1rem;
  color: #212529;
  margin-bottom: 0.25rem;
}

.info-header .btn-link {
  color: #6c757d;
  text-decoration: none;
  font-size: 0.9rem;
}

.info-header .btn-link:hover {
  color: #495057;
}

/* Info Actions */
.info-actions {
  background: #fff;
}

.info-actions .btn-link {
  color: #6c757d;
  text-decoration: none;
  flex-direction: column;
  min-width: 70px;
}

.info-actions .btn-link:hover {
  color: #495057;
  background: #f8f9fa;
  border-radius: 8px;
}

.info-actions .pi {
  font-size: 1.2rem;
}

.info-actions small {
  font-size: 0.75rem;
  white-space: nowrap;
}

/* Info Content */
.info-content {
  background: #fff;
  margin-bottom: 20px;
}

.info-section {
  background: #fff;
}

/* Section Toggle */
.section-toggle {
  background: none;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s;
  font-weight: 500;
  color: #212529;
}

.section-toggle:hover {
  background-color: #f8f9fa;
}

.section-toggle .pi {
  font-size: 0.875rem;
  color: #6c757d;
}

/* Section Content */
.section-content {
  animation: slideDown 0.2s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Media Grid */
.media-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.media-item {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s;
}

.media-item:hover {
  transform: scale(1.05);
}

.media-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* File Item */
.file-item {
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 8px;
}

.file-item:hover {
  background-color: #f8f9fa;
}

.file-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e7f3ff;
  border-radius: 8px;
}

.file-icon .pi {
  font-size: 1.25rem;
}

.file-name {
  font-weight: 500;
  font-size: 0.9rem;
  color: #212529;
}

.min-width-0 {
  min-width: 0;
}

/* Link Item */
.link-item {
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 8px;
}

.link-item:hover {
  background-color: #f8f9fa;
}

.link-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f0f0f0;
  border-radius: 8px;
}

.link-icon .pi {
  font-size: 1.25rem;
  color: #6c757d;
}

.link-url {
  color: #0d6efd;
  font-weight: 500;
}

/* Setting Item */
.setting-item {
  cursor: pointer;
  transition: background-color 0.2s;
  border-radius: 8px;
  padding: 0.75rem 0;
}

.setting-item:hover {
  background-color: #f8f9fa;
}

.setting-item .pi {
  font-size: 1.1rem;
  color: #6c757d;
}

.setting-item.text-danger .pi {
  color: #dc3545;
}

/* Toggle Switch */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.3s;
  border-radius: 24px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.3s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #0d6efd;
}

input:checked + .slider:before {
  transform: translateX(20px);
}

/* Buttons */
.btn-light {
  background-color: #f8f9fa;
  border-color: #dee2e6;
  color: #212529;
  font-size: 0.875rem;
}

.btn-light:hover {
  background-color: #e9ecef;
  border-color: #dee2e6;
}

/* Scrollbar */
.chat-info::-webkit-scrollbar {
  width: 6px;
}

.chat-info::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.chat-info::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-info::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* Responsive */
@media (max-width: 768px) {
  .chat-info {
    width: 100%;
    position: fixed;
    top: 0;
    right: 0;
    z-index: 1000;
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  }
}
</style>