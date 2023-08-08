<script setup lang="ts">

import Header from "@/components/Header.vue";
import type Tournament from "@/models/tournament.model";
import {computed, type ComputedRef, onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import type Team from "@/models/team.model";
import TournamentStatisticsList from "@/components/TournamentStatisticsList.vue";
import {startEndTimeOfTournament} from "@/common/general.service";

const props = defineProps<{ id: number}>();
const ApiService = useApiService();

let tournament = ref<Tournament | null>(null);
let tournamentLoading = ref<boolean | null>(true);

let teams = ref<Team[] | null>(null);
let teamsLoading = ref<boolean | null>(true);

onMounted(() => {
  ApiService.getTournament(props.id).then(result => {
    tournament.value = result;
    tournamentLoading.value = false;
  }).catch(() => {
    tournamentLoading.value = null;
  });

  ApiService.getChallengesTeams(new URLSearchParams([["tournament", String(props.id)]]))
    .then(result => {
      teams.value = result.sort((a, b) => b.account.balance - a.account.balance);
      teamsLoading.value = false;
    }).catch(() => {
      teamsLoading.value = null;
    });
  
  console.log(teams.value);
});

const firstTeam: ComputedRef<Team | null> = computed(() => {
  if (teams.value === null || teams.value.length === 0) {
    return null;
  } else {
    return teams.value[0];
  }
});
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto">
    <div v-if="tournament !== null" class="custom-card text-center">
      <h1>{{ tournament.name }}</h1>
      <h4>{{ startEndTimeOfTournament(tournament) }}</h4>
    </div>
    <div v-else-if="teamsLoading === null" class="alert alert-warning">
      Failed to load tournaments, please try again.
    </div>
    <div v-if="teams?.length === 0" class="alert alert-warning">
      There are currently no teams in this tournament.
    </div>
    <div v-else>
      <div class="d-flex justify-content-between align-items-start first-of-tournament">
        <template v-if="firstTeam !== null">
          <h1>#1 {{ firstTeam.name }}</h1>
          <h1>{{ firstTeam.account.balance }} points</h1>
        </template>
      </div>
      <TournamentStatisticsList v-if="teams !== null" v-bind:teams="teams.slice(1, teams.length)" />
    </div>
  </div>
</template>

<style>
.first-of-tournament {
  color: var(--primary);
  font-family: 'Gill Sans MT Condensed';
  text-transform: uppercase;
  margin: 0;
  margin-top: 1rem;
  background-color: white;
}

.first-of-tournament h1 {
  margin: 0.5rem 1rem;
}
</style>
