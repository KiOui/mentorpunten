<script setup lang="ts">
  import TournamentCard from "@/components/TournamentCard.vue";
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from 'vue';
  import type Tournament from "@/models/tournament.model";

  const ApiService = useApiService();
  let tournaments = ref<Tournament[] | null>(null);

  onMounted(() => {
    ApiService.getTournaments().then(result => {
      tournaments.value = result;
    });
  });
</script>

<template>
  <TournamentCard v-for="tournament in tournaments" v-bind:tournament="tournament" v-bind:key="tournament.id" />
</template>
