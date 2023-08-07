<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Challenge from "@/models/challenge.model";

    defineProps<{challenge: Challenge}>();
</script>

<template>
    <router-link :to="{ name: 'Challenge', params: { id: challenge.id }}" style="text-decoration: none;">
        <div class="custom-card">
            <h1 v-if="challenge.completed" class="text-success">{{ challenge.name }}</h1>
            <h1 v-else>{{ challenge.name }}</h1>
            <h3>{{ challenge.points }} points</h3>
            <p v-if="challenge.description.length<100" style="margin-top: 1rem;">{{  challenge.description }}</p>
            <p v-else style="margin-top: 1rem;">{{ challenge.description.substring(0,100)+"..." }}</p>
        </div>
    </router-link>
</template>

<style scoped>

</style>