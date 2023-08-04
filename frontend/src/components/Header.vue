<script setup lang="ts">
import {useTournamentStore} from "@/stores/tournament.module";
import {onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import type Tournament from "@/models/tournament.model";
import {useCredentialsStore} from "@/stores/credentials.module";
import Loader from "@/components/Loader.vue";
import {useToast} from "vue-toastification";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import type Team from "@/models/team.model";
import type User from "@/models/user.model";

defineProps({
  title: String,
});

const TournamentStore = useTournamentStore();
const UserStore = useCredentialsStore();
const ApiService = useApiService();
const toast = useToast();

const tournaments = ref<Tournament[] | null>(null);
const tournamentsLoading = ref<boolean | null>(true);
const selectedTournament = ref<Tournament | null>(null);
const tournamentSelectorValue = ref<number | null>(null);

const team = ref<Team | null>(null);
const teamLoading = ref<boolean | null>(true);

const user = ref<User | null>(null);
const userLoading = ref<boolean | null>(true);

onMounted(() => {
  selectedTournament.value = TournamentStore.tournament;

  if (selectedTournament.value !== null) {
    tournamentSelectorValue.value = selectedTournament.value.id;
  }

  ApiService.getTournaments().then(result => {
    tournaments.value = result;
    checkSelectedTournament();
    tournamentsLoading.value = false;
  }).catch(() => {
    tournamentsLoading.value = null;
  });

  if (UserStore.loggedIn) {
    const usersPromise = ApiService.getUsersMe().then(result => {
      user.value = result;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });
    usersPromise.then(() => {
      reloadTeam();
    })
  } else {
    user.value = null;
    userLoading.value = false;
    reloadTeam();
  }
});

function reloadTeam() {
  teamLoading.value = true;
  if (selectedTournament.value !== null && user.value !== null) {
    const teamSearchParameters = [
        ["tournament", String(selectedTournament.value.id)],
        ["members", String(user.value.id)]
    ];
    ApiService.getChallengesTeams(new URLSearchParams(teamSearchParameters)).then(result => {
      if (result.length > 0) {
        team.value = result[0];
      } else {
        team.value = null;
      }
      teamLoading.value = false;
    }).catch(() => {
      teamLoading.value = null;
    });
  } else {
    team.value = null;
    teamLoading.value = false;
  }
}

function selectedTournamentInList(): boolean {
  if (tournaments.value === null || selectedTournament.value === null) {
    return false;
  }

  for (let i = 0; i < tournaments.value.length; i++) {
    const tournament = tournaments.value[i];
    if (tournament.id === selectedTournament.value.id) {
      return true;
    }
  }
  return false;
}

function checkSelectedTournament(): void {
  if (!selectedTournamentInList()) {
    TournamentStore.removeSelectedTournament();
    TournamentStore.storeState();
    toast.warning("Your currently selected Tournament does not exist anymore, please select a different tournament to continue.")
  }
}

function getTournamentById(id: number): Tournament | null {
  if (tournaments.value === null) {
    return null;
  }

  for (let i = 0; i < tournaments.value.length; i++) {
    const tournament = tournaments.value[i];
    if (tournament.id === id) {
      return tournament;
    }
  }

  return null;
}

function changeSelectedTournament() {
  if (tournamentSelectorValue.value === null) {
    TournamentStore.removeSelectedTournament();
  } else {
    const tournament = getTournamentById(tournamentSelectorValue.value);
    if (tournament === null) {
      TournamentStore.removeSelectedTournament();
    } else {
      TournamentStore.storeNewTournament(tournament);
    }
  }
  TournamentStore.storeState();
}

function tournamentIsActive(tournament: Tournament) {
  const currentDate = new Date();
  const startDate = new Date(tournament.active_from);
  const endDate = new Date(tournament.active_until);
  return startDate <= currentDate && currentDate < endDate;
}
</script>

<template>
  <nav class="navbar navbar-dark header">
    <div class="container">
      <h1 class="me-auto">{{ title }}</h1>
      <ul class="header-right navbar-nav">
        <li class="nav-item">
          <button class="navbar-toggler ms-auto" type="button" data-bs-toggle="offcanvas"
                  data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar">
            <span class="navbar-toggler-icon"></span>
          </button>
        </li>
      </ul>
    </div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar"
         aria-labelledby="offcanvasNavbarLabel">
      <div class="offcanvas-header" style="background-color: var(--nav-background-color);">
        <button type="button" class="btn-close btn-close-white ms-auto" data-bs-dismiss="offcanvas"
                aria-label="Close"></button>
      </div>
      <div class="offcanvas-body information-screen">
        <div class="mb-3">
          <h2 class="mb-3">Tournament information</h2>
          <Loader v-if="tournamentsLoading === true" size="60px" background-color="#FFFFFF"/>
          <div v-else-if="tournamentsLoading === null" class="alert alert-warning">
            Failed to load tournament data, please try again.
          </div>
          <div v-else>
            <select class="form-select" v-on:change="changeSelectedTournament" v-model="tournamentSelectorValue">
              <option v-for="tournament in tournaments" v-bind:key="tournament.id" :value="tournament.id">
                {{ tournament.name }}
              </option>
            </select>
          </div>
        </div>
        <div class="mb-3">
          <h2>Team information</h2>
          <div v-if="!UserStore.loggedIn" class="alert alert-info">
            You are not logged in yet, please log in to see your team information.
          </div>
          <Loader v-else-if="teamLoading === true" size="60px" background-color="#FFFFFF"/>
          <div v-else-if="teamLoading === null" class="alert alert-warning">
            Failed to load team data, please try again.
          </div>
          <template v-else>
            <div v-if="team === null" class="alert alert-info">
              You are not in a team yet, ask an administrator to put you in a team.
            </div>
            <p v-else>
              You are in team {{ team.name }}.
            </p>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
  .header {
    background-color: var(--nav-background-color);
    color: var(--nav-link-color);
  }

  .information-screen {
    background-color: var(--nav-background-color);
    color: var(--nav-link-color);
  }
</style>