<script setup lang="ts">
  import ChallengeCard from "@/components/ChallengeCard.vue";
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from 'vue';
  import type Challenge from "@/models/challenge.model";

  const ApiService = useApiService();
  let challenges = ref<Challenge[] | null>(null);

  onMounted(() => {
    ApiService.getChallenges().then(result => {
      challenges.value = result;
      console.log(challenges.value);
    });
  });
</script>

<template>
  <ChallengeCard v-for="challenge in challenges" v-bind:challenge="challenge" v-bind:key="challenge.id" />
</template>
