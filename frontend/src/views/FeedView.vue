<script setup lang="ts">
  import {useUserStore} from "@/stores/user.module";
  import useApiService from "@/common/api.service";
  import Header from "@/components/Header.vue";
  import {ref} from "vue";
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
</script>

<template>
  <Header title="Mentorpunten"/>
  <div v-if="feedLoading" class="container">
    <Loader size="60px" background-color="#000000"/>
  </div>
  <div v-else class="container my-5">
    <template v-for="(submission, index) in submissions">

    </template>
    <SubmissionCard v-for="submission in submissions" v-bind:submission="submission" v-bind:key="submission.id"/>
  </div>
</template>
