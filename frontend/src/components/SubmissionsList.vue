<script setup lang="ts">

import SubmissionCard from "@/components/SubmissionCard.vue";
import {onMounted, ref} from "vue";
import type Submission from "@/models/submission.model";
import useApiService from "@/common/api.service";
import {useToast} from "vue-toastification";
import Loader from "@/components/Loader.vue";

const props = defineProps<{submissionSearchFilters: string[][], showAccepted: boolean, noSubmissionsWarning: string}>();

const ApiService = useApiService();

const toast = useToast();

let submissions = ref<Submission[]>([]);
let submissionsLoading = ref<boolean|null>(true);
let nextDataExists = ref<boolean>(true);
let limit = ref<number>(10);

onMounted(() => {
  addNewData();
});

defineExpose({
  refresh
});

function getSubmissionsQueryParameters(): URLSearchParams {
  const limitOffsetPaginationParameters =
    [
      ["limit", String(limit.value)],
      ["offset", String(submissions.value.length)]
    ];
  if (props.submissionSearchFilters) {
    return new URLSearchParams(props.submissionSearchFilters.concat(limitOffsetPaginationParameters));
  } else {
    return new URLSearchParams(limitOffsetPaginationParameters);
  }
}

function addNewData() {
  submissionsLoading.value = true;
  ApiService.getChallengesSubmissions(getSubmissionsQueryParameters()).then(result => {
    nextDataExists.value = result.next !== null;
    submissions.value = submissions.value.concat(result.results);
  }).catch(() => {
    toast.error("Failed to load submissions data, please try again.")
  }).finally(() => {
    submissionsLoading.value = false;
  })
}

function refresh() {
  submissions.value = [];
  addNewData();
}
</script>

<template>
  <div v-if="submissions.length === 0 && !submissionsLoading">
    <div class="alert alert-warning mx-1" style="margin-top: 1rem;">
      {{ noSubmissionsWarning }}
    </div>
  </div>
  <SubmissionCard v-else v-for="submission in submissions" v-bind:submission="submission" v-bind:show-accepted="showAccepted" v-bind:key="submission.id" />
  <Loader v-if="submissionsLoading" size="60px" background-color="#000000"/>
  <div v-else-if="!submissionsLoading && nextDataExists" class="w-100 d-flex justify-content-center" style="margin-top: 1rem;">
    <button v-on:click="addNewData" class="btn btn-primary text-center">Load more</button>
  </div>
  <div v-else-if="!submissionsLoading && !nextDataExists && submissions.length > 0" class="alert alert-info text-center mx-1" style="margin-top: 1rem;">
    That's it for now! Check back later!
  </div>
</template>

<style scoped>

</style>