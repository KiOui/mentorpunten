<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Challenge from "@/models/challenge.model";
    import {startTimeOfChallenge} from "@/common/general.service";
    import {SUBMISSIONS_VISIBLE_ON_ACCEPTED_SUBMISSION} from "@/common/general.service";

    defineProps<{challenge: Challenge}>();

    let current_time = Date.parse(new Date().toISOString());
</script>

<template>
        <div v-if="Date.parse(String(challenge.active_from)) > current_time" class="custom-card disabled">
            <h1 v-if="challenge.completed" class="text-success">{{ challenge.name }}</h1>
            <h1 v-else>{{ challenge.name }}</h1>
            <h3>{{ challenge.points }} points</h3>
            <p style="margin-top: 1rem;">available from {{ startTimeOfChallenge(challenge) }}</p>
        </div>
    <router-link v-else :to="{ name: 'Challenge', params: { id: challenge.id }}" style="text-decoration: none;">
        <div class="custom-card">
          <div v-if="challenge.submission_visibility === SUBMISSIONS_VISIBLE_ON_ACCEPTED_SUBMISSION && !challenge.completed" class="row">
            <div class="col-8">
              <h1 v-if="challenge.completed" class="text-success">{{ challenge.name }}</h1>
              <h1 v-else>{{ challenge.name }}</h1>
            </div>
            <div class="col-4 text-end my-auto">
              <div class="badge bg-danger">
                Submissions hidden
              </div>
            </div>
          </div>
          <template v-else>
            <h1 v-if="challenge.completed" class="text-success">{{ challenge.name }}</h1>
            <h1 v-else>{{ challenge.name }}</h1>
          </template>
          <h3>{{ challenge.points }} points</h3>
          <p v-if="challenge.description.length<100" style="margin-top: 1rem;">{{  challenge.description }}</p>
          <p v-else style="margin-top: 1rem;">{{ challenge.description.substring(0,100)+"..." }}</p>
        </div>
    </router-link>
</template>

<style scoped>

</style>