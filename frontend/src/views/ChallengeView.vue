<script lang="ts" setup>
    const props = defineProps(['id'])

    import { RouterLink } from 'vue-router'
    import { useUserStore } from '@/stores/user.module';
    import useApiService from "@/common/api.service";
    import { ref, toRef } from 'vue';
    import Navbar from "@/components/Navbar.vue";

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


    
</script>

<template>
    <Navbar/>
    <div class="container pt-2">
        <div class="card my-2">
            <div class="card-body">
                <h3 class="card-title">{{ challenge.name }}</h3>
                <p class="card-text">{{ challenge.description }}</p>
                <form action="" method="post" class="input-group">
                    <input type="file" class="form-control" id="inputGroupFile" aria-describedby="inputGroupFileAddon" aria-label="Upload">
                    <button class="btn btn-primary" type="button" id="inputGroupFileAddon">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>