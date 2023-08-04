<script setup lang="ts">
  import { useCredentialsStore } from '@/stores/credentials.module';
  import useApiService from "@/common/api.service";
  import {computed, type ComputedRef, onMounted, ref, toRaw} from 'vue';
  import type Team from "@/models/team.model";
  import Loader from "@/components/Loader.vue";
  import Header from "@/components/Header.vue";

  const store = useCredentialsStore();
  const ApiService = useApiService();
  const teams = ref<Team[] | null>(null);
  const teamsLoading = ref<boolean>(true);

  onMounted(() => {
    ApiService.getChallengesTeams().then(result => {
      teams.value = result;
      teamsLoading.value = false;
    });
  });

  const sortByBalance = (team1: Team, team2: Team) => {
    return team1.account.balance - team2.account.balance;
  }

  // const teamsSortedBalance: ComputedRef<Team[]> = computed(() => {
  //   const teamsToSort = structuredClone(toRaw(teams.value));
  //   teamsToSort.sort(sortByBalance);
  //   return teamsToSort;
  // });
</script>

<template>
  
</template>
