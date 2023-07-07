import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/FeedView.vue'
import ChallengesView from '../views/ChallengesView.vue'
import GroupView from '../views/GroupView.vue'
import ProfileView from '../views/ProfileView.vue'
import StatisticsView from '../views/StatisticsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/challenges',
      name: 'challenges',
      component: ChallengesView
    },
    {
      path: '/statistics',
      name: 'statistics',
      component: StatisticsView
    },
    {
      path: '/user',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/group',
      name: 'group',
      component: GroupView
    }
  ]
})

export default router
