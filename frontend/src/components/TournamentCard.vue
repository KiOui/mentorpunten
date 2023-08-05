<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Tournament from "@/models/tournament.model";
    import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

    defineProps<{tournament: Tournament}>();

    function start_end_time(tournament: Tournament): string {
      if (tournament.active_from) {
        const start_date = new Date(tournament.active_from);
        const end_date = new Date(tournament.active_until);
        const today_date = new Date();

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
    <router-link :to="{ name: 'Challenges', params: { id: tournament.id }}" style="text-decoration: none;">
        <div class="custom-card">
            <h1>{{ tournament.name }}</h1>
            <h3>{{ start_end_time(tournament) }}</h3>
        </div>
    </router-link>
</template>

<style scoped>
</style>