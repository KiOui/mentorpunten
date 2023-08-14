<script setup lang="ts">

import type Team from '@/models/team.model';

defineProps<{team: Team, index: number}>();
</script>

<template>
  <div class="row w-100 justify-content-between ranking-header">
        <h4 class="col-2 text-center">{{ index+2 }}</h4>
        <router-link :to="{ name: 'Team', params: { id: team.id }}" style="text-decoration: none; color: black; padding: 0;" class="col-8">
          <h4>{{ team.name }}</h4>
        </router-link>
        <h4 class="col-2 text-center">{{ team.points_account.balance }}</h4>
    </div>
</template>

<style scoped>
</style>