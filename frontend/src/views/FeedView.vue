<script setup lang="ts">
  import {useUserStore} from "@/stores/user.module";
  import useApiService from "@/common/api.service";
  import Header from "@/components/Header.vue";
  import {ref} from "vue";
  import SubmissionCard from "@/components/SubmissionCard.vue";

  const store = useUserStore();
  const ApiService = useApiService(store);

  let feedLoading = ref(true);
  let submissions = ref([]);

  ApiService.getChallengesSubmissions().then(response => {
    if (response.status === 200) {
      return response;
    } else {
      throw response;
    }
  }).then(
      data => data.json()
  ).then(data => {
    submissions.value = data;
    feedLoading.value = false;
  });
</script>

<template>
  <Header title="Mentorpunten"/>
  <SubmissionCard v-for="submission in submissions" submission="submission"/>
</template>
