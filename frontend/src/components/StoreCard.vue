<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Tournament from "@/models/tournament.model";
    import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

    defineProps<{tournament: Tournament, balance: number | null}>();
</script>

<template>
  <router-link :to="{ name: 'Store', params: { id: tournament.id }}" style="text-decoration: none;">
    <div class="custom-card">
      <div class="row">
        <div class="col-md-8">
          <h1>{{ tournament.name }}</h1>
        </div>
        <div class="col-md-4 d-flex justify-content-md-end align-items-center mb-md-auto mb-2">
          <div class="badge" style="background-color: var(--primary);">Item store</div>
        </div>
      </div>
      <div v-if="balance !== null" class="d-flex flex-row">
        <font-awesome-icon icon="fa-solid fa-coins" style="color: var(--primary);" class="me-1"/><p>{{ balance }} coins</p>
      </div>
    </div>
  </router-link>
</template>

<style scoped>
</style>