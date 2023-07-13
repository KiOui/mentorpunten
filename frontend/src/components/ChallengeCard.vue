<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Challenge from "@/models/challenge.model";

    defineProps<{challenge: Challenge}>();
</script>

<template>
    <div class="card my-2">
        <div class="card-body">
          <div class="row">
            <div class="col-8">
              <h3 class="card-title">{{ challenge.name }}</h3>
            </div>
            <div class="col-4 text-end">
              <span class="badge bg-success fs-6">{{ challenge.points }} points</span>
            </div>
          </div>
            <p v-if="challenge.description.length<100" class="card-text">{{  challenge.description }}</p>
            <p v-else class="card-text">{{ challenge.description.substring(0,100)+"..." }}</p>
            <router-link :to="{ name: 'Challenge', params: { id: challenge.id } }">
                <button class="btn btn-primary">View</button>
            </router-link>
        </div>
    </div>
</template>

<style scoped>

</style>