<script setup lang="ts">
  import {useUserStore} from "@/stores/user.module";
  import useApiService from "@/common/api.service";
  import Loader from "@/components/Loader.vue";
  import {computed, ref} from "vue";
  import {onMounted} from "vue";
  import Header from "@/components/Header.vue";
  import type User from "@/models/user.model";
  import type ChallengeUser from "@/models/challengeUser.model";
  import {useRouter} from "vue-router";
  import type Submission from "@/models/submission.model";
  import SubmissionCard from "@/components/SubmissionCard.vue";

  let user = ref<User|null>(null);
  let group = ref<ChallengeUser|null>(null);
  let userLoading = ref<boolean|null>(true);
  let groupLoading = ref<boolean|null>(true);
  let submissions = ref<Submission[]|null>(null);
  let submissionsLoading = ref<boolean|null>(true);

  const router = useRouter();

  const store = useUserStore();
  const ApiService = useApiService(store);

  function logout() {
    store.logOut();
    store.storeState();
    router.push("/");
  }

  onMounted(() => {
    if (!store.loggedIn) {
      return;
    }

    ApiService.getUsersMe().then(userData => {
      user.value = userData;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });

    refreshSubmissions();
  });

  function _refreshSubmissions(groupData: ChallengeUser) {
    if (groupData.team === null) {
      submissions.value = [];
      submissionsLoading.value = false;
    } else {
      ApiService.getChallengesSubmissions(new URLSearchParams({
        team: groupData.team.id,
      })).then(result => {
        submissions.value = result.filter(
            (submission) => {
              return submission.image !== null;
            }
        ).reverse();
        submissionsLoading.value = false;
      }).catch(() => {
        submissionsLoading.value = null;
      });
    }
  }

  function refreshSubmissions() {
    submissionsLoading.value = true;
    submissions.value = null;
    if (group.value === null) {
      groupLoading.value = true;
      ApiService.getChallengesUsersMe().then(challengeUserData => {
        group.value = challengeUserData;
        _refreshSubmissions(challengeUserData);
      }).catch(() => {
        groupLoading.value = null;
      });
    } else {
      _refreshSubmissions(group.value);
    }
  }

  const splittedSubmissions = computed(() => {
    if (submissions.value === null) {
      return null;
    }
    return submissions.value.reduce((result: Submission[][], item: Submission, index: number) => {
      const chunkIndex = Math.floor(index / 3);
      if (!result[chunkIndex]) {
        result[chunkIndex] = [];
      }
      result[chunkIndex].push(item);
      return result;
    }, [])
  });
</script>

<template>
  <Header title="Profile"/>
  <div class="container mt-5">
    <div v-if="user !== null" class="profile-data text-center">
      <div class="profile-image m-auto" :style="{ 'background-image': `url(${user.profile_image})` }"></div>
      <h2 class="mt-2">{{ user.display_name }}</h2>
    </div>
    <Loader v-else-if="userLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="userLoading === null" class="alert alert-warning">
      Failed to load user data, please try again.
    </div>
    <div class="d-flex justify-content-center">
      <button v-on:click="logout()" type="button" class="btn btn-danger mx-auto">Logout</button>
    </div>
    <hr>
    <div class="group-data text-center">
      <h3 class="mt-4 mb-4 text-center">Group</h3>
      <div v-if="group !== null">
        <div v-if="group.team === null" class="alert alert-info">
          You are not part of any team yet. Please contact an administrator to be assigned to a team.
        </div>
        <p v-else>You are in <strong>{{ group.team.name }}</strong></p>
      </div>
      <Loader v-else-if="groupLoading === true" size="60px" background-color="#000000"/>
      <div v-else-if="groupLoading === null" class="alert alert-warning">
        Failed to load group data, please try again.
      </div>
    </div>
    <hr>
    <div class="upload-data">
      <h3 class="mt-4 mb-4 text-center">Uploaded pictures</h3>
      <div v-if="submissions !== null && group !== null && group.team !== null">
        <div v-for="(submissionsRow, index) in splittedSubmissions" class="row" v-bind:key="index">
          <div class="col-md d-flex align-items-stretch" v-for="submission in submissionsRow" v-bind:key="submission.id">
            <SubmissionCard v-bind:submission="submission" v-bind:show-accepted="true"/>
          </div>
          <div v-if="submissionsRow.length < 3" class="col-md"></div>
          <div v-if="submissionsRow.length < 2" class="col-md"></div>
        </div>
      </div>
      <div v-else-if="submissions !== null && group !== null && group.team === null" class="alert alert-info">
        You are not in a team yet so there are no recently uploaded pictures to show.
      </div>
      <Loader v-else-if="submissionsLoading === true" size="60px" background-color="#000000"/>
      <div v-else-if="submissionsLoading === null" class="alert alert-warning">
        Failed to load submissions data, please try again.
      </div>
    </div>
  </div>
</template>

<style scoped>
  .profile-image {
    height: 100px;
    width: 100px;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    border-radius: 100%;
  }
</style>
