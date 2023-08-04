<script setup lang="ts">
  import ChallengeCard from "@/components/ChallengeCard.vue";
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from 'vue';
  import type Challenge from "@/models/challenge.model";
  import Header from "@/components/Header.vue";

  const ApiService = useApiService();
  let challenges = ref<Challenge[] | null>(null);

  onMounted(() => {
    ApiService.getChallenges().then(result => {
      challenges.value = result;
    });
  });
</script>

<template>
  <Header title="Challenges"/>
  <div class="container mt-5">
    <ChallengeCard v-for="challenge in challenges" v-bind:challenge="challenge" v-bind:key="challenge.id" />
  </div>
</template>
