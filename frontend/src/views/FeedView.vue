<script setup lang="ts">
  import {useUserStore} from "@/stores/user.module";
  import useApiService from "@/common/api.service";
  import Header from "@/components/Header.vue";
  import {computed, ref} from "vue";
  import SubmissionCard from "@/components/SubmissionCard.vue";
  import type Submission from "@/models/submission.model";
  import Loader from "@/components/Loader.vue";

  const store = useUserStore();
  const ApiService = useApiService(store);

  let feedLoading = ref<boolean>(true);
  let submissions = ref<Submission[]>([]);

  ApiService.getChallengesSubmissions().then(result => {
    submissions.value = result;
    feedLoading.value = false;
  });

  const splittedSubmissions = computed(() => {
    return submissions.value.reduce((result: Submission[][], item: Submission, index: number) => {
      const chunkIndex = Math.floor(index / 3);
      if (!result[chunkIndex]) {
        result[chunkIndex] = [];
      }
      result[chunkIndex].push(item);
      return result;
    }, [])
  })
</script>

<template>
  <Header title="Mentorpunten"/>
  <div v-if="feedLoading" class="container">
    <Loader size="60px" background-color="#000000"/>
  </div>
  <div v-else class="container my-5">
    <div v-for="(submissionsRow, index) in splittedSubmissions" class="row" v-bind:key="index">
      <div class="col-md" v-for="submission in submissionsRow" v-bind:key="submission.id">
        <SubmissionCard v-bind:submission="submission"/>
      </div>
      <div v-if="submissionsRow.length < 3" class="col-md"></div>
      <div v-if="submissionsRow.length < 2" class="col-md"></div>
    </div>
  </div>
</template>
