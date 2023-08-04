<script setup lang="ts">
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

// const TournamentStore = useTournamentStore();
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
  // selectedTournament.value = TournamentStore.tournament;

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
    // TournamentStore.removeSelectedTournament();
    // TournamentStore.storeState();
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

// function changeSelectedTournament() {
//   if (tournamentSelectorValue.value === null) {
//     TournamentStore.removeSelectedTournament();
//   } else {
//     const tournament = getTournamentById(tournamentSelectorValue.value);
//     if (tournament === null) {
//       TournamentStore.removeSelectedTournament();
//     } else {
//       TournamentStore.storeNewTournament(tournament);
//     }
//   }
//   TournamentStore.storeState();
// }

function tournamentIsActive(tournament: Tournament) {
  const currentDate = new Date();
  const startDate = new Date(tournament.active_from);
  const endDate = new Date(tournament.active_until);
  return startDate <= currentDate && currentDate < endDate;
}
</script>

<template>
  
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