<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type Tournament from "@/models/tournament.model";
import type Team from "@/models/team.model";
import {computed} from "vue";
import {startEndTimeOfTournament} from "@/common/general.service";

const props = defineProps<{tournament: Tournament, teams: Team[], userTeam: null | Team}>();

const tournamentPosition = computed(() => {
  if (props.userTeam === null) {
    return null;
  }

  for (let i = 0; i < props.teams.length; i++) {
    const currentTeam = props.teams[i];
    if (currentTeam.id === props.userTeam.id) {
      return i + 1;
    }
  }

  return null;
});
</script>

<template>
    <router-link :to="{ name: 'TournamentStatistics', params: { id: tournament.id }}" style="text-decoration: none;">
        <div class="custom-card">
          <h1>{{ tournament.name }}</h1>
          <h3>{{ startEndTimeOfTournament(tournament) }}</h3>
          <h6 v-if="tournamentPosition !== null">current position: {{ tournamentPosition }}</h6>
        </div>
    </router-link>
</template>

<style scoped>
</style>