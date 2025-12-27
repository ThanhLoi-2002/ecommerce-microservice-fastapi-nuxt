<template>
    <div class="chat-container d-flex h-100">
        <!-- Left Sidebar - Conversations List -->
        <Conversations />

        <!-- Right Side - Chat Area -->
        <div class="chat-area flex-grow-1 d-flex flex-column">
            <!-- Chat Header -->
            <div class="chat-header bg-white border-bottom p-3 d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center">
                    <div class="avatar mr-3">
                        <i :class="['fas', selectedConversation?.isGroup ? 'fa-users' : 'fa-user']"></i>
                    </div>
                    <div>
                        <h6 class="mb-0 font-weight-bold">{{ selectedConversation?.name }}</h6>
                        <small v-if="selectedConversation?.isGroup" class="text-muted">
                            {{ selectedConversation.members?.length }} thành viên
                        </small>
                    </div>
                </div>
                <div class="d-flex align-items-center">
                    <button class="btn btn-link text-secondary p-2">
                        <i class="pi pi-phone"></i>
                    </button>
                    <button class="btn btn-link text-secondary p-2">
                        <i class="pi pi-video"></i>
                    </button>
                    <button class="btn btn-link text-secondary p-2">
                        <i class="pi pi-ellipsis-v"></i>
                    </button>
                </div>
            </div>

            <!-- Messages Area -->
            <div class="messages-area flex-grow-1 overflow-auto p-3 bg-light">
                <div v-for="message in messages" :key="message.id"
                    :class="['message-wrapper mb-3', message.senderId === 'me' ? 'justify-content-end' : 'justify-content-start']">
                    <div v-if="message.senderId !== 'me'" class="avatar-small mr-2">
                        <i class="pi pi-user"></i>
                    </div>

                    <div class="message-content">
                        <div v-if="message.type === 'text'"
                            :class="['message-bubble', message.senderId === 'me' ? 'message-sent' : 'message-received']">
                            {{ message.content }}
                        </div>

                        <div v-else-if="message.type === 'file'"
                            :class="['message-bubble file-message', message.senderId === 'me' ? 'message-sent' : 'message-received']">
                            <i class="pi pi-file mr-2"></i>
                            <span>{{ message.fileName }}</span>
                        </div>

                        <small class="d-block text-muted mt-1">
                            {{ formatTime(message.timestamp) }}
                        </small>
                    </div>
                </div>
            </div>

            <!-- Message Input -->
            <div class="message-input bg-white border-top p-3">
                <div class="d-flex align-items-center">
                    <!-- File Upload -->
                    <input type="file" ref="fileInput" @change="handleFileSelect" style="display: none" />
                    <button @click="triggerFileInput" class="btn btn-light rounded-circle mr-2" title="Đính kèm file">
                        <i class="pi pi-paperclip"></i>
                    </button>

                    <!-- Emoji Button -->
                    <button @click="showEmojiPicker = !showEmojiPicker" class="btn btn-light rounded-circle mr-2"
                        title="Chọn emoji">
                        <i class="pi pi-smile"></i>
                    </button>

                    <!-- Emoji Picker -->
                    <div v-if="showEmojiPicker"
                        class="emoji-picker position-absolute bg-white border rounded shadow-sm p-2">
                        <span v-for="emoji in emojis" :key="emoji" @click="addEmoji(emoji)" class="emoji-item">
                            {{ emoji }}
                        </span>
                    </div>

                    <!-- Image Upload -->
                    <input type="file" ref="imageInput" @change="handleImageSelect" accept="image/*"
                        style="display: none" />
                    <button @click="triggerImageInput" class="btn btn-light rounded-circle mr-2" title="Gửi ảnh">
                        <i class="pi pi-image"></i>
                    </button>

                    <!-- Text Input -->
                    <input v-model="inputMessage" @keypress.enter="sendMessage" type="text"
                        class="form-control rounded-pill mr-2" placeholder="Nhập tin nhắn..." />

                    <!-- Send Button -->
                    <button @click="sendMessage" class="btn btn-primary rounded-circle"
                        :disabled="!inputMessage.trim() && !selectedFile">
                        <i class="pi pi-paper-plane"></i>
                    </button>
                </div>

                <!-- File Preview -->
                <div v-if="selectedFile"
                    class="file-preview mt-2 p-2 bg-light rounded d-flex align-items-center justify-content-between">
                    <div class="d-flex align-items-center">
                        <i class="pi pi-file text-primary mr-2"></i>
                        <span class="small">{{ selectedFile.name }}</span>
                    </div>
                    <button @click="clearSelectedFile" class="btn btn-sm btn-link text-danger">
                        <i class="pi pi-times"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import Conversations from './components/Conversations.vue';
