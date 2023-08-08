import { createRouter, createWebHistory } from 'vue-router'
import ChallengesView from '../views/ChallengesView.vue'
import TeamView from '../views/TeamView.vue'
import ProfileView from '../views/ProfileView.vue'
import StatisticsView from '../views/StatisticsView.vue'
import FeedView from '../views/FeedView.vue'
import ChallengeView from '../views/ChallengeView.vue'
import TournamentsView from '../views/TournamentsView.vue'
import TransactionsView from "@/views/TransactionsView.vue";
import ProfileSubmissionsView from "@/views/ProfileSubmissionsView.vue";
import TournamentStatisticsView from "@/views/TournamentStatisticsView.vue";
import LogoutView from "@/views/LogoutView.vue";
import SubmissionAcceptView from "@/views/SubmissionAcceptView.vue";
import useApiService from '@/common/api.service';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/tournaments',
      name: 'Tournaments',
      component: TournamentsView
    },
    {
      path: '/challenges/:id',
      name: 'Challenges',
      component: ChallengesView,
      props: (route) => {
        if (Array.isArray(route.params.id)) {
          router.push("/");
          return;
        }
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
      path: '/challenge/:id',
      name: 'Challenge',
      component: ChallengeView,
      props: (route) => {
        if (Array.isArray(route.params.id)) {
          router.push("/");
          return;
        }
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
      path: '/statistics/tournament/:id',
      name: 'TournamentStatistics',
      component: TournamentStatisticsView,
      props: (route) => {
        if (Array.isArray(route.params.id)) {
          router.push("/");
          return;
        }
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
      path: '/profile',
      name: 'Profile',
      component: ProfileView
    },
    {
      path: '/profile/tournament/:id/submissions',
      name: 'ProfileSubmissions',
      component: ProfileSubmissionsView,
      props: (route) => {
        if (Array.isArray(route.params.id)) {
          router.push("/");
          return;
        }
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
      path: '/team/:id',
      name: 'Team',
      component: TeamView,
      props: (route) => {
        if (Array.isArray(route.params.id)) {
          router.push("/");
          return;
        }
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
      path: '/team/:id/transactions',
      name: 'Transactions',
      component: TransactionsView,
      props: (route) => {
        if (Array.isArray(route.params.id)) {
          router.push("/");
          return;
        }
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
      path: '/acceptsubmissions',
      name: 'SubmissionAccept',
      component: SubmissionAcceptView,
    },
    {
      path: '/',
      name: 'Index',
      component: FeedView
    },
    {
      path: '/logout',
      name: 'Logout',
      component: LogoutView
    },
    {
      path: "/auth/callback",
      name: "OAuth Authorization",
      component: () => import("../views/AuthorizeView.vue"),
    },
  ]
})

export default router
