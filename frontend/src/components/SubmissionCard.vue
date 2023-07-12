<script setup lang="ts">
import type Submission from "@/models/submission.model";

defineProps<{submission: Submission}>();
</script>

<template>
  <div class="card mb-3">
    <div class="card-body">
      <h3 class="card-title">{{ submission.team.name }}</h3>
      <p class="card-subtitle mb-2 text-body-secondary">{{ submission.challenge.name }}</p>
    </div>
    <img class="card-img-bottom" :src="submission.image"/>
  </div>
</template>

<style scoped>

</style>