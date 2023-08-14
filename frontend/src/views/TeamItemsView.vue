<script setup lang="ts">

import {computed, onMounted, ref} from "vue";
import type Team from "@/models/team.model";
import useApiService from "@/common/api.service";
import Loader from "@/components/Loader.vue";
import Header from "@/components/Header.vue";
import type User from "@/models/user.model";
import {useCredentialsStore} from "@/stores/credentials.module";
import BoughtItemsList from "@/components/BoughtItemsList.vue";

const props = defineProps<{id: number}>();

const ApiService = useApiService();
const CredentialsStore = useCredentialsStore();

const team = ref<Team | null>(null);
const teamLoading = ref<boolean | null>(true);

const user = ref<User | null>(null);
const userLoading = ref<boolean | null>(true);

onMounted(() => {
  ApiService.getChallengesTeam(props.id).then(result => {
    team.value = result;
    teamLoading.value = false;
  }).catch(() => {
    teamLoading.value = null;
  });

  if (CredentialsStore.loggedIn) {
    ApiService.getUsersMe().then((result) => {
      user.value = result;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });
  } else {
    userLoading.value = false;
  }
});

const userIsInTeam = computed(() => {
  if (team.value === null || user.value === null) {
    return false;
  }

  return team.value.members.map((member) => {
    return user.value.id !== null && member.id === user.value.id;
  }).reduce((previousValue, currentValue) => {
    return previousValue || currentValue;
  }, false);
});
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto">
    <Loader v-if="teamLoading === true || userLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="teamLoading === null" class="alert alert-warning mx-1">
      There was an error loading this team, please try again.
    </div>
    <div v-else-if="userLoading === null" class="alert alert-warning mx-1">
      There was an error loading the user, please try again.
    </div>
    <div v-else-if="!userIsInTeam" class="alert alert-warning mx-1">
      You are not in this team so you are not able to see the bought items of this team.
    </div>
    <BoughtItemsList v-else-if="!teamLoading && team !== null" v-bind:bought-items-search-filters="[['team', String(team.id)]]"/>
  </div>
</template>