import { useConversationStore } from '@/stores/conversation.store';
import { storeToRefs } from 'pinia';

// Types
interface Message {
    id: string;
    senderId: string;
    content: string;
    type: 'text' | 'file' | 'image';
    fileName?: string;
    timestamp: Date;
}

const messages = ref<Message[]>([
    {
        id: '1',
        senderId: 'other',
        content: 'Chào bạn! Bạn khỏe không?',
        type: 'text',
        timestamp: new Date(Date.now() - 3600000),
    },
    {
        id: '2',
        senderId: 'me',
        content: 'Mình khỏe, cảm ơn bạn!',
        type: 'text',
        timestamp: new Date(Date.now() - 3000000),
    },
    {
        id: '3',
        senderId: 'other',
        content: 'Hẹn gặp bạn chiều nay nhé!',
        type: 'text',
        timestamp: new Date(Date.now() - 1800000),
    },
]);

const inputMessage = ref('');
const selectedFile = ref<File | null>(null);
const showEmojiPicker = ref(false);
const fileInput = ref<HTMLInputElement | null>(null);
const imageInput = ref<HTMLInputElement | null>(null);

const conversationStore = useConversationStore()
const { selectedConversation } = storeToRefs(conversationStore)

const emojis = ['😀', '😂', '😍', '🥰', '😊', '😎', '🤔', '😢', '😭', '😡', '👍', '👏', '🎉', '❤️', '💯'];

const sendMessage = () => {
    if (inputMessage.value.trim() || selectedFile.value) {
        const newMessage: Message = {
            id: Date.now().toString(),
            senderId: 'me',
            content: inputMessage.value,
            type: selectedFile.value ? 'file' : 'text',
            fileName: selectedFile.value?.name,
            timestamp: new Date(),
        };
        messages.value.push(newMessage);
        inputMessage.value = '';
        selectedFile.value = null;
        showEmojiPicker.value = false;
    }
};

const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
};

const triggerFileInput = () => {
    fileInput.value?.click();
};

const triggerImageInput = () => {
    imageInput.value?.click();
};

const handleFileSelect = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        selectedFile.value = target.files[0];
    }
};

const handleImageSelect = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        selectedFile.value = target.files[0];
    }
};

const clearSelectedFile = () => {
    selectedFile.value = null;
    if (fileInput.value) fileInput.value.value = '';
    if (imageInput.value) imageInput.value.value = '';
};

const addEmoji = (emoji: string) => {
    inputMessage.value += emoji;
    showEmojiPicker.value = false;
};
</script>

<style scoped>
.chat-container {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.chat-area {
    background-color: #f5f5f5;
}

.messages-area {
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23e0e0e0' fill-opacity='0.1'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.message-wrapper {
    display: flex;
}

.message-content {
    max-width: 60%;
}

.message-bubble {
    padding: 10px 15px;
    border-radius: 18px;
    word-wrap: break-word;
    display: inline-block;
}

.message-sent {
    background-color: #007bff;
    color: white;
    border-bottom-right-radius: 4px;
}

.message-received {
    background-color: white;
    color: #333;
    border-bottom-left-radius: 4px;
}

.file-message {
    display: flex;
    align-items: center;
    cursor: pointer;
}

.file-message:hover {
    opacity: 0.9;
}

.cursor-pointer {
    cursor: pointer;
}

.min-width-0 {
    min-width: 0;
}

.message-input {
    position: relative;
}

.emoji-picker {
    bottom: 70px;
    left: 50px;
    z-index: 1000;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 5px;
    max-width: 200px;
}

.emoji-item {
    cursor: pointer;
    font-size: 24px;
    padding: 5px;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.emoji-item:hover {
    background-color: #f0f0f0;
}

.file-preview {
    border: 1px solid #dee2e6;
}

.btn-link {
    text-decoration: none;
}

.btn-link:hover {
    color: #007bff !important;
}

/* Scrollbar Styling */
.conversations-list::-webkit-scrollbar,
.messages-area::-webkit-scrollbar {
    width: 6px;
}

.conversations-list::-webkit-scrollbar-track,
.messages-area::-webkit-scrollbar-track {
    background: #f1f1f1;
}

.conversations-list::-webkit-scrollbar-thumb,
.messages-area::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
}

.conversations-list::-webkit-scrollbar-thumb:hover,
.messages-area::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
}
</style>