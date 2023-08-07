<script lang="ts" setup>
import {useCredentialsStore} from '@/stores/credentials.module';
import useApiService from "@/common/api.service";
import {onMounted, ref, toRef} from 'vue';
import type Challenge from "@/models/challenge.model";
import Loader from "@/components/Loader.vue";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {useToast} from "vue-toastification";
import Header from "@/components/Header.vue";
import type User from "@/models/user.model";
import type Team from "@/models/team.model";
import SubmissionsList from "@/components/SubmissionsList.vue";

const props = defineProps<{ id: number }>();

const submissionsList = ref();

const toast = useToast();

const store = useCredentialsStore();
const ApiService = useApiService();

let challengeLoading = ref<boolean | null>(true);
let challenge = ref<Challenge | null>(null);

let uploadingImage = ref<boolean>(false);
const id = toRef(props, 'id');

const imageFile = ref<File | null>(null);
const imageField = ref<HTMLInputElement | null>(null);

let user = ref<User|null>(null);
let userLoading = ref<boolean|null>(true);

let userTeam = ref<Team|null>(null);
let userTeamLoading = ref<boolean|null>(true);

onMounted(() => {
  ApiService.getChallenge(id.value).then(result => {
    challenge.value = result;
    challengeLoading.value = false;
  }).catch(() => {
    challengeLoading.value = null;
  });

  const userPromise = ApiService.getUsersMe().then(result => {
    user.value = result;
    userLoading.value = false;
  }).catch(() => {
    userLoading.value = null;
  });

  userPromise.then(() => {
    if (userLoading.value === false && user.value !== null) {
      ApiService.getChallengesTeams(new URLSearchParams([["members", String(user.value.id)]])).then(result => {
        if (result.length > 0) {
          userTeam.value = result[0];
        }
        userTeamLoading.value = false;
      }).catch(() => {
        userTeamLoading.value = null;
      });
    } else {
      userTeamLoading.value = false;
    }
  });
});

function changeImageFile(event: Event) {
  const files: FileList | null = (<HTMLInputElement>event.target).files;
  if (files === null || files.length === 0) {
    return;
  }
  imageFile.value = files[0];
}

function startUpload() {
  if (challenge.value !== null && imageFile.value !== null && userTeam.value !== null) {
    uploadingImage.value = true;
    const formData = new FormData();
    formData.append("challenge", String(challenge.value.id));
    formData.append("image", imageFile.value, imageFile.value.name);
    formData.append("team", String(userTeam.value.id));
    ApiService.postChallengesSubmissions(formData).then(() => {
      toast.success("Image successfully submitted!");
      submissionsList.value.refresh();
    }).catch(() => {
      toast.error("Image submission failed, please try again");
    }).finally(() => {
      imageFile.value = null;
      if (imageField.value !== null) {
        imageField.value.value = "";
      }
      uploadingImage.value = false;
    });
  }
}
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto my-5">
    <div v-if="challenge !== null" class="custom-card">
      <div class="row">
        <div class="col-8">
          <h1 class="card-title">{{ challenge.name }}</h1>
        </div>
        <div class="col-4 text-end">
          <h1><span v-if="challenge.completed" class="text-success"><font-awesome-icon icon="fa-solid fa-check"/></span></h1>
        </div>
      </div>
      <h3>{{ challenge.points }} points</h3>
      <p style="margin-top: 1rem;">{{ challenge.description }}</p>
      <form v-if="store.loggedIn && !challenge.completed" class="input-group mt-3">
        <label for="image" class="w-100 mb-2" style="font-family: 'Open sans condensed';">Make a picture</label>
        <input v-on:change="changeImageFile($event)" ref="imageField" type="file" class="form-control" id="image"
               capture="user" accept="image/*" aria-label="Upload">
        <button v-if="!uploadingImage" v-on:click="startUpload()" class="btn btn-primary" type="button">Submit</button>
        <button v-else class="btn btn-primary disabled" type="button">Submit</button>
      </form>
      <div v-else-if="challenge.completed" class="alert alert-success" style="margin-top: 1rem;">
        You have already completed this challenge, no submissions are possible anymore.
      </div>
    </div>
    <Loader v-else-if="challengeLoading === true" size="60px" background-color="#000000"/>
    <div v-else class="container mt-5">
      <div class="alert alert-warning">
        Failed to load challenge, please try again.
      </div>
    </div>
    <div v-if="store.loggedIn" class="container mt-5">
      <h2>Submissions</h2>
      <div v-if="challengeLoading === null" class="alert alert-warning">
        Failed loading challenge data, please try again.
      </div>
      <div v-else-if="userTeamLoading === null" class="alert alert-warning">
        Failed loading team data, please try again.
      </div>
      <template v-else-if="challenge !== null && userTeam !== null">
        <SubmissionsList ref="submissionsList" :show-accepted="true" :submission-search-filters="[['team', String(userTeam.id)], ['challenge', String(challenge.id)]]" :no-submissions-warning="'Your team has not made any submissions for this challenge yet.'"/>
      </template>
    </div>
  </div>
</template>

<style scoped>

</style>