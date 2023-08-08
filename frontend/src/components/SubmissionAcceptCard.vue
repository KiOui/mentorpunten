<script setup lang="ts">
import type Submission from "@/models/submission.model";
import {RouterLink} from "vue-router";
import SubmissionCard from "./SubmissionCard.vue";
import useApiService from "@/common/api.service";
import {useToast} from "vue-toastification";

const props = defineProps<{submission: Submission, showAccepted: boolean}>();

const ApiService = useApiService();
const toast = useToast();

function processSubmission(value: boolean) {
    const formData = new FormData();
    formData.append("accepted", String(value));
    ApiService.patchChallengesSubmissions(props.submission.id, formData).then(() => {
        props.submission.accepted = value;
    }).catch(() => {
        toast.error("Failed to process submission, please try again.")
    });
}
</script>

<template>
    <SubmissionCard :submission="submission" :show-accepted="showAccepted"/>
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