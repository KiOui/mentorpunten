<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Tournament from "@/models/tournament.model";
    import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

    defineProps<{tournament: Tournament, balance: number | null}>();
</script>

<template>
  <router-link :to="{ name: 'Store', params: { id: tournament.store.id }}" style="text-decoration: none;">
    <div class="custom-card">
      <h1>{{ tournament.store.name }}</h1>
      <h3>{{ tournament.name }}</h3>
      <div v-if="balance !== null" class="d-flex flex-row">
        <font-awesome-icon icon="fa-solid fa-coins" style="color: var(--primary);" class="me-1"/><p>{{ balance }} coins</p>
      </div>
    </div>
  </router-link>
</template>

<style scoped>
</style>