<script setup lang="ts">

import SubmissionCard from "@/components/SubmissionCard.vue";
import {computed, onMounted, ref} from "vue";
import type Submission from "@/models/submission.model";
import useApiService from "@/common/api.service";
import {useToast} from "vue-toastification";
import Loader from "@/components/Loader.vue";
import Header from "@/components/Header.vue";
import type Transaction from "@/models/transaction.model";

const ApiService = useApiService();

const toast = useToast();

const submission = ref<Submission | null>(null);
const submissionsForSameChallengeAndTeam = ref<Submission[]>([]);
const submissionLoading = ref<boolean|null>(true);
const pointsForSubmission = ref<number>(0);
const submissionProcessing = ref<boolean>(false);

const submissionSearchFilters = new URLSearchParams([["accepted__isnull", "true"]]);

const hasAcceptedSubmissionForSameChallengeAndTeam = computed(() => {
  return submissionsForSameChallengeAndTeam.value.filter((currentSubmission) => {
    if (submission.value === null)  {
      return false;
    }

    return currentSubmission.id !== submission.value.id;
  }).length > 0;
});

async function addPointsTransactionsToSubmission(submission: Submission) {
  const pointsTransactionFormData = new FormData();
  pointsTransactionFormData.append("account", String(submission.team.points_account.id));
  pointsTransactionFormData.append("amount", String(pointsForSubmission.value));
  pointsTransactionFormData.append("description", "Completed challenge " + submission.challenge.name);
  return ApiService.postTransaction(pointsTransactionFormData).then(result => {
    return result;
  }).catch(() => {
    toast.error("Failed to add points transaction, please refer to the admin page to fix this issue.");
    return null;
  });
}

async function addCoinsTransactionsToSubmission(submission: Submission) {
  if (submission.team.coins_account === null) {
    return null;
  }

  const pointsTransactionFormData = new FormData();
  pointsTransactionFormData.append("account", String(submission.team.coins_account.id));
  pointsTransactionFormData.append("amount", String(pointsForSubmission.value));
  pointsTransactionFormData.append("description", "Completed challenge " + submission.challenge.name);
  return ApiService.postTransaction(pointsTransactionFormData).then(result => {
    return result;
  }).catch(() => {
    toast.error("Failed to add coins transaction, please refer to the admin page to fix this issue.");
    return null;
  });
}

function processSubmission(value: boolean, event: Event) {
  event.preventDefault();

  if (submission.value === null) {
    return;
  }

  if (value && hasAcceptedSubmissionForSameChallengeAndTeam) {
    if (!confirm("This team already has an accepted submission for this challenge, are you sure you want to grant them points for this submission as well?")) {
      return;
    }
  }

  submissionProcessing.value = true;
  const formData = new FormData();
  formData.append("accepted", String(value));

  ApiService.patchChallengesSubmissions(submission.value.id, formData).then((submission) => {
    if (value) {
      // If accepted, also add points transactions.
      const pointsPromise = addPointsTransactionsToSubmission(submission);
      let coinsPromise: Promise<Transaction | null> = Promise.resolve(null);
      if (submission.team.coins_account !== null) {
        coinsPromise = addCoinsTransactionsToSubmission(submission);
      }
      Promise.all([pointsPromise, coinsPromise]).then(([pointsTransaction, coinsTransaction]) => {
        const addTransactionsToSubmissionFormData = new FormData();
        if (pointsTransaction !== null) {
          addTransactionsToSubmissionFormData.append("points_transaction", pointsTransaction.id);
        }

        if (coinsTransaction !== null) {
          addTransactionsToSubmissionFormData.append("coins_transaction", coinsTransaction.id);
        }

        ApiService.patchChallengesSubmissions(submission.id, addTransactionsToSubmissionFormData).then(() => {
          toast.success("Submission processed successfully");
          submissionProcessing.value = false;
          refresh();
        }).catch(() => {
          toast.error("Failed to update transaction data in submission, please refer to the admin page to manually fix the issue.");
          submissionProcessing.value = false;
          refresh();
        });
      });
    } else {
      toast.success("Submission processed successfully");
      submissionProcessing.value = false;
      refresh();
    }
  }).catch(() => {
    toast.error("Failed to process submission, please try again.");
    submissionProcessing.value = false;
    refresh();
  });
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
    pointsForSubmission.value = 0;
    ApiService.getChallengesSubmissions(submissionSearchFilters).then(result => {
      if (result.results.length > 0) {
          submission.value = result.results[0];
          pointsForSubmission.value = submission.value.challenge.points;
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
                <input v-if="submissionProcessing" type="number" id="amount" name="amount" v-bind:value="pointsForSubmission" disabled>
                <input v-else type="number" id="amount" name="amount" v-model="pointsForSubmission">
                <div class="d-flex flex-row">
                  <div class="flex-grow-1 justify-content-center d-flex">
                    <button v-if="submissionProcessing" class="btn btn-accept disabled text-white d-flex justify-content-center align-items-center p-2">
                      <span class="loader"></span>
                    </button>
                    <button v-else class="btn btn-accept" v-on:click="processSubmission(true, $event)">
                      <font-awesome-icon icon="fa-solid fa-check"/>
                    </button>
                  </div>
                  <div class="flex-grow-1 justify-content-center d-flex">
                    <button v-if="submissionProcessing" class="btn btn-reject disabled text-white d-flex justify-content-center align-items-center p-2">
                      <span class="loader"></span>
                    </button>
                    <button v-else class="btn btn-reject" v-on:click="processSubmission(false, $event)">
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
    padding: 0 0.75rem;
}

.btn-reject {
    color: white;
    background-color: var(--danger) !important;
    border-color: var(--danger) !important;
    text-transform: uppercase;
    font-family: 'Gill sans MT condensed', sans-serif !important;
    font-size: 1.2rem !important;
    padding: 0 0.75rem;
}

.loader {
  width: 20px;
  height: 20px;
  padding: 0;
  border: 2px solid var(--text-color);
  border-bottom-color: var(--background-shade);
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
