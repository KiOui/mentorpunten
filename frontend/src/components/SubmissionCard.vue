<script setup lang="ts">
import type Submission from "@/models/submission.model";
import {RouterLink} from "vue-router";

defineProps<{submission: Submission, showAccepted: boolean}>();
</script>

<template>
  <div class="overflow-hidden w-100 bg-white" style="margin-top: 1rem;">
      <div class="d-flex flex-column h-100">
        <div class="row">
          <div class="col-8 submission-heading">
              <router-link :to="{ name: 'Team', params: { id: submission.team.id } }" style="text-decoration: none;">
                <h3>{{ submission.team.name }}</h3>
              </router-link>
              <router-link :to="{ name: 'Challenge', params: { id: submission.challenge.id } }" style="text-decoration: none;">
                <h4>{{ submission.challenge.name }} - {{ submission.challenge.tournament.name }}</h4>
              </router-link>
              <template v-if="showAccepted">
                <div v-if="submission.accepted" class="badge bg-success">Accepted</div>
                <div v-else-if="submission.accepted === false" class="badge bg-danger">Denied</div>
                <div v-else class="badge bg-warning">Not processed yet</div>
              </template>
          </div>
          <div class="col-4 text-end my-auto" style="padding-right: 1.5rem;">
            <span v-if="submission.transaction !== null && submission.transaction.amount < 0" class="badge bg-danger fs-6">- {{ submission.transaction.amount * -1 }} points</span>
            <span v-if="submission.transaction !== null && submission.transaction.amount > 0" class="badge bg-success fs-6">+ {{ submission.transaction.amount }} points</span>
          </div>
        </div>

        <div style="flex-grow: 1" class="d-flex align-items-center">
          <img v-if="submission.file.file_type.startsWith('image')" class="w-100" :src="submission.file.file"/>
          <video v-else-if="submission.file.file_type.startsWith('video')" controls class="mw-100">
            <source :src="submission.file.file"/>
            Your browser does not support the video tag.
          </video>
        </div>
      </div>
  </div>
</template>

<style scoped>

</style>