<script setup lang="ts">
  import ChallengeCard from "@/components/ChallengeCard.vue";
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from 'vue';
  import type Challenge from "@/models/challenge.model";
  import Loader from "@/components/Loader.vue";
  import Header from "@/components/Header.vue";

  const props = defineProps<{ id: number }>();

  const ApiService = useApiService();
  const challenges = ref<Challenge[] | null>(null);
  const challengesLoading = ref<boolean | null>(true);

  onMounted(() => {
    ApiService.getChallenges(new URLSearchParams([["tournament", String(props.id)], ["ordering", "active_from,active_until,name"]])).then(result => {
      challenges.value = result.filter(function(challenge) {
      if (challenge.active_until !== null){
        return !(Date.parse(String(challenge.active_until)) < Date.parse(new Date().toISOString()));
      } else {
        return true;
      }
    });
      challengesLoading.value = false;
    }).catch(() => {
      challengesLoading.value = null;
    });
  });
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto">
    <Loader v-if="challengesLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="challengesLoading === null" class="alert alert-warning mx-1">
      Failed to load challenges, please try again.
    </div>
    <div v-else-if="challenges?.length === 0" class="alert alert-warning mx-1">
      There are no challenges for this tournament yet.
    </div>
    <ChallengeCard v-else v-for="challenge in challenges" v-bind:challenge="challenge" v-bind:key="challenge.id" />
  </div>
</template>

<style scoped>
.alert {
  margin-top: 1rem;
}
</style>
