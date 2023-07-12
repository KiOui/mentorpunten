<script setup lang="ts">
    import { RouterLink } from 'vue-router'
    import { useUserStore } from '@/stores/user.module';
    import useApiService from "@/common/api.service";
    import { ref, toRef } from 'vue';
    import type Challenge from "@/models/challenge.model";

    const props = defineProps(['id'])

    const store = useUserStore();
    const ApiService = useApiService(store);
    let challenge = ref<Challenge|null>(null);
    const id = toRef(props, 'id');

    ApiService.getChallenge(id.value).then(result => {
        challenge.value = result;
    });
    // console.log(challenge);
</script>

<template>
    <div class="card my-2">
        <div class="card-body">
            <h3 class="card-title">{{ challenge.name }}</h3>
            <p v-if="challenge.description.length<100" class="card-text">{{  challenge.description }}</p>
            <p v-else class="card-text">{{ challenge.description.substring(0,100)+"..." }}</p>
            <router-link :to="{ name: 'Challenge', params: { id: id } }">
                <button class="btn btn-primary">View</button>
            </router-link>
        </div>
    </div>
</template>

<style scoped>

</style>