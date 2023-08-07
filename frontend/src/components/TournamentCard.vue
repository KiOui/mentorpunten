<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Tournament from "@/models/tournament.model";
    import {startEndTimeOfTournament} from "@/common/general.service";

    defineProps<{tournament: Tournament}>();
    
</script>

<template>
    <router-link :to="{ name: 'Challenges', params: { id: tournament.id }}" style="text-decoration: none;">
        <div class="custom-card">
            <h1>{{ tournament.name }}</h1>
            <h3>{{ startEndTimeOfTournament(tournament) }}</h3>
        </div>
    </router-link>
</template>

<style scoped>
</style>