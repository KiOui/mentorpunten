<script setup lang="ts">
import type Submission from "@/models/submission.model";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {RouterLink} from "vue-router";

defineProps<{submission: Submission, showAccepted: boolean}>();
</script>

<template>
  <div class="card mb-3 overflow-hidden w-100">
    <div class="card-body p-0">
      <div class="d-flex flex-column h-100">
        <div class="row p-3" style="flex-grow: 0">
          <div class="col-8">
            <router-link :to="{ name: 'Team', params: { id: submission.team.id } }">
              <h3 class="card-title d-flex align-items-center">{{ submission.team.name }} <font-awesome-icon icon="fa-solid fa-angle-right" class="fs-6 ms-2 text-secondary"/></h3>
            </router-link>
            <p class="card-subtitle mb-2 text-body-secondary">{{ submission.challenge.name }} - {{ submission.challenge.tournament.name }}</p>
            <template v-if="showAccepted">
              <div v-if="submission.accepted" class="badge bg-success">Accepted</div>
              <div v-else-if="submission.accepted === false" class="badge bg-danger">Denied</div>
              <div v-else class="badge bg-warning">Not processed yet</div>
            </template>
          </div>
          <div class="col-4 text-end">
            <span v-if="submission.transaction !== null && submission.transaction.amount < 0" class="badge bg-danger fs-6">- {{ submission.transaction.amount }} points</span>
            <span v-if="submission.transaction !== null && submission.transaction.amount > 0" class="badge bg-success fs-6">+ {{ submission.transaction.amount }} points</span>
          </div>
        </div>
        <div style="flex-grow: 1" class="d-flex align-items-center">
          <img v-if="submission.image !== null" class="w-100" :src="submission.image"/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>