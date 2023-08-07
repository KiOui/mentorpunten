<script setup lang="ts">

import Header from "@/components/Header.vue";
import type Tournament from "@/models/tournament.model";
import {onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import type Team from "@/models/team.model";
import TournamentStatisticsList from "@/components/TournamentStatisticsList.vue";

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
});

function start_end_time(tournament: Tournament): string {
  if (tournament.active_from) {
    const start_date = new Date(tournament.active_from);
    const end_date = new Date(tournament.active_until);
    const today_date = new Date();

    return `${start_date.toLocaleDateString("en-GB")}, ${start_date.toLocaleTimeString(
        "en-GB",
      { hour: "2-digit", minute: "2-digit" }
    )} until ${end_date.toLocaleDateString("en-GB")}, ${end_date.toLocaleTimeString(
        "en-GB",
      { hour: "2-digit", minute: "2-digit" }
    )}`;
  }
  return "";
}

function first_team_name(): string {
  if (teams.value === null) {
    return "";
  }
  if (teams.value.length > 0) {
    return teams.value[0].name;
  }
  return "";
}

function first_team_points(): string {
  if (teams.value === null) {
    return "";
  }
  if (teams.value.length > 0) {
    return teams.value[0].account.balance.toString();
  }
  return "";
}

</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto my-5">
    <div v-if="tournament !== null" class="custom-card text-center">
      <h1>{{ tournament.name }}</h1>
      <h4>{{ start_end_time(tournament) }}</h4>
    </div>
    <div class="d-flex justify-content-between align-items-start first-of-tournament">
      <h1>#1 {{ first_team_name() }}</h1>
      <h1>{{ first_team_points() }} points</h1>
    </div>
    <TournamentStatisticsList v-if="teams !== null" v-bind:teams="teams.slice(1, teams.length)" />
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
