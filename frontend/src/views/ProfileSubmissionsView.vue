<script setup lang="ts">

import Header from "@/components/Header.vue";
import Loader from "@/components/Loader.vue";
import {onMounted, ref} from "vue";
import type User from "@/models/user.model";
import useApiService from "@/common/api.service";
import SubmissionsList from "@/components/SubmissionsList.vue";
import type Team from "@/models/team.model";
import type Tournament from "@/models/tournament.model";

const props = defineProps<{id: number}>();

const ApiService = useApiService();

const tournament = ref<Tournament | null>(null);
const tournamentLoading = ref<boolean | null>(true);

const user = ref<User | null>(null);
const userLoading = ref<boolean | null>(true);

const team = ref<Team | null>(null);
const teamLoading = ref<boolean | null>(true);

onMounted(() => {
  ApiService.getTournament(props.id).then(result => {
    tournament.value = result;
    tournamentLoading.value = false;
  }).catch(() => {
    tournamentLoading.value = null;
  });

  const userPromise = ApiService.getUsersMe().then(result => {
    user.value = result;
    userLoading.value = false;
  }).catch(() => {
    userLoading.value = null;
  });

  userPromise.then(() => {
    if (user.value !== null) {
      ApiService.getChallengesTeams(new URLSearchParams([['members', String(user.value.id)], ['tournament', String(props.id)]])).then(result => {
        if (result.length > 0) {
          team.value = result[0];
        }
        teamLoading.value = false;
      }).catch(() => {
        teamLoading.value = null;
      })
    } else {
      teamLoading.value = false;
    }
  });
})
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto">
    <Loader v-if="tournamentLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="tournamentLoading === null" class="alert alert-warning">
      An error occurred during loading of tournament data, please try again.
    </div>
    <div v-else-if="!tournamentLoading && tournament !== null" class="custom-card">
      <h1>{{ tournament.name }}</h1>
    </div>
    <Loader v-if="userLoading === true || teamLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="userLoading === null" class="alert alert-warning">
      An error occurred during loading of user data, please try again.
    </div>
    <div v-else-if="teamLoading === null" class="alert alert-warning">
      An error occurred during loading of team data, please try again.
    </div>
    <div v-else-if="!teamLoading && team === null" class="alert alert-info">
      You are not registered for a team in this tournament.
    </div>
    <SubmissionsList v-else-if="!userLoading && user !== null && !teamLoading && team !== null" :show-accepted="true" :submission-search-filters="[['team', String(team.id)], ['tournament', String(props.id)]]" no-submissions-warning="No submissions found for this tournament."/>
  </div>
</template>

<style scoped>
</style>
