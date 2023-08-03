<script setup lang="ts">

import SubmissionCard from "@/components/SubmissionCard.vue";
import {computed, onMounted, ref} from "vue";
import Submission from "@/models/submission.model";
import {useUserStore} from "@/stores/user.module";
import useApiService from "@/common/api.service";
import {useToast} from "vue-toastification";
import Loader from "@/components/Loader.vue";

const props = defineProps<{submissionSearchFilters: string[][], showAccepted: boolean}>();

const store = useUserStore();
const ApiService = useApiService(store);

const toast = useToast();

let submissions = ref<Submission[]>([]);
let submissionsLoading = ref<boolean|null>(true);
let nextDataExists = ref<boolean>(true);
let limit = ref<number>(20);

onMounted(() => {
  addNewData();
});

defineExpose({
  refresh
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
  <div v-for="(submissionsRow, index) in splittedSubmissions" class="row" v-bind:key="index">
    <div class="col-md" v-for="submission in submissionsRow" v-bind:key="submission.id">
      <SubmissionCard v-bind:submission="submission" v-bind:show-accepted="showAccepted" />
    </div>
    <div v-if="submissionsRow.length < 3" class="col-md"></div>
    <div v-if="submissionsRow.length < 2" class="col-md"></div>
  </div>
  <div v-if="submissions.length === 0 && !submissionsLoading">
    <div class="alert alert-warning">
      Your team has not made any submissions for this challenge yet.
    </div>
  </div>
  <Loader v-if="submissionsLoading" size="60px" background-color="#000000"/>
  <div v-else-if="!submissionsLoading && nextDataExists">
    <button v-on:click="addNewData" class="btn btn-primary">Load more</button>
  </div>
</template>

<style scoped>

</style>