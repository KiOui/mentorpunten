<script setup lang="ts">
import Loader from "@/components/Loader.vue";
import {onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import {LOGOUT_TOKEN_NAME} from "@/common/general.service";
import router from "@/router";
import {useCredentialsStore} from "@/stores/credentials.module";
import Header from "@/components/Header.vue";

const route = useRoute();
const CredentialsStore = useCredentialsStore();

const hasToken = ref<boolean>(true);
const nextUrl = ref<string | null>(null);

function logOut() {
  CredentialsStore.logOut();
  CredentialsStore.storeState();
  localStorage.removeItem(LOGOUT_TOKEN_NAME);
  if (nextUrl.value !== null) {
    window.location.href = nextUrl.value;
  } else {
    window.location.href = '/';
  }
}

function takeBack() {
  router.back();
}

onMounted(() => {
  if (!CredentialsStore.loggedIn) {
    router.push('/');
  }

  nextUrl.value = Object.keys(route.query).includes('next') ? String(route.query['next']) : '/';
  const logoutQueryParam = Object.keys(route.query).includes('logout') ? route.query['logout'] : null;

  const logoutState = localStorage.getItem(LOGOUT_TOKEN_NAME);
  if (logoutState === null || logoutQueryParam === null || logoutState !== logoutQueryParam) {
    hasToken.value = false;
  } else {
    logOut();
  }
});
</script>

<template>
  <Header :show-back-button="false"/>
  <div class="feed-container authorize mt-5 text-center mx-auto">
    <template v-if="hasToken">
      <h1>Logging you out...</h1>
      <p>
        You will be redirected shortly, if redirection fails, please click
        <router-link :to="{ name: 'Index' }" style="text-decoration: none;">here</router-link>
      </p>
      <div class="d-flex justify-content-center align-items-center">
        <Loader size="60px" background-color="#000000"></Loader>
      </div>
    </template>
    <template v-else>
      <h1>Are you sure you want to log out?</h1>
      <div class="d-flex justify-content-center align-items-center">
        <button v-on:click="logOut" class="btn btn-success me-2">Log out</button>
        <button v-on:click="takeBack" class="btn btn-danger">Take me back</button>
      </div>
    </template>
  </div>
</template>

<style scoped>

</style>