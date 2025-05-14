import Vue from 'vue'
import VueRouter from 'vue-router'
import RegistryView from '../views/RegistryView.vue'
import ReportView from '../views/ReportView.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'registry-view',
    component: RegistryView
  },
  {
    path: '/report',
    name: 'report',
    component: ReportView
  }
]

const router = new VueRouter({
  routes
})

export default router
