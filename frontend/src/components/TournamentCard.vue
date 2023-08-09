<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Tournament from "@/models/tournament.model";
    import {startEndTimeOfTournament} from "@/common/general.service";

    const props = defineProps<{tournament: Tournament}>();

    let current_time = Date.parse(new Date().toISOString());
    
</script>

<template>
    <div v-if="Date.parse(tournament.active_from) > current_time" class="custom-card disabled">
        <h1>{{ tournament.name }}</h1>
        <h3>{{ startEndTimeOfTournament(tournament) }}</h3>
    </div>

    <router-link v-else :to="{ name: 'Challenges', params: { id: tournament.id }}" style="text-decoration: none;">
        <div class="custom-card">
            <h1>{{ tournament.name }}</h1>
            <h3>{{ startEndTimeOfTournament(tournament) }}</h3>
        </div>
    </router-link>
</template>

<style scoped>
</style>