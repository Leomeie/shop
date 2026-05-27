import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import { ElMessage, ElPagination } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import 'element-plus/es/components/pagination/style/css'
import 'element-plus/es/components/skeleton/style/css'
import 'element-plus/es/components/skeleton-item/style/css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router'
import './styles/global.css'

const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)
app.use(ElMessage, { locale: zhCn })
app.component('ElPagination', ElPagination)
app.mount('#app')
