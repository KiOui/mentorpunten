<script setup lang="ts">
import { RouterLink } from 'vue-router'
import type Tournament from "@/models/tournament.model";
import type Team from "@/models/team.model";
import {computed} from "vue";
import {ref} from "vue";
import type User from "@/models/user.model";
import useApiService from "@/common/api.service";

const props = defineProps<{tournament: Tournament, teams: Team[]}>();

const ApiService = useApiService();

let user = ref<User|null>(null);
let userLoading = ref<boolean|null>(true);

let userteams = ref<Team[]|null>(null);
let userteamsLoading = ref<boolean|null>(true);

const firstThreeTeams = computed(() => {
  return props.teams.slice(0, 3);
});

function getTournamentPosition(): number {
  const userPromise = ApiService.getUsersMe().then(userData => {
    user.value = userData;
    userLoading.value = false;
  }).catch(() => {
    userLoading.value = null;
  });

  userPromise.then(() => {
    if (user.value !== null) {
      ApiService.getChallengesTeams(new URLSearchParams([["members", String(user.value.id)]])).then(result => {
        userteams.value = result;
        userteamsLoading.value = false;
      }).catch(() => {
        userteamsLoading.value = null;
      })
    } else {
      userteamsLoading.value = false;
    }
  });

  

  for(let i=0; userteams.value?.length; i++) {
    // console.log(userteams.value[i].tournament.id, props.tournament.id)
    if(userteams.value[i].tournament.id == props.tournament.id) {
      // console.log(props.teams.indexOf(userteams.value[i]));
      if(userteams.value === null) {
        return 0;
      }
      let id = userteams.value[i].id;
      let team = props.teams.find((team) => team.id === id)
      // console.log(team);
      if(team === undefined) {
        return 0;
      }
      return (props.teams.indexOf(team) + 1);
    }
  }

  return 0;
}

function start_end_time(tournament: Tournament): string {
  if (tournament.active_from) {
    const start_date = new Date(tournament.active_from);
    const end_date = new Date(tournament.active_until);
    const today_date = new Date();

    return `${start_date.toLocaleDateString("en-GB")}, ${start_date.toLocaleTimeString(
        "en-GB",
      { hour: "2-digit", minute: "2-digit" }
    )} until ${end_date.toLocaleDateString("en-GB")}, ${end_date.toLocaleTimeString(
        "en-GB",
      { hour: "2-digit", minute: "2-digit" }
    )}`;
  }
  return "";
}
</script>

<template>
    <router-link :to="{ name: 'TournamentStatistics', params: { id: tournament.id }}" style="text-decoration: none;">
        <div class="custom-card">
          <h1>{{ tournament.name }}</h1>
          <h3>{{ start_end_time(tournament) }}</h3>
          <h6>current position: {{ getTournamentPosition() }}</h6>
        </div>
    </router-link>
</template>

<style scoped>
</style>