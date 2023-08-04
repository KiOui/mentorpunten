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
    console.log(tournaments)
  });
</script>

<template>
    <div class="mt-5">
        <TournamentCard v-for="tournament in tournaments" v-bind:tournament="tournament" v-bind:key="tournament.id" />
    </div>
</template>
