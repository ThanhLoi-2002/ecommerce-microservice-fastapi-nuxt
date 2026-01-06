<template>
    <div v-if="selectedConversation" class="w-100 h-100">
        <div class="chat-area d-flex">
            <div class="d-flex flex-column w-100">
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
                        <VideoCallButton :remoteUser="remoteUser" />
                        <button class="btn btn-link text-secondary p-2" @click="isOpenInfo = !isOpenInfo"
                            :class="isOpenInfo ? 'active' : ''">
                            <i :class="`pi ${isOpenInfo ? 'pi-table' : 'pi-stop'}`"></i>
                        </button>
                    </div>
                </div>

                <!-- Messages Area -->
                <div ref="messagesArea" class="messages-area flex-grow-1 p-3 bg-light">
                    <div v-for="message in messages" :key="message.id"
                        :class="['message-wrapper mb-3', message.senderId === 'me' ? 'justify-content-end' : 'justify-content-start']">
                        <div v-if="message.senderId !== 'me'" class="avatar-small mr-2">
                            <i class="pi pi-user"></i>
                        </div>

                        <MessageBody :message="message" />
                    </div>
                </div>

                <div class="px-4 bg-light text-muted">Đang nhập ......</div>
                <!-- Message Input -->
                <div class="message-input bg-white border-top p-3">

                    <!-- File Preview -->
                    <div v-if="selectedFile"
                        class="file-preview mb-2 p-2 bg-light rounded d-flex align-items-center justify-content-between">
                        <div class="d-flex align-items-center">
                            <i class="pi pi-file text-primary mr-2"></i>
                            <span class="small">{{ selectedFile.name }}</span>
                        </div>
                        <button @click="clearSelectedFile" class="btn btn-sm btn-link text-danger">
                            <i class="pi pi-times"></i>
                        </button>
                    </div>


                    <div class="d-flex mb-2 gap-1">
                        <!-- File Upload -->
                        <input type="file" ref="fileInput" @change="handleFileSelect" style="display: none" />
                        <button @click="triggerFileInput" class="btn-action" title="Đính kèm file">
                            <i class="pi pi-paperclip"></i>
                        </button>

                        <div ref="emojiWrapper">
                            <!-- Emoji Button -->
                            <button @click="showEmojiPicker = !showEmojiPicker" class="btn-action"
                                :class="showEmojiPicker ? 'active' : ''" title="Chọn emoji">
                                <i class="pi pi-face-smile"></i>
                            </button>

                            <!-- Emoji Picker -->
                            <div v-if="showEmojiPicker"
                                class="emoji-picker position-absolute bg-white border rounded shadow-sm p-2">
                                <span v-for="emoji in emojis" :key="emoji" @click="addEmoji(emoji)" class="emoji-item">
                                    {{ emoji }}
                                </span>
                            </div>
                        </div>

                        <!-- Image Upload -->
                        <input type="file" ref="imageInput" @change="handleImageSelect" accept="image/*"
                            style="display: none" />
                        <button @click="triggerImageInput" class="btn-action" title="Gửi ảnh">
                            <i class="pi pi-image"></i>
                        </button>
                    </div>

                    <div class="d-flex gap-1">
                        <!-- Text Input -->
                        <input v-model="inputMessage" @keypress.enter="sendMessage" type="text"
                            class="form-control rounded-pill" placeholder="Nhập tin nhắn..." />

                        <!-- Send Button -->
                        <button @click="sendMessage" class="btn btn-primary rounded-circle"
                            :disabled="!inputMessage.trim() && !selectedFile">
                            <i class="pi pi-send small" style="transform: rotate(45deg);"></i>
                        </button>
                    </div>

                </div>
            </div>
            <!-- Info panel -->
            <InfoPanel v-if="isOpenInfo" />
        </div>
    </div>

    <div v-else class="w-100 d-flex justify-content-center align-items-center">
        <img src="https://play-lh.googleusercontent.com/a_DZ0xqWRDNPvA7rBIIPTeWOPDZp6MEAXuz2fuSgaLOfnEk3q1Xsg35cv7QtL7QEBvM"
            class="rounded-circle" />
    </div>
</template>

<script setup lang="ts">
import { useConversationStore } from '@/stores/conversation.store';
import { storeToRefs } from 'pinia';
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue';
import InfoPanel from './InfoPanel.vue';
import VideoCallButton from './VideoCallButton.vue';
import MessageBody from './MessageBody.vue';

// Types
interface Message {
    id: number;
    senderId: string;
    content?: string;
    type: 'text' | 'file' | 'image';
    fileName?: string;
    fileUrl?: string        // file, image
    timestamp: Date;
}

const messages = ref<Message[]>([
    {
        id: 1,
        senderId: 'other',
        content: 'Chào bạn! Bạn khỏe không?',
        type: 'text',
        timestamp: new Date(Date.now() - 3600000),
    },
    {
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },
    {
        id: 3,
        senderId: 'me',
        type: 'image',
        fileUrl: 'https://media-cdn-v2.laodong.vn/storage/newsportal/2023/8/26/1233821/Giai-Nhi-1--Nang-Tre.jpg?w=800&crop=auto&scale=both',
        timestamp: new Date()
    },
    {
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },{
        id: 2,
        senderId: 'me',
        type: 'file',
        fileName: '123.pdf',
        fileUrl: '/uploads/123.pdf',
        timestamp: new Date()
    },
]);

const conversationStore = useConversationStore()
const { selectedConversation } = storeToRefs(conversationStore)
const fileInput = ref<HTMLInputElement | null>(null);
const imageInput = ref<HTMLInputElement | null>(null);
const messagesArea = ref<HTMLDivElement | null>(null);
const inputMessage = ref('');
const selectedFile = ref<File | null>(null);
const isOpenInfo = ref(false)

const remoteUser = { id: 1, name: "123", avatar: '123' }

const emojis = ['😀', '😂', '😍', '🥰', '😊', '😎', '🤔', '😢', '😭', '😡', '👍', '👏', '🎉', '❤️', '💯'];

const sendMessage = () => {
    if (inputMessage.value.trim() || selectedFile.value) {
        const newMessage: Message = {
            id: Date.now(),
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
        nextTick(() => {
            if (messagesArea.value) {
                messagesArea.value.scrollTop = messagesArea.value.scrollHeight;
            }
        });
    }
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

const showEmojiPicker = ref(false);
const emojiWrapper = ref<any>(null)


const handleClickOutside = (event: any) => {
    if (
        emojiWrapper.value &&
        !emojiWrapper.value.contains(event.target)
    ) {
        showEmojiPicker.value = false
    }
}

const handleResize = () => {
    isOpenInfo.value = window.innerWidth >= 1200
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside)

    handleResize()
    window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside)
})
</script>
<style>
.chat-area {
    background-color: #f5f5f5;
    height: 100%;
}

.messages-area {
    max-height: 100%;
    overflow-y: auto;
    scrollbar-gutter: stable;
}

.message-wrapper {
    display: flex;
}

.message-content {
    max-width: 60%;
}

.btn-action {
    border: none;
    background-color: white;
}

.btn-action.active {
    color: white;
    background: rgb(58, 168, 241);
}

.btn-action:not(.active):hover {
    background-color: rgb(223, 221, 221);
}

.message-input {
    position: relative;
}

.emoji-picker {
    bottom: 100px;
    left: 50px;
    z-index: 1000;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
    max-width: 200px;
    overflow-y: auto;
    overflow-x: hidden;
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

.btn.btn-link.active i {
    color: #0d6efd;
    /* xanh Bootstrap */
}

.chat-info {
    width: 30%;
    background: #fff;
}
</style>