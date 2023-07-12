<script setup lang="ts">
  import {useUserStore} from "@/stores/user.module";
  import useApiService from "@/common/api.service";
  import Loader from "@/components/Loader.vue";
  import {ref} from "vue";
  import {onMounted} from "vue";
  import Header from "@/components/Header.vue";
  import type User from "@/models/user.model";
  import type ChallengeUser from "@/models/challengeUser.model";

  let user = ref<User|null>(null);
  let group = ref<ChallengeUser|null>(null);
  let userDataLoading = ref(true);
  let groupDataLoading = ref(true);
  let uploadDataLoading = ref(true);

  const store = useUserStore();
  const ApiService = useApiService(store);

  onMounted(() => {
    if (!store.loggedIn) {
      return;
    }

    ApiService.getUsersMe().then(userData => {
      user.value = userData;
      userDataLoading.value = false;
    });

    ApiService.getChallengesUsersMe().then(challengeUserData => {
      group.value = challengeUserData;
      groupDataLoading.value = false;
    });
  });
</script>

<template>
  <Header title="Profile"/>
  <div class="container mt-5">
    <Loader v-if="userDataLoading" size="60px" background-color="#000000"/>
    <div v-else class="profile-data text-center">
      <div class="profile-image m-auto" :style="{ 'background-image': `url(${user.profile_image})` }"></div>
      <h2 class="mt-2">{{ user.display_name }}</h2>
    </div>
    <hr>
    <div class="group-data text-center">
      <h3 class="mt-2 text-center">Group</h3>
      <Loader v-if="groupDataLoading" size="60px" background-color="#000000"/>
      <div class="v-else">
      </div>
    </div>
    <hr>
    <div class="upload-data">
      <h3 class="mt-2 text-center">Uploaded pictures</h3>
      <Loader v-if="uploadDataLoading" size="60px" background-color="#000000"/>
      <div class="v-else">
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
