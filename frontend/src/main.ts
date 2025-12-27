import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import 'primeicons/primeicons.css'
import { createPinia } from 'pinia'
import SocketPlugin, { createSocket } from "@/plugins/socketio";

const app = createApp(App)
const pinia = createPinia()

// tạo socket instance
const socket = createSocket();

// dùng plugin
app.use(SocketPlugin, socket);
app.use(router)
app.use(pinia)
app.mount('#app')