<script setup lang="ts">
  import ChallengeCard from "@/components/ChallengeCard.vue";
  import useApiService from "@/common/api.service";
  import {computed, onMounted, ref} from 'vue';
  import type Challenge from "@/models/challenge.model";
  import Loader from "@/components/Loader.vue";
  import Header from "@/components/Header.vue";

  const props = defineProps<{ id: number }>();

  const ApiService = useApiService();
  const challenges = ref<Challenge[] | null>(null);
  const challengesLoading = ref<boolean | null>(true);

  onMounted(() => {
    ApiService.getChallenges(new URLSearchParams([["tournament", String(props.id)], ["ordering", "active,active_from,active_until,name"]])).then(result => {
      challenges.value = result;
      challengesLoading.value = false;
    }).catch(() => {
      challengesLoading.value = null;
    });
  });

  function challengeHasPassed(challenge: Challenge) {
    if (challenge.active_until === null) {
      return false;
    }

    return Date.parse(challenge.active_until) < Date.parse(new Date().toISOString());
  }

  function challengeStartsInFuture(challenge: Challenge) {
    if (challenge.active_from === null) {
      return false;
    }

    return Date.parse(challenge.active_from) > Date.parse(new Date().toISOString())
  }

  function challengeIsActive(challenge: Challenge) {
    return !challengeHasPassed(challenge) && !challengeStartsInFuture(challenge);
  }

  function challengeIsNotActive(challenge: Challenge) {
    return challengeHasPassed(challenge) || challengeStartsInFuture(challenge);
  }

  const challengesActive = computed(() => {
    if (challenges.value === null) {
      return null;
    }

    return challenges.value.filter((challenge) => {
      return challengeIsActive(challenge);
    });
  });

  const challengesLockedInThePast = computed(() => {
    if (challenges.value === null) {
      return null;
    }

    return challenges.value.filter((challenge) => {
      return !challenge.completed && challengeHasPassed(challenge);
    });
  });

  const challengesLockedInTheFuture = computed(() => {
    if (challenges.value === null) {
      return null;
    }

    return challenges.value.filter((challenge) => {
      return !challenge.completed && challengeStartsInFuture(challenge);
    });
  });

  const challengesDoneAndLocked = computed(() => {
    if (challenges.value === null) {
      return null;
    }

    return challenges.value.filter((challenge) => {
      return challenge.completed && challengeIsNotActive(challenge);
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
    <template v-else>
      <ChallengeCard v-for="challenge in challengesActive" v-bind:challenge="challenge" v-bind:key="challenge.id" />
      <ChallengeCard v-for="challenge in challengesLockedInTheFuture" v-bind:challenge="challenge" v-bind:key="challenge.id" />
      <ChallengeCard v-for="challenge in challengesDoneAndLocked" v-bind:challenge="challenge" v-bind:key="challenge.id" />
      <ChallengeCard v-for="challenge in challengesLockedInThePast" v-bind:challenge="challenge" v-bind:key="challenge.id" />
    </template>
  </div>
</template>

<style scoped>
.alert {
  margin-top: 1rem;
}
</style>
