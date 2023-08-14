<script setup lang="ts">
import type Team from "@/models/team.model";
import {computed, onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import Loader from "@/components/Loader.vue";
import type Transaction from "@/models/transaction.model";
import TransactionCard from "@/components/TransactionCard.vue";
import Header from "@/components/Header.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import type BoughtItem from "@/models/boughtitem.model";
import type User from "@/models/user.model";
import {useCredentialsStore} from "@/stores/credentials.module";

const props = defineProps<{id: number}>();

const ApiService = useApiService();
const CredentialsStore = useCredentialsStore();

const user = ref<User | null>(null);
const userLoading = ref<boolean | null>(true);

const team = ref<Team | null>(null);
const teamLoading = ref<boolean | null>(true);

const items = ref<BoughtItem[] | null>(null);
const itemsLoading = ref<boolean | null>(true);

const teams = ref<Team[] | null>(null);
const teamsLoading = ref<boolean | null>(true);

const latestTransactions = ref<Transaction[]>([]);
const latestTransactionsLoading = ref<boolean | null>(true);

onMounted(() => {
  let userLoadingPromise = Promise.resolve();
  if (CredentialsStore.loggedIn) {
    userLoadingPromise = ApiService.getUsersMe().then((result) => {
      user.value = result;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });
  }

  const teamLoadingPromise = ApiService.getChallengesTeam(props.id).then(result => {
    team.value = result;
    teamLoading.value = false;
  }).catch(() => {
    teamLoading.value = null;
  });

  teamLoadingPromise.then(() => {
    if (team.value !== null) {
      ApiService.getChallengesTeams(new URLSearchParams([['tournament', String(team.value.tournament.id)]])).then(result => {
        teams.value = result;
        teamsLoading.value = false;
      }).catch(() => {
        teamsLoading.value = null;
      });
    } else {
      teamsLoading.value = false;
    }
  });

  teamLoadingPromise.then(() => {
    if (team.value !== null) {
      ApiService.getTransactions(new URLSearchParams([["limit", "3"], ["account", `${team.value.points_account.id}`]])).then(result => {
        latestTransactions.value = result.results;
        latestTransactionsLoading.value = false;
      }).catch(() => {
        latestTransactionsLoading.value = null;
      })
    } else {
      latestTransactionsLoading.value = false;
    }
  });

  Promise.all([teamLoadingPromise, userLoadingPromise]).then(() => {
    if (user.value !== null && team.value !== null) {
      const userIsMemberOfTeam = team.value.members.map((member) => {
        return user.value !== null && member.id === user.value.id;
      }).reduce((previousValue, currentValue) => {
        return previousValue || currentValue;
      }, false);
      if (userIsMemberOfTeam) {
        const urlSearchParameters = new URLSearchParams([["team", String(team.value.id)]]);
        ApiService.getBoughtItems(urlSearchParameters).then((result) => {
          items.value = result;
          itemsLoading.value = false;
        }).catch(() => {
          itemsLoading.value = null;
        });
      } else {
        itemsLoading.value = false;
      }
    } else {
      itemsLoading.value = false;
    }
  });
});

const latestItems = computed(() => {
  if (items.value === null) {
    return null;
  }

  return items.value.slice(0, 3);
});

const tournamentRanking = computed(() => {
  if (teams.value === null || team.value === null) {
    return null;
  }
  const sortedTeamsList = Array.from(teams.value);
  sortedTeamsList.sort((teamA: Team, teamB: Team) => {
    return teamB.points_account.balance - teamA.points_account.balance;
  });
  for (let i = 0; i < sortedTeamsList.length; i++) {
    const currentPosition = i + 1;
    const currentTeam = sortedTeamsList[i];
    if (currentTeam.id === team.value.id) {
      return currentPosition;
    }
  }
  return null;
});
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto">
    <Loader v-if="teamLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="teamLoading === null" class="alert alert-warning mx-1">
      There was an error loading this team, please try again.
    </div>
    <template v-else-if="!teamLoading && team !== null">
      <div class="custom-card text-center">
        <h1> {{ team.name }}</h1>
        <h4> total points: {{ team.points_account.balance }}</h4>
      </div>

      <div class="custom-card">
        <h1 class="text-center">Tournament Rankings</h1>
        <Loader v-if="teamsLoading === true || teams === null" size="60px" background-color="#000000"/>
        <div v-else-if="teamsLoading === null || tournamentRanking === null" class="alert alert-warning mx-1">
          There was an error loading the tournament ranking, please try again.
        </div>
        <div v-else class="d-flex justify-content-between">
          <h3>{{ team.tournament.name }}</h3>
          <h3>#{{ tournamentRanking }}</h3>
        </div>
      </div>
      
      <div class="custom-card">
        <h2>Group members</h2>
        <ul>
          <li v-for="member in team.members" v-bind:key="member.id">
            {{ member.display_name }}
          </li>
        </ul>
      </div>

      <div v-if="team.coins_account !== null" class="custom-card">
        <h2>Coins</h2>
        <p>Current balance: <font-awesome-icon icon="fa-solid fa-coins" style="color: var(--primary);"/> {{ team.coins_account.balance }} coins</p>
      </div>

      <div v-if="latestItems !== null" class="custom-card">
        <h2>Items</h2>
        <div v-if="latestItems.length === 0" class="alert alert-warning">
          This team has not bought any items yet.
        </div>
        <div v-else v-for="item in latestItems" v-bind:key="item.id" class="row mb-1">
          <p class="col-8">
            {{ item.name }}
          </p>
          <div class="col-4 d-flex justify-content-end align-items-center">
            <div v-if="item.used" class="badge bg-danger">Used</div>
            <div v-else class="badge bg-success">Not used</div>
          </div>
        </div>
        <div class="w-100 d-flex justify-content-center" style="margin-top: 1rem;">
          <router-link :to="{ name: 'TeamItems', params: { id: team.id } }">
            <button v-if="latestItems.length > 0" class="btn btn-primary">Show all items</button>
          </router-link>
        </div>
      </div>

      <div class="custom-card">
        <h2>Latest Transactions</h2>
        <Loader v-if="latestTransactionsLoading === true" size="60px" background-color="#000000"/>
        <div v-else-if="latestTransactionsLoading === null" class="alert alert-warning mx-1">
          An error occurred during loading of the latest transactions, please try again.
        </div>
        <template v-else>
          <TransactionCard v-for="transaction in latestTransactions" v-bind:key="transaction.id" v-bind:transaction="transaction"/>
          <div class="w-100 d-flex justify-content-center" style="margin-top: 1rem;">
            <router-link :to="{ name: 'Transactions', params: { id: team.id } }">
              <button v-if="latestTransactions.length > 0" class="btn btn-primary">Show all transactions</button>
            </router-link>
          </div>
        </template>
      </div>
    </template>
  </div>
</template>
