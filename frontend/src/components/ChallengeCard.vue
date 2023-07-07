<script lang="ts">
import router from '@/router';

</script>

<template>
    <div class="card my-2">
        <div class="card-body">
            <h3 class="card-title">Challenge name</h3>
            <p class="card-text">Challenge description</p>
            <router-link :to="{ name: 'Challenge', params: { id: '1' } }">
                <button class="btn btn-primary">View</button>
            </router-link>
        </div>
    </div>
</template>

<style scoped>

</style>