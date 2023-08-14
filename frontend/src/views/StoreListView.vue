<script setup lang="ts">

import Header from "@/components/Header.vue";
import type Tournament from "@/models/tournament.model";
import {onMounted, ref} from "vue";
import Loader from "@/components/Loader.vue";
import StoreCard from "@/components/StoreCard.vue";
import useApiService from "@/common/api.service";
import {useCredentialsStore} from "@/stores/credentials.module";
import type Team from "@/models/team.model";
import type User from "@/models/user.model";

const ApiService = useApiService();
const CredentialsStore = useCredentialsStore();

const tournaments = ref<Tournament[] | null>(null);
const tournamentsLoading = ref<boolean | null>(true);

const user = ref<User | null>(null);
const userLoading = ref<boolean | null>(true);

const teams = ref<Team[] | null>(null);
const teamsLoading = ref<boolean | null>(true);

onMounted(() => {
  const urlSearchParamsTournaments = new URLSearchParams([["store__isnull", "false"]]);
  ApiService.getTournaments(urlSearchParamsTournaments).then(result => {
    tournaments.value = result;
    tournamentsLoading.value = false;
  }).catch(() => {
    tournamentsLoading.value = null;
  });

  if (CredentialsStore.loggedIn) {
    const userPromise = ApiService.getUsersMe().then(userData => {
      user.value = userData;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });

    userPromise.then(() => {
      if (user.value !== null) {
        ApiService.getChallengesTeams(new URLSearchParams([["members", String(user.value.id)]])).then(result => {
          teams.value = result;
          teamsLoading.value = false;
        }).catch(() => {
          teamsLoading.value = null;
        })
      } else {
        teamsLoading.value = false;
      }
    });
  } else {
    userLoading.value = false;
    teamsLoading.value = false;
  }
});

function getAmountOfCoinsForTournament(tournament: Tournament): number {
  if (teams.value === null) {
    return null;
  }

  for (let i = 0; i < teams.value.length; i++) {
    const currentTeam: Team = teams.value[i];
    if (currentTeam.tournament.id === tournament.id) {
      if (currentTeam.coins_account !== null) {
        return currentTeam.coins_account.balance;
      } else {
        return null;
      }
    }
  }
  return null;
}
</script>

<template>
  <Header :show-back-button="false"/>
  <div class="feed-container mx-auto">
    <Loader v-if="tournamentsLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="tournamentsLoading === null" class="alert alert-warning">
      Failed to load tournaments, please try again.
    </div>
    <div v-else-if="tournaments !== null && tournaments.length === 0" class="alert alert-warning mx-1">
      There are currently no available stores.
    </div>
    <StoreCard v-else v-for="tournament in tournaments" v-bind:tournament="tournament" v-bind:balance="getAmountOfCoinsForTournament(tournament)" v-bind:key="tournament" />
  </div>
</template>

<style scoped>

</style>