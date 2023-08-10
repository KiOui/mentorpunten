<script setup lang="ts">

import {onMounted, ref} from "vue";
import type Team from "@/models/team.model";
import useApiService from "@/common/api.service";
import TransactionsList from "@/components/TransactionsList.vue";
import Loader from "@/components/Loader.vue";
import Header from "@/components/Header.vue";

const props = defineProps<{id: number}>();

const ApiService = useApiService();

const team = ref<Team | null>(null);
const teamLoading = ref<boolean | null>(true);

onMounted(() => {
  ApiService.getChallengesTeam(props.id).then(result => {
    team.value = result;
    teamLoading.value = false;
  }).catch(() => {
    teamLoading.value = null;
  });
});
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto">
    <Loader v-if="teamLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="teamLoading === null" class="alert alert-warning mx-1">
      There was an error loading this team, please try again.
    </div>
    <TransactionsList v-else-if="!teamLoading && team !== null" v-bind:transaction-search-filters="[['account', String(team.account.id)]]"/>
  </div>
</template>
