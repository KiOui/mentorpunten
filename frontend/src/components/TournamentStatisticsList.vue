<script setup lang="ts">
import type Team from "@/models/team.model";
import TournamentStatisticsCard from "@/components/TournamentStatisticsCard.vue";

const props = defineProps<{teams: Team[] | null}>();

</script>

<template>
  <div class="custom-card">
    <div class="row w-100 justify-content-between ranking-header">
        <h4 class="col-2 text-center">place</h4>
        <h4 class="col-8">team</h4>
        <h4 class="col-2 text-center">points</h4>
    </div>
    <div v-if="props.teams !== null" class="row">
        <div v-if="props.teams.length === 0" class="alert alert-info mt-3 mb-2">
          No other teams in this tournament.
        </div>
        <TournamentStatisticsCard v-else v-for="team in props.teams" v-bind:team="team" v-bind:key="team.id" v-bind:index="props.teams.indexOf(team)"/>
    </div>
  </div>
</template>

<style scoped>
</style>