<script setup lang="ts">
  import { useCredentialsStore } from "@/stores/credentials.module";
  import useApiService from "@/common/api.service";
  import Loader from "@/components/Loader.vue";
  import {computed, ref} from "vue";
  import {onMounted} from "vue";
  import Header from "@/components/Header.vue";
  import type User from "@/models/user.model";
  import type ChallengeUser from "@/models/challengeUser.model";
  import {useRouter} from "vue-router";
  import type Submission from "@/models/submission.model";
  import SubmissionCard from "@/components/SubmissionCard.vue";

  let user = ref<User|null>(null);
  let group = ref<ChallengeUser|null>(null);
  let userLoading = ref<boolean|null>(true);
  let groupLoading = ref<boolean|null>(true);
  let submissions = ref<Submission[]|null>(null);
  let submissionsLoading = ref<boolean|null>(true);

  const router = useRouter();

  const store = useCredentialsStore();
  const ApiService = useApiService();

  function logout() {
    store.logOut();
    store.storeState();
    router.push("/");
  }

  onMounted(() => {
    if (!store.loggedIn) {
      return;
    }

    ApiService.getUsersMe().then(userData => {
      user.value = userData;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });

    // refreshSubmissions();
  });

  // function _refreshSubmissions(groupData: ChallengeUser) {
  //   if (groupData.team === null) {
  //     submissions.value = [];
  //     submissionsLoading.value = false;
  //   } else {
  //     ApiService.getChallengesSubmissions(new URLSearchParams({
  //       team: groupData.team.id,
  //     })).then(result => {
  //       submissions.value = result.filter(
  //           (submission) => {
  //             return submission.image !== null;
  //           }
  //       ).reverse();
  //       submissionsLoading.value = false;
  //     }).catch(() => {
  //       submissionsLoading.value = null;
  //     });
  //   }
  // }

  // function refreshSubmissions() {
  //   submissionsLoading.value = true;
  //   submissions.value = null;
  //   if (group.value === null) {
  //     groupLoading.value = true;
  //     ApiService.getChallengesUsersMe().then(challengeUserData => {
  //       group.value = challengeUserData;
  //       _refreshSubmissions(challengeUserData);
  //     }).catch(() => {
  //       groupLoading.value = null;
  //     });
  //   } else {
  //     _refreshSubmissions(group.value);
  //   }
  // }

  const splittedSubmissions = computed(() => {
    if (submissions.value === null) {
      return null;
    }
    return submissions.value.reduce((result: Submission[][], item: Submission, index: number) => {
      const chunkIndex = Math.floor(index / 3);
      if (!result[chunkIndex]) {
        result[chunkIndex] = [];
      }
      result[chunkIndex].push(item);
      return result;
    }, [])
  });
</script>

<template>
  
</template>

<style scoped>
  .profile-image {
    height: 100px;
    width: 100px;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    border-radius: 100%;
  }
</style>
