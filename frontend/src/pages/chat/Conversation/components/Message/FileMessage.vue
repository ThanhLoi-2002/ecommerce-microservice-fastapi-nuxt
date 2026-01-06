<template>
    <!-- Messages Demo Section -->
    <div class="p-3">
        <h5 class="mb-3">Demo Messages</h5>

        <!-- Date Divider -->
        <div class="text-center mb-3">
            <span class="badge badge-secondary px-3 py-1">T5 01/01/2026</span>
        </div>

        <!-- Messages -->
        <div v-for="message in messages" :key="message.id" class="mb-3">
            <!-- Link Preview Message -->
            <div v-if="message.type === MessageTypeEnum.TEXT" class="ml-auto" style="max-width: 400px;">
                <div class="card border-0 shadow-sm" style="background: #e3f2fd;">
                    <div class="card-body p-3">
                        <!-- Link URL -->
                        <a :href="message.linkPreview?.url" class="text-primary small d-block mb-2 text-break"
                            target="_blank">
                            {{ message.linkPreview?.url }}
                        </a>

                        <!-- Preview Card -->
                        <div class="card border-0 bg-white">
                            <div class="card-body p-2">
                                <!-- Preview Image/Icon -->
                                <div class="text-center mb-2" style="font-size: 48px;">
                                    {{ message.linkPreview?.image }}
                                </div>

                                <!-- Preview Content -->
                                <h6 class="font-weight-bold mb-1">{{ message.linkPreview?.title }}</h6>
                                <p class="text-muted small mb-0">{{ message.linkPreview?.description }}</p>
                            </div>
                        </div>

                        <!-- Timestamp -->
                        <div class="text-right mt-2">
                            <small class="text-muted">{{ message.created_at }}</small>
                        </div>
                    </div>
                </div>
            </div>

            <!-- File Message -->
            <div v-if="message.type === MessageTypeEnum.FILE" class="ml-auto" style="max-width: 400px;">
                <div class="card border-0 shadow-sm" style="background: #e3f2fd;">
                    <div class="card-body p-3">
                        <div class="d-flex align-items-center">
                            <!-- File Icon -->
                            <div class="rounded d-flex align-items-center justify-content-center mr-3"
                                style="width: 48px; height: 48px; background: #ff6b35; color: white; font-weight: bold; font-size: 20px;">
                                P
                            </div>

                            <!-- File Info -->
                            <div class="flex-grow-1 mr-2">
                                <div class="font-weight-bold text-truncate" style="max-width: 250px;">
                                    {{ message.file?.name }}
                                </div>
                                <div class="d-flex align-items-center text-muted small">
                                    <span>{{ message.file?.size }}</span>
                                </div>
                            </div>

                            <!-- Action Buttons -->
                            <div class="d-flex" style="gap: 8px;">
                                <button class="btn btn-light btn-sm rounded-circle p-2"
                                    @click="previewFile(message.file)" style="width: 32px; height: 32px;"
                                    title="Xem trước">
                                    <i class="pi pi-eye" style="font-size: 12px;"></i>
                                </button>
                                <button class="btn btn-light btn-sm rounded-circle p-2"
                                    @click="downloadFile(message.file)" style="width: 32px; height: 32px;"
                                    title="Tải xuống">
                                    <i class="pi pi-download" style="font-size: 12px;"></i>
                                </button>
                            </div>
                        </div>

                        <!-- Timestamp -->
                        <div class="text-right mt-2">
                            <small class="text-muted">{{ message.created_at }}</small>
                        </div>
                    </div>
                </div>

                <!-- Reaction and Status -->
                <div class="d-flex justify-content-end align-items-center mt-1">
                    <i class="pi pi-thumbs-up text-primary mr-2" style="font-size: 14px;"></i>
                    <i class="pi pi-check-circle text-success" style="font-size: 14px;"></i>
                    <small class="text-success ml-1">Đã gửi</small>
                </div>
            </div>
        </div>

        <!-- Date Divider -->
        <div class="text-center my-3">
            <span class="badge badge-secondary px-3 py-1">T6 02/01/2026</span>
        </div>

        <!-- Message Input Demo -->
        <div class="mt-4 p-3 border rounded">
            <h6 class="mb-3">Test Link Preview</h6>
            <div class="input-group mb-2">
                <input type="text" class="form-control" placeholder="Nhập link để test preview..." @keyup.enter="async (e) => {
                    const input = e.target as HTMLInputElement;
                    if (input.value.trim()) {
                        const msg = await processMessage(input.value);
                        messages.push(msg);
                        input.value = '';
                    }
                }" />
            </div>
            <small class="text-muted">
                Nhấn Enter để gửi. Thử với:
                <span class="badge badge-info ml-1">docs.google.com</span>
                <span class="badge badge-info ml-1">youtube.com</span>
                <span class="badge badge-info ml-1">github.com</span>
            </small>
        </div>

    </div>
