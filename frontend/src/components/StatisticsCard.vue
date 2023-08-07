<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type Tournament from "@/models/tournament.model";
import type Team from "@/models/team.model";
import {computed} from "vue";
import {ref} from "vue";
import type User from "@/models/user.model";
import useApiService from "@/common/api.service";

const props = defineProps<{tournament: Tournament, teams: Team[], userTeam: null | Team}>();

const firstThreeTeams = computed(() => {
  return props.teams.slice(0, 3);
});

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

function start_end_time(tournament: Tournament): string {
  if (tournament.active_from) {
    const start_date = new Date(tournament.active_from);
    const end_date = new Date(tournament.active_until);

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
</script>

<template>
    <router-link :to="{ name: 'TournamentStatistics', params: { id: tournament.id }}" style="text-decoration: none;">
        <div class="custom-card">
          <h1>{{ tournament.name }}</h1>
          <h3>{{ start_end_time(tournament) }}</h3>
          <h6 v-if="tournamentPosition !== null">current position: {{ tournamentPosition }}</h6>
        </div>
    </router-link>
</template>

<style scoped>
</style>