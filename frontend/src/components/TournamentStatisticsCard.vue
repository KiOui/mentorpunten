<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type Tournament from "@/models/tournament.model";
import type Team from "@/models/team.model";
import {computed} from "vue";

const props = defineProps<{tournament: Tournament, teams: Team[]}>();

const firstThreeTeams = computed(() => {
  return props.teams.slice(0, 3);
});
</script>

<template>
    <router-link :to="{ name: 'TournamentStatistics', params: { id: tournament.id }}" style="text-decoration: none;">
        <div class="custom-card">
            <h1>{{ tournament.name }}</h1>
            <ul>
              <li v-for="(team, index) in firstThreeTeams" v-bind:key="team.id">
                #{{index + 1}}: {{ team.name }}, {{ team.account.balance }} points
              </li>
            </ul>
        </div>
    </router-link>
</template>

<style scoped>
</style>