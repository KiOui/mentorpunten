<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Tournament from "@/models/tournament.model";
    import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

    defineProps<{tournament: Tournament}>();
</script>

<template>
    <div class="mt-1 py-2 px-4">
        <div class="row">
            <h1>{{ tournament.name }}</h1>
        </div>
        <div class="row">
            <h3>{{ tournament.active_from }} until {{ tournament.active_until }}</h3>
        </div>
    </div>
</template>

<style scoped>

</style>