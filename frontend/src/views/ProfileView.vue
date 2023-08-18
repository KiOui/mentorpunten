<script setup lang="ts">
import {useCredentialsStore} from "@/stores/credentials.module";
import useApiService from "@/common/api.service";
import Loader from "@/components/Loader.vue";
import {onMounted, ref} from "vue";
import type User from "@/models/user.model";
import {useRouter} from "vue-router";
import type Team from "@/models/team.model";
import Header from "@/components/Header.vue";
import {getEnvVar, LOGOUT_TOKEN_NAME} from "@/common/general.service";
import CryptoService from "@/common/crypto.service";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

let user = ref<User|null>(null);
  let userLoading = ref<boolean|null>(true);

  let teams = ref<Team[]|null>(null);
  let teamsLoading = ref<boolean|null>(true);

  const router = useRouter();

  const store = useCredentialsStore();
  const ApiService = useApiService();

  function logout() {
    const logoutState = CryptoService.getRandomString(12);
    localStorage.setItem(LOGOUT_TOKEN_NAME, logoutState);
    const backUrl = encodeURIComponent(window.location.href);
    const nextUrl = encodeURIComponent(`${new URL(router.resolve({name: 'Logout'}).href, window.location.origin).href}?logout=${logoutState}`);
    window.location.href = `${getEnvVar('VITE_API_BASE_URI')}${getEnvVar('VITE_API_LOGOUT_URL')}?back=${backUrl}&next=${nextUrl}`;
  }

  onMounted(() => {
    if (!store.loggedIn) {
      router.push("/");
    }

    const userPromise = ApiService.getUsersMe().then(userData => {
      user.value = userData;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });

    userPromise.then(() => {
      if (user.value !== null) {
        ApiService.getChallengesTeams(new URLSearchParams([["members", String(user.value.id)]])).then(result => {
          teams.value = result;
          teamsLoading.value = false;
        }).catch(() => {
          teamsLoading.value = null;
        })
      } else {
        teamsLoading.value = false;
      }
    });

  });
</script>

<template>
  <Header :show-back-button="false"/>
  <div class="feed-container mx-auto">
    <Loader v-if="userLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="userLoading === null" class="alert alert-warning mx-1">
      Failed to load user data, please try again.
    </div>
    <template v-else-if="user !== null">
      <div class="custom-card">
        <div class="d-flex flex-column">
          <div class="d-flex justify-content-center mt-3">
            <div class="profile-image-container" v-bind:style="{'background-image': `url(${user.profile_image})`}">
            </div>
          </div>
        </div>
        <h1 class="text-center">{{ user.display_name }}</h1>
      </div>
      <Loader v-if="teamsLoading === true" size="60px" background-color="#000000"/>
      <div v-else-if="teamsLoading === null" class="alert alert-warning mx-1">
        Failed to load team data, please try again.
      </div>
      <div v-else-if="!teamsLoading && teams !== null && teams.length === 0" class="alert alert-info mx-1">
        You are not in any team yet, contact an administrator to join a team.
      </div>
      <div v-else-if="!teamsLoading && teams !== null" v-for="team in teams" class="custom-card" v-bind:key="team.id">
        <h2>{{ team.tournament.name }}</h2>
        <router-link :to="{ name: 'Team', params: { id: team.id } }" style="text-decoration: none; color: black;"><p class="mb-2">{{ team.name }}</p></router-link>
        <div class="d-flex flex-column">
          <div class="d-flex flex-row">
            <font-awesome-icon icon="fa-solid fa-star" style="color: var(--primary);" class="me-1"/><p>{{ team.points_account.balance }} points</p>
          </div>
          <div v-if="team.coins_account !== null" class="d-flex flex-row">
            <font-awesome-icon icon="fa-solid fa-coins" style="color: var(--primary);" class="me-1"/><p>{{ team.coins_account.balance }} coins</p>
          </div>
        </div>
        <router-link :to="{ name: 'ProfileSubmissions', params: { id: team.tournament.id }}" class="link" style="text-decoration: none;">View Submissions</router-link>
      </div>
    </template>
    <div class="d-flex justify-content-center mx-auto" style="margin-top: 1rem; width: max-content;">
      <router-link :to="{ name: 'FAQ' }" style="text-decoration: none; color: black; margin-left: 0.25rem; margin-right: 0.25rem;">
        <button v-on:click="logout" class="btn btn-primary">F.A.Q.</button>
      </router-link>
      <button v-on:click="logout" class="btn btn-primary" style="margin-left: 0.25rem; margin-right: 0.25rem;">Logout</button>
    </div>
    <div class="d-flex justify-content-center" style="margin-top: 1rem;">
      <p class="source-code">
        <a href="https://github.com/KiOui/mentorpunten">Check out the source code on GitHub</a>
      </p>
    </div>
  </div>
</template>

<style scoped>
.profile-image-container {
  height: 150px;
  width: 150px;
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  border-radius: 100%;
  color: #d9d9d9;
  background-color: #d9d9d9;
}

.alert {
  margin-top: 1rem;
}

.source-code a {
  color: #555555;
  font-size: 10pt;
}
</style>