</template>
<script setup lang="ts">
import { useUserStore } from '@/stores/user.store';
import { MessageTypeEnum } from '@/types/common';
import type { MessageType } from '@/types/entities';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
const userStore = useUserStore()
const { user } = storeToRefs(userStore)

// Sample Messages
const messages = ref<MessageType[]>([
    {
        id: 1,
        conversation_id: 1,
        sender_id: 1,
        sender: user.value!,
        content: 'https://docs.google.com/document/d/1n3bp2n0s65qhnViedQMzGCBSGdhQ3g0Rg6XHX8M0t-4/ed....t.0',
        created_at: '19:16',
        type: MessageTypeEnum.TEXT,
        linkPreview: {
            url: 'https://docs.google.com/document/d/1n3bp2n0s65qhnViedQMzGCBSGdhQ3g0Rg6XHX8M0t-4/ed....t.0',
            title: 'Vũ trụ Dragon Ball x7game',
            description: 'Cấp 60 (chú ý : cấp trong hình ảnh của tất cả tướng là sai ) Link youtube :... docs.google.com',
            image: '🐉'
        }
    },
    {
        id: 2,
        conversation_id: 1,
        sender_id: 1,
        sender: user.value!,
        content: '2026_目標設定_UI_20251227 (CN-VN).pptx',
        created_at: '14:37',
        type: MessageTypeEnum.FILE,
        file: {
            name: '2026_目標設定_UI_20251227 (CN-VN).pptx',
            size: '507.04 KB',
            url: '#',
            public_id: ''
        }
    }
]);

// Link detection and preview
const urlRegex = /(https?:\/\/[^\s]+)/g;

const detectLinks = (text: string): string[] => {
    const matches = text.match(urlRegex);
    return matches || [];
};

const fetchLinkPreview = async (url: string) => {
    // Simulate API call to fetch link preview
    // In real app, you would call a backend service that fetches Open Graph data
    try {
        // Mock preview data based on URL patterns
        if (url.includes('docs.google.com')) {
            return {
                url: url,
                title: 'Google Docs Document',
                description: 'View document on Google Docs',
                image: '📄'
            };
        } else if (url.includes('youtube.com') || url.includes('youtu.be')) {
            return {
                url: url,
                title: 'YouTube Video',
                description: 'Watch on YouTube',
                image: '🎥'
            };
        } else if (url.includes('github.com')) {
            return {
                url: url,
                title: 'GitHub Repository',
                description: 'View on GitHub',
                image: '💻'
            };
        } else {
            return {
                url: url,
                title: 'Web Link',
                description: url,
                image: '🔗'
            };
        }
    } catch (error) {
        console.error('Error fetching link preview:', error);
        return null;
    }
};

const processMessage = async (content: string): Promise<MessageType> => {
    const links = detectLinks(content);

    if (links.length > 0) {
        const preview = await fetchLinkPreview(links[0]!);
        return {
            id: 1,
            conversation_id: 1,
            sender_id: 1,
            content: content,
            sender: user.value!,
            created_at: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
            type: MessageTypeEnum.TEXT,
            linkPreview: preview || undefined
        };
    }

    return {
        id: 1,
        conversation_id: 1,
        sender_id: 1,
        content: content,
        sender: user.value!,
        created_at: new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' }),
        type: MessageTypeEnum.TEXT
    };
};

const downloadFile = (file: any) => {
    console.log('Downloading file:', file.name);
};

const previewFile = (file: any) => {
    console.log('Previewing file:', file.name);
};
</script>
<style></style>