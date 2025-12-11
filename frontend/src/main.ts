import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import 'primeicons/primeicons.css'
import { createPinia } from 'pinia'

const app = createApp(App)
const pinia = createPinia()

app.use(router)
app.use(pinia)
app.mount('#app')
