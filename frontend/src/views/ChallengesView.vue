<script setup lang="ts">
  import ChallengeCard from "@/components/ChallengeCard.vue";
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from 'vue';
  import type Challenge from "@/models/challenge.model";
  import Loader from "@/components/Loader.vue";

  const props = defineProps<{ id: number }>();

  const ApiService = useApiService();
  const challenges = ref<Challenge[] | null>(null);
  const challengesLoading = ref<boolean | null>(true);

  onMounted(() => {
    ApiService.getChallenges(new URLSearchParams([["tournament", String(props.id)]])).then(result => {
      challenges.value = result;
      challengesLoading.value = false;
    }).catch(() => {
      challengesLoading.value = null;
    });
  });
</script>

<template>
  <div class="feed-container mx-auto">
    <Loader v-if="challengesLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="challengesLoading === null" class="alert alert-warning">
      Failed to load challenges, please try again.
    </div>
    <ChallengeCard v-else v-for="challenge in challenges" v-bind:challenge="challenge" v-bind:key="challenge.id" />
  </div>
</template>
