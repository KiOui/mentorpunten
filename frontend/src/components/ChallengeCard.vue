<script setup lang="ts">
    const props = defineProps(['id'])

    import { RouterLink } from 'vue-router'
    import { useUserStore } from '@/stores/user.module';
    import useApiService from "@/common/api.service";
    import { ref, toRef } from 'vue';

    const store = useUserStore();
    const ApiService = useApiService(store);
    let challenge = ref(null);
    const id = toRef(props, 'id');

    ApiService.getChallenge(id.value).then(response => {
    if (response.status === 200) {
        return response;
    } else {
        throw response;
    }
    }).then(
        result => result.json()
    ).then(data => {
        challenge.value = data;
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