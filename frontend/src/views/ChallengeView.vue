<script lang="ts" setup>
import {useCredentialsStore} from '@/stores/credentials.module';
import useApiService from "@/common/api.service";
import {computed, onMounted, ref, toRef} from 'vue';
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

const videoFile = ref<File | null>(null);
const videoField = ref<HTMLInputElement | null>(null);

let user = ref<User|null>(null);
let userLoading = ref<boolean|null>(true);

let userTeam = ref<Team|null>(null);
let userTeamLoading = ref<boolean|null>(true);

const challengeIsActive = computed(() => {
  if (challenge.value === null) {
    return false;
  }

  const today = new Date();

  if (challenge.value.active_from !== null) {
    const activeFromDate = new Date(challenge.value.active_from);
    if (activeFromDate > today) {
      return false;
    }
  }

  if (challenge.value.active_until !== null) {
    const activeUntilDate = new Date(challenge.value.active_until);
    if (activeUntilDate < today) {
      return false;
    }
  }

  return true;
});

onMounted(() => {
  const challengePromise = ApiService.getChallenge(id.value).then(result => {
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

  Promise.all([userPromise, challengePromise]).then(() => {
    if (userLoading.value === false && user.value !== null && challengeLoading.value === false && challenge.value !== null) {
      ApiService.getChallengesTeams(new URLSearchParams([["members", String(user.value.id)], ["tournament", String(challenge.value.tournament.id)]])).then(result => {
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

function changeImageFile(event: Event): void {
  const htmlInputEvent = event.target as unknown as HTMLInputElement;
  const files: FileList | null = htmlInputEvent.files;
  if (files !== null && files.length > 0) {
    imageFile.value = files[0];
    videoFile.value = null;
    videoField.value = null;
  }
}

function changeVideoFile(event: Event): void {
  const htmlInputEvent = event.target as unknown as HTMLInputElement;
  const files: FileList | null = htmlInputEvent.files;
  if (files !== null && files.length > 0) {
    videoFile.value = files[0];
    imageFile.value = null;
    imageField.value = null;
  }
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

function startDirectUpload({ fileName, fileType }: { fileName: string, fileType: string }) {
  const formData = new FormData();
  formData.append("file_name", fileName);
  formData.append("file_type", fileType);

  return ApiService.postFileUploadStart(formData);
}

async function directUploadDo({ data, file }: { data: any, file: File }) {
  const formData = new FormData();
  
  for (const key in data.fields) {
    formData.append(key, data.fields[key]);
  }

  formData.append("file", file);

  return fetch(data.url, {
    method: "POST",
    body: formData,
    
  }).then(() => Promise.resolve({ fileId: data?.id}));
}

function directUploadFinish({ data }: any) {
  const formData = new FormData();
  console.log(data)
  formData.append("file_id", data?.fileId);

  return ApiService.postFileUploadFinish(formData);
}

function videoUpload() {

  if (challenge.value !== null && videoFile.value !== null && userTeam.value !== null) {
    uploadingImage.value = true;

    startDirectUpload({ fileName: videoFile.value.name, fileType: videoFile.value.type }).then((data) => {
      console.log('data1', data)
      directUploadDo({ data, file: videoFile.value as File }).then((data) => {
        console.log('data2', data)
        directUploadFinish({ data }).then(() => {
          toast.success("Video successfully submitted!");
          submissionsList.value.refresh();
        }).catch(() => {
          toast.error("Video submission failed, please try again");
        }).finally(() => {
          videoFile.value = null;
          if (videoField.value !== null) {
            videoField.value.value = "";
          }
          uploadingImage.value = false;
        });
      });
    });
  }
}
</script>

<template>
  <Header :show-back-button="true" />
  <div class="feed-container mx-auto">
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
      <img v-if="challenge.image" class="img-fluid" :src="challenge.image" alt="Challenge image" style="margin-top: 1rem;">
      <p style="margin-top: 1rem;">{{ challenge.description }}</p>
      <form v-if="store.loggedIn && !challenge.completed && userTeam !== null && challengeIsActive" class="input-group mt-3">
        <label for="image" class="w-100 mb-2" style="font-family: 'Open sans condensed';">Make a picture</label>
        <input v-on:change="changeImageFile($event)" ref="imageField" type="file" class="form-control" id="image"
               capture="user" accept="image/*" aria-label="Upload">

        <label for="video" class="w-100 mb-2" style="font-family: 'Open sans condensed';">Or a video</label>
        <input v-on:change="changeVideoFile($event)" ref="videoField" type="file" class="form-control" id="video"
               capture="user" accept="*" aria-label="Upload">
        
        <button v-if="!uploadingImage" v-on:click="videoUpload()" class="btn btn-primary" type="button">Submit</button>
        <button v-else class="btn btn-primary disabled d-flex justify-content-center align-items-center" type="button">Submit <span class="loader ms-1"></span></button>
      </form>
      <div v-else-if="challenge.completed" class="alert alert-success mt-2 mb-1">
        You have already completed this challenge, no submissions are possible anymore.
      </div>
      <div v-else-if="!challengeIsActive" class="alert alert-warning mt-2 mb-1">
        This challenge is not active.
      </div>
      <div v-else-if="userTeam === null" class="alert alert-info mt-2 mb-1">
        You are not in a team for this tournament so you can not submit pictures.
      </div>
    </div>
    <Loader v-else-if="challengeLoading === true" size="60px" background-color="#000000"/>
    <div v-else class="container mt-5">
      <div class="alert alert-warning">
        Failed to load challenge, please try again.
      </div>
    </div>
    <div v-if="store.loggedIn" class="custom-card" style="margin-top: 1rem; margin-bottom: -1rem;">
      <h1>Submissions</h1>
    </div>
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
</template>

<style scoped>
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