<script setup lang="ts">

import SubmissionCard from "@/components/SubmissionCard.vue";
import {computed, onMounted, ref} from "vue";
import type Submission from "@/models/submission.model";
import useApiService from "@/common/api.service";
import {useToast} from "vue-toastification";
import Loader from "@/components/Loader.vue";
import Header from "@/components/Header.vue";

const ApiService = useApiService();

const toast = useToast();

const submission = ref<Submission | null>(null);
const submissionsForSameChallengeAndTeam = ref<Submission[]>([]);
const submissionLoading = ref<boolean|null>(true);

const submissionSearchFilters = new URLSearchParams([["accepted__isnull", "true"]]);

function processSubmission(value: boolean, event: Event) {
  event.preventDefault();
  if (value && hasAcceptedSubmissionForSameChallengeAndTeam.value) {
    if (!confirm("This team already has an accepted submission for this challenge, are you sure you want to grant them points for this submission as well?")) {
      return;
    }
  }

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
      toast.success("Submission processed successfully")
  })

  if(value){
    const pointsForm = document.getElementById("transaction") as HTMLFormElement;
    const pointsFormData = new FormData(pointsForm);
    const pointsData = Object.fromEntries(pointsFormData.entries());
    const transactionFormData = new FormData();
    transactionFormData.append("account", String(submission.value.team.points_account.id));
    transactionFormData.append("amount", pointsData.amount);
    transactionFormData.append("description", "Completed challenge " + submission.value.challenge.name);
    ApiService.postTransaction(transactionFormData).then(() => {
    }).catch(() => {
      toast.error("Failed to add transaction, please try again.")
    });
    if(submission.value.team.coins_account !== null){
      const coinsForm = document.getElementById("transaction") as HTMLFormElement;
      const coinsFormData = new FormData(coinsForm);
      const coinsData = Object.fromEntries()
      transactionFormData.set("account", String(submission.value.team.coins_account.id));
      ApiService.postTransaction(transactionFormData).then(() => {
      }).catch(() => {
        toast.error("Failed to add transaction, please try again.")
      });
    }
  }
}

onMounted(() => {
  ApiService.getUsersMe().then(result => {
    const canChangeSubmissions = result.user_permissions.map((permission) => {
      return permission === 'challenges.change_submission';
    }).reduce((previousValue, currentValue) => {
      return previousValue || currentValue;
    }, false);
    if (!canChangeSubmissions) {
      window.location.href = "/";
    } else {
      refresh();
    }
  }).catch(() => {
    toast.error("Failed to load user data, please try again.")
  });
});

function refresh() {
    submissionLoading.value = true;
    submission.value = null;
    ApiService.getChallengesSubmissions(submissionSearchFilters).then(result => {
      if (result.results.length > 0) {
          submission.value = result.results[0];
          const sameTeamChallengeSubmissions = new URLSearchParams([["team", String(submission.value.team.id)], ["accepted", "true"], ["challenge", String(submission.value.challenge.id)]])
          ApiService.getChallengesSubmissions(sameTeamChallengeSubmissions).then(result => {
            submissionsForSameChallengeAndTeam.value = result.results;
            submissionLoading.value = false;
          }).catch(() => {
            submissionLoading.value = null;
          });
      } else {
        submissionLoading.value = false;
      }
    }).catch(() => {
      toast.error("Failed to load submissions data, please try again.");
      submissionLoading.value = null;
    });
}

const hasAcceptedSubmissionForSameChallengeAndTeam = computed(() => {
  return submissionsForSameChallengeAndTeam.value.filter((currentSubmission) => {
    if (submission.value === null)  {
      return false;
    }

    return currentSubmission.id !== submission.value.id;
  }).length > 0;
});
</script>

<template>
    <Header :show-back-button="false"/>
    <div class="feed-container mx-auto">
      <Loader v-if="submissionLoading" size="60px" background-color="#000000"/>
      <div v-else-if="submissionLoading === null" class="alert alert-warning mx-1">
        Failed to load submission, please try again.
      </div>
      <template v-else>
        <div v-if="submission === null" class="alert alert-warning mx-1">
          There are no new submissions to review!
        </div>
        <template v-else>
          <SubmissionCard :submission="submission" :show-accepted="true"/>
          <div class="submission-card" style="margin-top: 0;">
            <div v-if="hasAcceptedSubmissionForSameChallengeAndTeam" class="alert alert-warning">
              This team already has an accepted submission for this challenge
            </div>
              <form class="row custom-form" id="transaction" ref="form">
                <input type="number" id="amount" name="amount" placeholder="submission.challenge.points" v-model="submission.challenge.points">
                <div class="d-flex flex-row">
                  <div class="flex-grow-1 justify-content-center d-flex">
                    <button class="btn btn-accept" v-on:click="processSubmission(true, $event)">
                      <font-awesome-icon icon="fa-solid fa-check"/>
                    </button>
                  </div>
                  <div class="flex-grow-1 justify-content-center d-flex">
                    <button class="btn btn-reject" v-on:click="processSubmission(false, $event)">
                      <font-awesome-icon icon="fa-solid fa-x"/>
                    </button>
                  </div>
                </div>
              </form>
          </div>
        </template>
      </template>
    </div>
</template>

<style scoped>
.submission-card {
    border-radius: 0;
    border: none;
    background-color: white;
    color: black;
  padding: 0.5rem 1.5rem;
  margin-top: 1rem;

}

.btn-accept {
    color: white;
    background-color: var(--success) !important;
    border-color: var(--success) !important;
    text-transform: uppercase;
    font-family: 'Gill sans MT condensed', sans-serif !important;
    font-size: 1.2rem !important;
    padding: 0 0.75rem !important;
}

.btn-reject {
    color: white;
    background-color: var(--danger) !important;
    border-color: var(--danger) !important;
    text-transform: uppercase;
    font-family: 'Gill sans MT condensed', sans-serif !important;
    font-size: 1.2rem !important;
    padding: 0 0.75rem !important;
}
</style>
