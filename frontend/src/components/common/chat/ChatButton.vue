<template>
    <div class="chat-app">
        <button @click="toggleChat" class="chat-button"><i class="pi pi-comment" /></button>
        <div v-if="isChatVisible" class="chat-container">
            <div class="user-list">
                <input type="text" placeholder="Tìm kiếm..." v-model="searchTerm" class="form-control search" />
                <ul>
                    <li v-for="user in filteredUsers" :key="user.id" @click="selectUser(user)"
                        :class="{ selected: selectedUser && selectedUser.id === user.id }">
                        <img :src="user.avatar" alt="Avatar" class="avatar-small" />
                        <div class="user-info">
                            <div class="user-name">{{ user.name }}</div>
                            <div class="text-truncate">{{ user.lastMessage.sender == 'me' ? "Bạn" : user.name }}: {{
                                user.lastMessage.text }}</div>
                        </div>
                        <div class="timestamp d-flex flex-column align-items-center"><span>{{ user.lastMessage.time
                                }}</span><span
                                class="bg-danger text-center text-white mt-1 rounded-circle small w-75">+5</span></div>
                    </li>
                </ul>
            </div>
            <div class="chat-ui" v-if="selectedUser">
                <div class="chat-header">
                    <img :src="selectedUser.avatar" alt="Avatar" class="rounded-circle border"
                        style="width: 50px; height: 50px" />
                    <div class="d-flex flex-column justify-content-between">
                        <h5>{{ selectedUser.name }}</h5>
                        <span
                            :style="`width: 10px; height: 10px; border-radius: 50%; background: ${selectedUser.isOnline ? 'green' : 'gray'}`">
                        </span>
                    </div>
                </div>
                <div class="messages">
                    <div v-for="msg in currentMessages" :key="msg.id" class="message"
                        :class="{ sent: msg.sender === 'me', received: msg.sender !== 'me' }">
                        <div class="message-content">
                            {{ msg.text }}
                            <span class="time">{{ msg.time }}</span>
                        </div>
                        <div v-if="msg.seen" class="seen">Đã xem</div>
                    </div>
                </div>
                <input type="text" v-model="newMessage" @keyup.enter="sendMessage" placeholder="Gõ tin nhắn..."
                    class="form-control" />
                <!-- <input type="file" @change="sendFile" class="file-input" /> -->
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface User {
    id: number;
    name: string;
    avatar: string;
    isOnline: boolean;
    lastMessage: { text: string; time: string, sender: string };
}

interface Message {
    id: number;
    text: string;
    time: string;
    sender: string;
    seen?: boolean;
}

const isChatVisible = ref(false);
const searchTerm = ref('');
const users = ref<User[]>([
    { id: 1, name: 'Người dùng A', avatar: '	https://res.cloudinary.com/dqoepulwu/image/upload/v1765504718/fastapi/oami3y1ztcwimthqxczh.jpg', isOnline: true, lastMessage: { text: 'Chào bạn!', time: '15:30', sender: 'me' } },
    { id: 2, name: 'Người dùng B', avatar: '	https://res.cloudinary.com/dqoepulwu/image/upload/v1765504718/fastapi/oami3y1ztcwimthqxczh.jpg', isOnline: false, lastMessage: { text: 'Hẹn gặp lại!', time: '14:20', sender: 'other' } }
]);

const messages = ref<{ [key: number]: Message[] }>({
    1: [{ id: 1, text: 'Chào bạn!', time: '15:00', sender: 'me', seen: true }],
    2: [{ id: 1, text: 'Xin chào!', time: '14:00', sender: 'other', seen: false }]
});

const newMessage = ref('');
const selectedUser = ref<User | null>(null);

const filteredUsers = computed(() => {
    return users.value.filter(user =>
        user.name.toLowerCase().includes(searchTerm.value.toLowerCase())
    );
});

const selectUser = (user: User) => {
    selectedUser.value = user;
};

const sendMessage = () => {
    if (newMessage.value.trim() && selectedUser.value) {
        const currentChat = messages.value[selectedUser.value.id] || [];
        currentChat.push({
            id: currentChat.length + 1,
            text: newMessage.value,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            sender: 'me',
            seen: false
        });
        messages.value[selectedUser.value.id] = currentChat;
        newMessage.value = '';
    }
};

const sendFile = (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
        // Xử lý gửi file
    }
};

const currentMessages = computed(() => {
    return selectedUser.value ? messages.value[selectedUser.value.id] : [];
});

const toggleChat = () => {
    isChatVisible.value = !isChatVisible.value;
    if (!isChatVisible.value) {
        selectedUser.value = null; // Reset khi đóng chat
    }
};
</script>

<style scoped>
.chat-app {
    position: relative;
}

.chat-button {
    position: fixed;
    width: 44px;
    bottom: 10px;
    right: 20px;
    padding: 10px 10px;
    border: none;
    background-color: #007bff;
    color: white;
    border-radius: 50%;
    cursor: pointer;
}

.chat-container {
    border: 1px solid #ddd;
    background-color: white;
    border-radius: 5px;
    width: 50%;
    height: 700px;
    position: fixed;
    bottom: 75px;
    /* Điều chỉnh nếu cần */
    right: 20px;
    display: flex;
    z-index: 1;
}

.user-list {
    width: 40%;
    border-right: 1px solid #ddd;
    padding: 10px;
    background-color: white;
    /* Nền trắng */
    overflow-y: auto;
}

.search {
    margin-bottom: 10px;
}

.user-list ul {
    list-style: none;
    padding: 0;
}

.user-list li {
    display: flex;
    align-items: start;
    padding: 5px;
    cursor: pointer;
    border-radius: 5px;
}

.user-list li.selected {
    background-color: #f1f1f1;
}

.avatar-small {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    margin-right: 10px;
    border: 0.5px solid #d4d3d3;
}

.user-info {
    flex-grow: 1;
    font-size: 13px;
    width: 65%;
}

.timestamp {
    font-size: 0.7em;
    color: gray;
}

.chat-ui {
    width: 60%;
    padding: 10px;
    display: flex;
    flex-direction: column;
    background-color: white;
    /* Nền trắng */
}

.chat-header {
    padding: 10px;
    display: flex;
    align-items: center;
    gap: 5px;
}

.messages {
    flex-grow: 1;
    overflow-y: auto;
    border: 1px solid #ddd;
    padding: 10px;
    margin-bottom: 10px;
    background-color: transparent;
    /* Trong suốt để thấy viền */
}

.message {
    margin-bottom: 10px;
}

.sent {
    text-align: right;
}

.received {
    text-align: left;
}

.message-content {
    display: inline-block;
    padding: 10px;
    border-radius: 5px;
}

.sent .message-content {
    background-color: #dcf8c6;
}

.received .message-content {
    background-color: #f1f0f0;
}

.time {
    font-size: 0.75em;
    color: gray;
    display: block;
}

.seen {
    font-size: 0.75em;
    color: green;
}

.file-input {
    margin-top: 10px;
}

.close-button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    font-size: 1.2em;
    color: #333;
}

@media (max-width: 768px) {
    .chat-container {
        width: 90%;
    }
}
</style>