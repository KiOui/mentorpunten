<script setup lang="ts">
import type Submission from "@/models/submission.model";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

defineProps<{submission: Submission}>();
</script>

<template>
  <div class="card mb-3">
    <div class="card-body">
      <div class="row">
        <div class="col-8">
          <h3 class="card-title d-flex align-items-center">{{ submission.team.name }} <font-awesome-icon icon="fa-solid fa-angle-right" class="fs-6 ms-2 text-secondary"/></h3>
          <p class="card-subtitle mb-2 text-body-secondary">{{ submission.challenge.name }}</p>
        </div>
        <div class="col-4 text-end">
          <span v-if="submission.transaction !== null && submission.transaction.amount < 0" class="badge bg-danger fs-6">- {{ submission.transaction.amount }} points</span>
          <span v-if="submission.transaction !== null && submission.transaction.amount > 0" class="badge bg-success fs-6">+ {{ submission.transaction.amount }} points</span>
        </div>
      </div>
    </div>
    <img class="card-img-bottom" :src="submission.image"/>
  </div>
</template>

<style scoped>

</style>