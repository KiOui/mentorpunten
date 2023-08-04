import { createRouter, createWebHistory } from 'vue-router'
import ChallengesView from '../views/ChallengesView.vue'
import TeamView from '../views/TeamView.vue'
import ProfileView from '../views/ProfileView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import FeedView from '../views/FeedView.vue'
import ChallengeView from '../views/ChallengeView.vue'
import TournamentsView from '../views/TournamentsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/tournaments',
      name: 'Tournaments',
      component: TournamentsView
    },
    {
      path: '/challenges',
      name: 'Challenges',
      component: ChallengesView
    },
    {
      path: '/challenge/:id',
      name: 'Challenge',
      component: ChallengeView,
      props: (route) => {
        const id= Number.parseInt(route.params.id, 10);
        if (Number.isNaN(id)) {
          router.push("/");
          return;
        }
        return {
          "id": id
        };
      }
    },
    {
      path: '/statistics',
      name: 'Statistics',
      component: StatisticsView
    },
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileView
    },
    {
      path: '/team/:id',
      name: 'Team',
      component: TeamView,
      props: (route) => {
        const id= Number.parseInt(route.params.id, 10);
        if (Number.isNaN(id)) {
          router.push("/");
          return;
        }
        return {
          "id": id
        };
      }
    },
    {
      path: '/',
      name: 'Index',
      component: FeedView
    },
    {
      path: "/auth/callback",
      name: "OAuth Authorization",
      component: () => import("../views/Authorize.vue"),
    },
  ]
})

export default router
