<script setup lang="ts">
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from "vue";
  import type Tournament from "@/models/tournament.model";
  import Loader from "@/components/Loader.vue";
  import TournamentStatisticsCard from "@/components/TournamentStatisticsCard.vue";
  import type Team from "@/models/team.model";

  const ApiService = useApiService();

  const tournaments = ref<Tournament[] | null>(null);
  const tournamentsLoading = ref<boolean | null>(true);

  const teams = ref<Team[] | null>(null);
  const teamsLoading = ref<boolean | null>(true);

  onMounted(() => {
    ApiService.getTournaments().then(result => {
      tournaments.value = result;
      tournamentsLoading.value = false;
    }).catch(() => {
      tournamentsLoading.value = null;
    });

    ApiService.getChallengesTeams().then(result => {
      teams.value = result;
      teamsLoading.value = false;
    }).catch(() => {
      teamsLoading.value = null;
    })
  })
</script>

<template>
<<<<<<< HEAD
  <Header :show-back-button="false"/>
=======
  <div class="feed-container my-5 mx-auto">
    <Loader v-if="tournamentsLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="tournamentsLoading === null" class="alert alert-warning">
      Failed to load tournaments, please try again.
    </div>
    <TournamentStatisticsCard v-else-if="!tournamentsLoading && tournaments !== null" v-for="tournament in tournaments" v-bind:tournament="tournament" v-bind:key="tournament.id" />
  </div>
>>>>>>> df059a0e285f8bf274a4353572956728a3c4c3fc
</template>
