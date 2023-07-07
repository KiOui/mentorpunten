<script lang="ts">
import router from '@/router';

</script>

<template>
    <div class="card my-2">
        <router-link :to="{ name: 'challenge', params: { id: 1 } }">
        <div class="card-body">
            <h3 class="card-title">Challenge name</h3>
            <p class="card-text">Challenge description</p>
        </div>
        </router-link>
    </div>
</template>

<style scoped>

</style>