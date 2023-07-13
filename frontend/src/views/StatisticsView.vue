<script setup lang="ts">
  import { useUserStore } from '@/stores/user.module';
  import useApiService from "@/common/api.service";
  import {computed, ComputedRef, onMounted, ref, toRaw} from 'vue';
  import type Team from "@/models/team.model";
  import Loader from "@/components/Loader.vue";
  import Header from "@/components/Header.vue";

  const store = useUserStore();
  const ApiService = useApiService(store);
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

  const teamsSortedBalance: ComputedRef<Team[]> = computed(() => {
    const teamsToSort = structuredClone(toRaw(teams.value));
    teamsToSort.sort(sortByBalance);
    return teamsToSort;
  });
</script>

<template>
  <Header title="Statistics"/>
  <Loader v-if="teamsLoading" size="60px" background-color="#000000"/>
  <div v-else class="container mt-5">
    <p v-if="teamsSortedBalance.length === 0" class="alert alert-warning">
      There are no teams registered on this website.
    </p>
    <table v-else class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Team</th>
          <th scope="col">Score</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="team in teamsSortedBalance" v-bind:key="team.id">
          <th scope="row">{{ team.name }}</th>
          <th>{{ team.account.balance }}</th>
        </tr>
      </tbody>
    </table>
  </div>
</template>
