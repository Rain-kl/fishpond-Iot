import { createRouter, createWebHistory } from 'vue-router'
import RealTimeControl from '../views/RealTimeControl.vue'
import RealTimeMonitor from '../views/RealTimeMonitor.vue'

const routes = [
    {
        path: '/',
        redirect: '/control'
    },
    {
        path: '/control',
        name: 'RealTimeControl',
        component: RealTimeControl
    },
    {
        path: '/monitor',
        name: 'RealTimeMonitor',
        component: RealTimeMonitor
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
