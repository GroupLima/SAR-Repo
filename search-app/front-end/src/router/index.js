import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/browse',
      name: 'browse',
      component: () => import('@/views/BrowseView.vue'),
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('@/views/SearchView.vue'),
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('@/views/AboutView.vue'),
    },
    {
      path: '/xquery',
      name: 'xquery',
      component: () => import('@/views/XQueryView.vue'),
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('@/views/HelpPageView.vue'),
    },
    {
      path: '/selected',
      name: 'selected',
      component: () => import('@/views/Selected.vue'),
    },
  ],
})

export default router
