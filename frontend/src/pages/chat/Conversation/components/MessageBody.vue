<template>
    <div class="message-wrapper" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
        <div class="message-content d-flex flex-column"
            :class="message.senderId === 'me' ? 'align-items-end' : 'align-items-start'">

            <!-- Message bubble wrapper with actions -->
            <div class="message-bubble-wrapper" :style="message.senderId != 'me' && 'flex-direction: row-reverse;'">
                <!-- Message Actions (hover) -->
                <div v-if="showActions" class="message-actions" :class="[
                    isMultiLine ? 'actions-bottom' : 'actions-middle'
                ]" @mouseenter="handleMouseEnter" @mouseleave="handleMouseLeave">
                    <button @click="toggleContextMenu" class="btn-action" title="Tùy chọn">
                        <i class="pi pi-ellipsis-v"></i>
                    </button>
                    <button @click="handleReply" class="btn-action" title="Trả lời">
                        <i class="pi pi-reply"></i>
                    </button>
                    <button @click="handleReact" class="btn-action" title="Thả cảm xúc">
                        <i class="pi pi-heart"></i>
                    </button>
                </div>

                <!-- Message Bubble -->
                <div v-if="message.type === 'text'" ref="messageBubbleRef"
                    :class="['message-bubble', message.senderId === 'me' ? 'message-sent' : 'message-received']">
                    {{ message.content }}
                </div>

                <div v-else-if="message.type === 'file'" ref="messageBubbleRef"
                    :class="['message-bubble file-message', message.senderId === 'me' ? 'message-sent' : 'message-received']">
                    <i class="pi pi-file mr-2"></i>
                    <span>{{ message.fileName }}</span>
                </div>

                <!-- IMAGE -->
                <div v-else-if="message.type === 'image'" ref="messageBubbleRef" :class="['message-bubble image-message',
                    message.senderId === 'me' ? 'message-sent' : 'message-received'
                ]">
                    <img :src="message.fileUrl" class="chat-image" @click="openImagePreview(0)" />
                </div>
            </div>

            <!-- Time -->
            <small class="d-block text-muted mt-1">
                {{ formatTime(message.timestamp) }}
            </small>
        </div>

        <!-- Context Menu -->
        <div v-if="showContextMenu" class="message-context-menu"
            :class="message.senderId === 'me' ? 'menu-left' : 'menu-right'" :style="contextMenuPosition" @click.stop>
            <div class="context-menu-item" @click="handleReply">
                <i class="pi pi-reply"></i>
                <span>Trả lời</span>
            </div>
            <div class="context-menu-item" @click="handleForward">
                <i class="pi pi-share-alt"></i>
                <span>Chuyển tiếp</span>
            </div>
            <div class="context-menu-item" @click="handleCopy">
                <i class="pi pi-copy"></i>
                <span>Sao chép</span>
            </div>
            <div class="context-menu-item" @click="handlePin">
                <i class="pi pi-thumbtack"></i>
                <span>Ghim tin nhắn</span>
            </div>
            <div class="context-menu-divider"></div>
            <div v-if="message.senderId === 'me'" class="context-menu-item" @click="handleEdit">
                <i class="pi pi-pencil"></i>
                <span>Chỉnh sửa</span>
            </div>
            <div class="context-menu-item" @click="handleDownload">
                <i class="pi pi-download"></i>
                <span>Tải xuống</span>
            </div>
            <div class="context-menu-divider"></div>
            <div class="context-menu-item text-danger" @click="handleDelete">
                <i class="pi pi-trash"></i>
                <span>Xóa tin nhắn</span>
            </div>
        </div>

        <!-- Reaction Picker -->
        <div v-show="showReactionPicker" class="reaction-picker"
            :class="message.senderId === 'me' ? 'picker-left' : 'picker-right'" @click.stop>
            <button v-for="emoji in reactionEmojis" :key="emoji" @click="addReaction(emoji)" class="reaction-emoji">
                {{ emoji }}
            </button>
        </div>

        <!-- IMAGE PREVIEW -->
        <div v-if="showImagePreview" class="image-preview-overlay">
            <!-- Main Image -->
            <div class="image-preview-main">
                <img :src="previewImages[currentIndex]" class="preview-image" :style="{ transform: `scale(${scale})` }"
                    @wheel="handleWheelZoom" @click="handleClickZoom" @dblclick="scale = 1" />
            </div>

            <!-- Thumbnail List -->
            <div class="image-preview-list">
                <div v-for="(img, index) in previewImages" :key="img" class="thumbnail"
                    :class="{ active: index === currentIndex }" @click="currentIndex = index">
                    <img :src="img" style="width: 150px;" />
                </div>
            </div>

            <!-- Close -->
            <button class="preview-close" @click="closeImagePreview">✕</button>
        </div>

    </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue';

interface Message {
    id: number;
    senderId: string;
    type: 'text' | 'file' | 'image';
    content?: string;
    fileName?: string;
    fileUrl?: string        // file, image
    timestamp: Date | string;
}

