<script setup lang="ts">
  import useApiService from "@/common/api.service";
  import {computed, onMounted, ref} from "vue";
  import type Tournament from "@/models/tournament.model";
  import Loader from "@/components/Loader.vue";
  import StatisticsCard from "@/components/StatisticsCard.vue";
  import type Team from "@/models/team.model";
  import Header from "@/components/Header.vue";
  import type User from "@/models/user.model";

  const ApiService = useApiService();

  const tournaments = ref<Tournament[] | null>(null);
  const tournamentsLoading = ref<boolean | null>(true);

  const teams = ref<Team[] | null>(null);
  const teamsLoading = ref<boolean | null>(true);

  const user = ref<User | null>(null);
  const userLoading = ref<boolean | null>(true);

  onMounted(() => {
    ApiService.getTournaments().then(result => {
      tournaments.value = result;
      tournamentsLoading.value = false;
    }).catch(() => {
      tournamentsLoading.value = null;
    });

    ApiService.getChallengesTeams().then(result => {
      teams.value = result;
      teamsLoading.value = false;
    }).catch(() => {
      teamsLoading.value = null;
    });

    ApiService.getUsersMe().then(result => {
      user.value = result;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });
  });

  const sortedTeamsPerTournament = computed(() => {
    if (teams.value === null) {
      return {};
    }
    const sortedTeams: { [tournamentId: number]: Team[] } = {};
    for (let i = 0; i < teams.value.length; i++) {
      const currentTeam = teams.value[i];
      if (Object.keys(sortedTeams).includes(String(currentTeam.tournament.id))) {
        sortedTeams[currentTeam.tournament.id] = sortedTeams[currentTeam.tournament.id].concat(currentTeam);
      } else {
        sortedTeams[currentTeam.tournament.id] = [currentTeam];
      }
    }

    const keys = Object.keys(sortedTeams);
    for (let i = 0; i < keys.length; i++) {
      const currentKey = Number(keys[i]);
      sortedTeams[currentKey] = sortedTeams[currentKey].sort((teamA: Team, teamB: Team) => {
        return teamB.account.balance - teamA.account.balance;
      });
    }

    return sortedTeams;
  });

  function userTeamForTournament(tournament: Tournament): Team | null {
    if (user.value === null) {
      return null;
    }

    const sortedTeams = sortedTeamsPerTournament.value[tournament.id];
    if (sortedTeams === undefined) {
      return null;
    }

    for (let i = 0; i < sortedTeams.length; i++) {
      const currentTeam = sortedTeams[i];
      const currentTeamMemberIds = currentTeam.members.map((member) => {
        return member.id;
      });
      if (currentTeamMemberIds.includes(user.value.id)) {
        return currentTeam;
      }
    }

    return null;
  }
</script>

<template>
  <Header :show-back-button="false"/>
  <div class="feed-container mx-auto">
    <Loader v-if="tournamentsLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="tournamentsLoading === null" class="alert alert-warning">
      Failed to load tournaments, please try again.
    </div>
    <StatisticsCard
        v-else-if="!tournamentsLoading && tournaments !== null"
        v-for="tournament in tournaments"
        v-bind:tournament="tournament"
        v-bind:key="tournament.id"
        v-bind:user-team="userTeamForTournament(tournament)"
        v-bind:teams="Object.keys(sortedTeamsPerTournament).includes(String(tournament.id)) ? sortedTeamsPerTournament[tournament.id] : []"/>
  </div>
</template>
