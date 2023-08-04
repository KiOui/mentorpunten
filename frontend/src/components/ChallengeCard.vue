<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import type Challenge from "@/models/challenge.model";
    import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

    defineProps<{challenge: Challenge}>();
</script>

<template>
    <!-- <div class="card my-2">
        <div class="card-body">
          <div class="row">
            <div class="col-8">
              <h3 class="card-title">{{ challenge.name }} <span v-if="challenge.completed" class="text-success"><font-awesome-icon icon="fa-solid fa-check"/></span></h3>
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
    </div> -->
    <router-link :to="{ name: 'Challenge', params: { id: challenge.id }}" style="text-decoration: none;">
        <div class="custom-card">
            <h1>{{ challenge.name }}</h1>
            <h3>{{ challenge.points }} points</h3>
        </div>
    </router-link>
</template>

<style scoped>

</style>