interface Props {
    message: Message;
}

const props = defineProps<Props>();
const emit = defineEmits(['reply', 'forward', 'copy', 'pin', 'edit', 'delete', 'download', 'react']);

// State
const showActions = ref(false);
const showContextMenu = ref(false);
const showReactionPicker = ref(false);
const contextMenuPosition = ref({ top: '0px', left: '0px' });
const isMultiLine = ref(false);
const messageBubbleRef = ref<HTMLElement>();

const reactionEmojis = ['❤️', '😂', '😮', '😢', '🙏', '👍'];

let hideTimer: number | null = null;

const scale = ref(1)
const minScale = 1
const maxScale = 3
const clickZoomScale = 2

const showImagePreview = ref(false)
const previewImages = ref<string[]>([props.message.fileUrl ?? '', props.message.fileUrl ?? '', props.message.fileUrl ?? '', props.message.fileUrl ?? ''])
const currentIndex = ref(0)

watch(currentIndex, () => {
    scale.value = 1
})

const handleClickZoom = () => {
    if (scale.value === minScale) {
        scale.value = clickZoomScale
    } else {
        scale.value = minScale
    }
}

const handleWheelZoom = (event: WheelEvent) => {
    event.preventDefault()

    const zoomStep = 0.1

    if (event.deltaY < 0) {
        // scroll up → zoom in
        scale.value = Math.min(maxScale, scale.value + zoomStep)
    } else {
        // scroll down → zoom out
        scale.value = Math.max(minScale, scale.value - zoomStep)
    }
}

const openImagePreview = (index = 0) => {
    currentIndex.value = index
    showImagePreview.value = true
}

const closeImagePreview = () => {
    showImagePreview.value = false
}


// Methods
const checkMultiLine = () => {
    if (messageBubbleRef.value) {
        const lineHeight = parseFloat(getComputedStyle(messageBubbleRef.value).lineHeight);
        const height = messageBubbleRef.value.offsetHeight;
        const padding = parseFloat(getComputedStyle(messageBubbleRef.value).paddingTop) +
            parseFloat(getComputedStyle(messageBubbleRef.value).paddingBottom);
        const contentHeight = height - padding;

        // Check if content is more than one line
        isMultiLine.value = contentHeight > lineHeight * 1.5;
    }
};

const handleMouseEnter = () => {
    if (hideTimer) {
        clearTimeout(hideTimer);
        hideTimer = null;
    }
    showActions.value = true;
    checkMultiLine();
};

const handleMouseLeave = () => {
    hideTimer = window.setTimeout(() => {
        if (!showContextMenu.value && !showReactionPicker.value) {
            showActions.value = false;
        }
    }, 300);
};

const toggleContextMenu = (event: MouseEvent) => {
    event.stopPropagation();
    showContextMenu.value = !showContextMenu.value;
    showReactionPicker.value = false;

    if (showContextMenu.value) {
        // Get mouse position
        const mouseX = event.clientX;
        const mouseY = event.clientY;

        // Get window dimensions
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        // Context menu dimensions (estimated)
        const menuWidth = 200;
        const menuHeight = 300;

        // Calculate position
        let top = mouseY;
        let left = mouseX;

        // Adjust if menu goes off screen right
        if (left + menuWidth > windowWidth) {
            left = mouseX - menuWidth;
        }

        // Adjust if menu goes off screen bottom
        if (top + menuHeight > windowHeight) {
            top = mouseY - menuHeight;
        }

        // Ensure menu doesn't go off screen top
        if (top < 0) {
            top = 10;
        }

        // Ensure menu doesn't go off screen left
        if (left < 0) {
            left = 10;
        }

        contextMenuPosition.value = {
            top: `${top}px`,
            left: `${left}px`
        };
    }
};

const handleReply = () => {
    emit('reply', props.message);
    closeMenus();
};

const handleForward = () => {
    emit('forward', props.message);
    closeMenus();
};

const handleCopy = () => {
    if (props.message.content) {
        navigator.clipboard.writeText(props.message.content);
    }
    emit('copy', props.message);
    closeMenus();
};

const handlePin = () => {
    emit('pin', props.message);
    closeMenus();
};

const handleEdit = () => {
    emit('edit', props.message);
    closeMenus();
};

const handleDelete = () => {
    if (confirm('Bạn có chắc muốn xóa tin nhắn này?')) {
        emit('delete', props.message);
    }
    closeMenus();
};

const handleDownload = () => {
    emit('download', props.message);
    closeMenus();
};

const handleReact = (event: MouseEvent) => {
    event.stopPropagation();
    showReactionPicker.value = !showReactionPicker.value;
    showContextMenu.value = false;
};

const addReaction = (emoji: string) => {
    emit('react', { message: props.message, emoji });
    closeMenus();
};

const closeMenus = () => {
    showContextMenu.value = false;
    showReactionPicker.value = false;
    showActions.value = false;
};

