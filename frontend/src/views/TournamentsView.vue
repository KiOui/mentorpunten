<script setup lang="ts">
  import TournamentCard from "@/components/TournamentCard.vue";
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from 'vue';
  import type Tournament from "@/models/tournament.model";
  import Loader from "@/components/Loader.vue";

  const ApiService = useApiService();
  const tournaments = ref<Tournament[] | null>(null);
  const tournamentsLoading = ref<boolean | null>(true);

  onMounted(() => {
    ApiService.getTournaments().then(result => {
      tournaments.value = result;
      tournamentsLoading.value = false;
    }).catch(() => {
      tournamentsLoading.value = null;
    });
  });
</script>

<template>
  <div class="feed-container my-5 mx-auto">
    <Loader v-if="tournamentsLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="tournamentsLoading === null" class="alert alert-warning">
      Failed to load tournaments, please try again.
    </div>
    <TournamentCard v-else v-for="tournament in tournaments" v-bind:tournament="tournament" v-bind:key="tournament.id" />
  </div>
</template>
