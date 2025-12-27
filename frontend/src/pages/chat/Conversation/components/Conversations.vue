<template>
    <div class="conversations-sidebar border-right bg-white">
        <!-- Header -->
        <div class="p-3 border-bottom">
            <h4 class="text-primary font-weight-bold mb-3">Chat</h4>
            <!-- Search Bar -->
            <div class="input-group">
                <div class="input-group-prepend">
                    <span class="input-group-text bg-light border-0">
                        <i class="pi pi-search text-muted"></i>
                    </span>
                </div>
                <input type="text" v-model="searchQuery" class="form-control border-0 bg-light"
                    placeholder="Tìm kiếm" />
            </div>
        </div>

        <!-- Conversations List -->
        <div class="conversations-list overflow-auto">
            <div v-for="conv in filteredConversations" :key="conv.id" @click="selectConversation(conv)"
                :class="['conversation-item p-3 cursor-pointer', { active: selectedConversation?.id === conv.id }]">
                <div class="d-flex align-items-center">
                    <!-- Avatar -->
                    <div class="position-relative mr-4" style="width: 10%">
                        <div class="avatar">
                            <i :class="['pi', conv.isGroup ? 'pi-users' : 'pi-user']"></i>
                        </div>
                        <span v-if="conv.isGroup" class="group-badge">
                            <i class="pi pi-users"></i>
                        </span>
                    </div>

                    <!-- Conversation Info -->
                    <div class="flex-grow-1 my-auto" style="width: 50%">
                        <h6 class="mb-0 font-weight-bold text-truncate">{{ conv.name }}</h6>
                        <p class="mb-0 text-muted small text-truncate">{{ conv.lastMessage }}</p>
                    </div>

                    <div class="d-flex flex-column align-items-center" style="width: 20%"><span
                            class="small">{{
                                conv.lastMessageTime
                            }}</span><span v-if="conv.unreadCount > 0" class="badge badge-danger mt-1">{{ conv.unreadCount
                            }}</span></div>
                    <!-- Unread Badge -->

                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useConversationStore } from '@/stores/conversation.store';
import { computed, ref } from 'vue';

interface Conversation {
    id: string;
    name: string;
    isGroup: boolean;
    lastMessage: string;
    lastMessageTime: string;
    unreadCount: number;
    members?: string[];
}

// State
const conversations = ref<Conversation[]>([
    {
        id: '1',
        name: 'Nguyễn Văn A',
        isGroup: false,
        lastMessage: 'Hẹn gặp bạn chiều nay nhé!',
        lastMessageTime: '14:30',
        unreadCount: 2,
    },
    {
        id: '2',
        name: 'Nhóm Dự Án Web',
        isGroup: true,
        lastMessage: 'Mai họp lúc 9h sáng nha mọi người',
        lastMessageTime: '13:15',
        unreadCount: 0,
        members: ['User1', 'User2', 'User3', 'User4'],
    },
    {
        id: '3',
        name: 'Trần Thị B',
        isGroup: false,
        lastMessage: 'Cảm ơn bạn nhiều!',
        lastMessageTime: 'Hôm qua',
        unreadCount: 0,
    },
    {
        id: '4',
        name: 'Team Marketing',
        isGroup: true,
        lastMessage: 'Đã gửi file báo cáo',
        lastMessageTime: 'Hôm qua',
        unreadCount: 5,
        members: ['User1', 'User2', 'User3'],
    },
]);

const selectedConversation = ref<Conversation | null>(conversations.value[0] || null);
const searchQuery = ref('');
const conversationStore = useConversationStore()

// Computed
const filteredConversations = computed(() => {
    return conversations.value.filter(conv =>
        conv.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
});

// Methods
const selectConversation = (conv: Conversation) => {
    conversationStore.setSelectedConversation(conv);
};
</script>
<style>
.conversations-sidebar {
    width: 320px;
    display: flex;
    flex-direction: column;
}

.conversations-list {
    flex: 1;
}

.conversation-item {
    transition: background-color 0.2s;
    cursor: pointer;
}

.conversation-item:hover {
    background-color: #f8f9fa;
}

.conversation-item.active {
    background-color: #e3f2fd;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 20px;
}

.avatar-small {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #a8a8a8 0%, #6c6c6c 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 14px;
    flex-shrink: 0;
}

.group-badge {
    position: absolute;
    bottom: -4px;
    right: -4px;
    width: 20px;
    height: 20px;
    background-color: #007bff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 10px;
    border: 2px solid white;
}
</style>