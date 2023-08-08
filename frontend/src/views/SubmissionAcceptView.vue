<script setup lang="ts">

import SubmissionCard from "@/components/SubmissionCard.vue";
import {onMounted, ref} from "vue";
import type Submission from "@/models/submission.model";
import useApiService from "@/common/api.service";
import {useToast} from "vue-toastification";
import Loader from "@/components/Loader.vue";
import Header from "@/components/Header.vue";

const ApiService = useApiService();

const toast = useToast();

let submission = ref<Submission | null>(null);
let submissionLoading = ref<boolean|null>(true);

let nextDataExists = ref<boolean>(true);
let limit = ref<number>(40);
let submissionSearchFilters = new URLSearchParams([["accepted__isnull", "true"]]);

function processSubmission(value: boolean) {
    const formData = new FormData();
    formData.append("accepted", String(value));
    if (submission.value === null) {
        return;
    }
    ApiService.patchChallengesSubmissions(submission.value.id, formData).then(() => {
        if (submission.value === null) {
            return;
        }
        submission.value.accepted = value;
    }).catch(() => {
        toast.error("Failed to process submission, please try again.")
    }).finally(() => {
        refresh();
    })
}

onMounted(() => {
  refresh();
});

function refresh() {
    submissionLoading.value = true;
    submission.value = null;
    ApiService.getChallengesSubmissions(submissionSearchFilters).then(result => {
    if (result.results.length > 0) {
        submission.value = result.results[0];
    }
    submissionLoading.value = false;
    }).catch(() => {
    toast.error("Failed to load submissions data, please try again.");
    submissionLoading.value = null;
    });
}
</script>

<template>
    <Header :show-back-button="false"/>
    <div v-if="submission === null && !submissionLoading">
        <div class="alert alert-warning" style="margin-top: 2rem;">
            There are no new submissions to review!
        </div>
    </div>
    <!-- <SubmissionAcceptCard v-else-if="submission !== null" v-bind:submission="submission" v-bind:show-accepted="true" v-bind:key="submission.id" v-on:click="refresh" /> -->
    <div v-else-if="submission !== null">
        <SubmissionCard :submission="submission" :show-accepted="true"/>
        <div class="submission-card justify-content-between d-flex flex-row justify-content-center" style="margin-top: 0rem;">
            <div class="flex-grow-1 justify-content-center d-flex">
                <button class="btn btn-accept" v-on:click="processSubmission(true)">
                    <font-awesome-icon icon="fa-solid fa-check"/>
                </button>
            </div>
            <div class="flex-grow-1 justify-content-center d-flex">
                <button class="btn btn-reject" v-on:click="processSubmission(false)">
                    <font-awesome-icon icon="fa-solid fa-x"/>
                </button>
            </div>
        </div>
    </div>
    <Loader v-if="submissionLoading" size="60px" background-color="#000000"/>
    <div v-else-if="!submissionLoading && !nextDataExists && submission !== null" class="alert alert-info text-center" style="margin-top: 1rem;">
        That's it for now! Check back later!
    </div>
</template>

<style scoped>
.submission-card {
    border-radius: 0;
    border: none;
    background-color: white;
    color: black;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;
    margin-top: 1rem;

}

.btn-accept {
    color: white;
    background-color: var(--success) !important;
    border-color: var(--success) !important;
    text-transform: uppercase;
    font-family: 'Gill sans MT condensed' !important;
    font-size: 1.2rem !important;
    padding: 0rem 0.75rem !important;
}

.btn-reject {
    color: white;
    background-color: var(--danger) !important;
    border-color: var(--danger) !important;
    text-transform: uppercase;
    font-family: 'Gill sans MT condensed' !important;
    font-size: 1.2rem !important;
    padding: 0rem 0.75rem !important;
}
</style>
