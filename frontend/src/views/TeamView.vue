<script setup lang="ts">
import type Team from "@/models/team.model";
import {computed, onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import Loader from "@/components/Loader.vue";
import type Transaction from "@/models/transaction.model";
import TransactionCard from "@/components/TransactionCard.vue";
import Header from "@/components/Header.vue";

const props = defineProps<{id: number}>();

const ApiService = useApiService();

const team = ref<Team | null>(null);
const teamLoading = ref<boolean | null>(true);

const teams = ref<Team[] | null>(null);
const teamsLoading = ref<boolean | null>(true);

const latestTransactions = ref<Transaction[]>([]);
const latestTransactionsLoading = ref<boolean | null>(true);

onMounted(() => {
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
      ApiService.getTransactions(new URLSearchParams([["limit", "3"], ["account", `${team.value.account.id}`]])).then(result => {
        latestTransactions.value = result.results;
        latestTransactionsLoading.value = false;
      }).catch(() => {
        latestTransactionsLoading.value = null;
      })
    } else {
      latestTransactionsLoading.value = false;
    }
  });
});

const tournamentRanking = computed(() => {
  if (teams.value === null || team.value === null) {
    return null;
  }
  const sortedTeamsList = Array.from(teams.value);
  sortedTeamsList.sort((teamA, teamB) => {
    return teamA.account.balance - teamB.account.balance;
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
        <h4> total points: {{ team.account.balance }}</h4>
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