const handleClickOutside = (event: MouseEvent) => {
    const target = event.target as HTMLElement;
    if (!target.closest('.message-wrapper')) {
        closeMenus();
    }
};

const formatTime = (timestamp: Date | string) => {
    const date = typeof timestamp === 'string' ? new Date(timestamp) : timestamp;
    return date.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
};

onMounted(() => {
    document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside);
    if (hideTimer) {
        clearTimeout(hideTimer);
    }
});
</script>

<style scoped>
.message-wrapper {
    position: relative;
}

.message-content {
    position: relative;
    max-width: 100%;
}

/* Message Bubble Wrapper - contains bubble and actions side by side */
.message-bubble-wrapper {
    position: relative;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Message Actions */
.message-actions {
    position: relative;
    display: flex;
    gap: 4px;
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 20px;
    padding: 4px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    z-index: 10;
    flex-shrink: 0;
}

/* Position for single line - middle aligned */
.message-actions.actions-middle {
    align-self: center;
}

/* Position for multi-line - bottom aligned */
.message-actions.actions-bottom {
    align-self: flex-end;
    margin-bottom: 4px;
}

.btn-action {
    width: 25px;
    height: 25px;
    border-radius: 50%;
    border: none;
    background: transparent;
    color: #666;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    font-size: 13px;
}

.btn-action:hover {
    background: #f0f0f0;
    color: #333;
    transform: scale(1.1);
}

.btn-action:active {
    transform: scale(0.95);
}

/* Message Bubble */
.message-bubble {
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 100%;
    word-wrap: break-word;
    line-height: 1.4;
}

.message-sent {
    background: #0d6efd;
    color: #fff;
    border-bottom-right-radius: 4px;
}

.message-received {
    background: #f0f0f0;
    color: #333;
    border-bottom-left-radius: 4px;
}

.file-message {
    display: flex;
    align-items: center;
    gap: 8px;
}

/* Context Menu */
.message-context-menu {
    position: fixed;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    min-width: 200px;
    z-index: 1000;
    animation: slideDown 0.2s ease;
    overflow: hidden;
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

.context-menu-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    cursor: pointer;
    transition: background-color 0.2s;
    color: #333;
    font-size: 14px;
}

.context-menu-item:hover {
    background: #f5f5f5;
}

.context-menu-item.text-danger {
    color: #dc3545;
}

.context-menu-item.text-danger:hover {
    background: #fee;
}

.context-menu-item i {
    font-size: 16px;
    width: 20px;
}

.context-menu-divider {
    height: 1px;
    background: #e0e0e0;
    margin: 4px 0;
}

/* Reaction Picker */
.reaction-picker {
    position: absolute;
    bottom: calc(100% + 8px);
    background: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 24px;
    padding: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    display: flex;
    gap: 4px;
    z-index: 100;
    animation: scaleIn 0.2s ease;
}

.reaction-picker.picker-left {
    right: 0;
}

.reaction-picker.picker-right {
    left: 0;
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.8);
    }

    to {
        opacity: 1;
        transform: scale(1);
    }
}

.reaction-emoji {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    background: transparent;
    font-size: 24px;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.reaction-emoji:hover {
    background: #f0f0f0;
    transform: scale(1.2);
}

.reaction-emoji:active {
    transform: scale(0.9);
}

.image-message {
    padding: 4px;
    background: none;
}

.chat-image {
    max-width: 150px;
    border-radius: 12px;
    cursor: pointer;
}

/* Responsive */
@media (max-width: 768px) {
    .message-content {
        max-width: 85%;
    }

    .btn-action {
        width: 28px;
        height: 28px;
        font-size: 12px;
    }

    .reaction-emoji {
        width: 36px;
        height: 36px;
        font-size: 20px;
    }
}

/* Thumbnail */
.chat-image {
    max-width: 220px;
    border-radius: 12px;
    cursor: zoom-in;
    transition: transform 0.2s ease;
}

.chat-image:hover {
    transform: scale(1.03);
}

/* Overlay */
.image-preview-overlay {
    position: fixed;
    inset: 0;
    background: #111;
    display: flex;
    z-index: 9999;
}

/* Main image */
.image-preview-main {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}

.preview-image {
    max-width: 90%;
    max-height: 90%;
    object-fit: contain;
    transition: transform 0.1s ease;
    cursor: zoom-in;
}

/* Right list */
.image-preview-list {
    width: 150px;
    background: #1e1e1e;
    padding: 8px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

/* Thumbnail */
.thumbnail {
    cursor: pointer;
    border-radius: 6px;
    overflow: hidden;
    opacity: 0.6;
    border: 2px solid transparent;
}

.thumbnail img {
    width: 100%;
    height: 70px;
    object-fit: cover;
}

.thumbnail.active {
    opacity: 1;
    border-color: #0d6efd;
    z-index: 1;
}

/* Close */
.preview-close {
    position: absolute;
    top: 12px;
    right: 170px;
    background: transparent;
    border: none;
    font-size: 28px;
    color: #fff;
    cursor: pointer;
}
</style>