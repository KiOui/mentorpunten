<script lang="ts" setup>
import {useCredentialsStore} from '@/stores/credentials.module';
import useApiService from "@/common/api.service";
import {onMounted, ref, toRef} from 'vue';
import type Challenge from "@/models/challenge.model";
import Loader from "@/components/Loader.vue";
import type ChallengeUser from "@/models/challengeUser.model";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import {useToast} from "vue-toastification";
import BackButtonNavBar from "@/components/BackButtonNavBar.vue";

const props = defineProps<{ id: number }>();

const submissionsList = ref();

const toast = useToast();

const store = useCredentialsStore();
const ApiService = useApiService();
let challengeLoading = ref<boolean | null>(true);
let challenge = ref<Challenge | null>(null);
let groupLoading = ref<boolean | null>(true);
let group = ref<ChallengeUser | null>(null);
let uploadingImage = ref<boolean>(false);
const id = toRef(props, 'id');

const imageFile = ref<File | null>(null);
const imageField = ref<HTMLInputElement | null>(null);

onMounted(() => {
  ApiService.getChallenge(id.value).then(result => {
    challenge.value = result;
    challengeLoading.value = false;
  }).catch(() => {
    challengeLoading.value = null;
  });
  if (store.loggedIn) {
    ApiService.getChallengesUsersMe().then(challengeUserData => {
      group.value = challengeUserData;
    }).catch(() => {
      groupLoading.value = null;
    });
  } else {
    groupLoading.value = null;
  }
});

function changeImageFile(event: Event) {
  const files: FileList | null = (<HTMLInputElement>event.target).files;
  if (files === null || files.length === 0) {
    return;
  }
  imageFile.value = files[0];
}

function startUpload() {
  if (challenge.value !== null && imageFile.value !== null) {
    uploadingImage.value = true;
    const formData = new FormData();
    formData.append("challenge", String(challenge.value.id));
    formData.append("image", imageFile.value, imageFile.value.name);
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
  <BackButtonNavBar/>
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
    <SubmissionsList ref="submissionsList" show-accepted="true" submission-search-filters="[['team', String(groupData.team.id)], ['challenge', String(id.value)]]" no-submissions-warning="'Your team has not made any submissions for this challenge yet.'"/>
  </div>
</template>

<style scoped>

</style>