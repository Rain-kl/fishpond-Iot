import { createRouter, createWebHistory } from 'vue-router'
import RealTimeControl from '../views/RealTimeControl.vue'
import RealTimeMonitor from '../views/RealTimeMonitor.vue'
import HistoryData from '../views/HistoryData.vue'
import AboutUs from '../views/AboutUs.vue'

const routes = [
    {
        path: '/',
        redirect: '/monitor'
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
    },
    {
        path: '/about',
        name: 'AboutUs',
        component: AboutUs
    },
    {
        path: '/history',
        name: 'HistoryData',
        component: HistoryData
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
