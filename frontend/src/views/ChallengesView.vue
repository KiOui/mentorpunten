<script setup lang="ts">
  import { RouterLink } from 'vue-router'
  import ChallengeCard from "@/components/ChallengeCard.vue";
  import { useUserStore } from '@/stores/user.module';
  import useApiService from "@/common/api.service";
  import { ref } from 'vue';

  const store = useUserStore();
  const ApiService = useApiService(store);
  let challenges = ref(null);

  ApiService.getChallenges().then(response => {
    if (response.status === 200) {
      return response;
    } else {
      throw response;
    }
  }).then(
      result => result.json()
  ).then(data => {
    challenges.value = data;
  });
  console.log(challenges);
</script>

<template>
  <main>
    <div class="container">
      <ChallengeCard v-for="challenge in challenges" :id="challenge.id"/>
    </div>
  </main>
</template>
