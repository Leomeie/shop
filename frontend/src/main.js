import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { ElMessage, ElPagination } from 'element-plus'
import 'element-plus/es/components/message/style/css'
import 'element-plus/es/components/pagination/style/css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import App from './App.vue'
import router from './router'
import './styles/global.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElMessage, { locale: zhCn })
app.component('ElPagination', ElPagination)
app.mount('#app')
