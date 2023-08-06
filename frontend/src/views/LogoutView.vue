<script setup lang="ts">
import Loader from "@/components/Loader.vue";
import {onMounted} from "vue";
import {useRoute} from "vue-router";
import {LOGOUT_TOKEN_NAME} from "@/common/general.service";
import router from "@/router";
import {useCredentialsStore} from "@/stores/credentials.module";

const route = useRoute();
const CredentialsStore = useCredentialsStore();

onMounted(() => {
  const logoutState = localStorage.getItem(LOGOUT_TOKEN_NAME);
  const nextUrl = Object.keys(route.query).includes('next') ? route.query['next'] : null;
  const logoutQueryParam = Object.keys(route.query).includes('logout') ? route.query['logout'] : null;
  if (logoutState === null || logoutQueryParam === null || logoutState !== logoutQueryParam) {
    return;
  } else {
    CredentialsStore.logOut();
    CredentialsStore.storeState();
    localStorage.removeItem(LOGOUT_TOKEN_NAME);
    if (nextUrl === null || Array.isArray(nextUrl)) {
      router.push('/');
    } else {
      window.location.href = nextUrl;
    }
  }
});
</script>

<template>
  <div class="container authorize mt-5 text-center">
    <h1 class="font-oswald">Logging you out...</h1>
    <p>
      You will be redirected shortly, if redirection fails, please click
      <router-link :to="{ name: 'Index' }">here</router-link>
    </p>
    <div class="d-flex justify-content-center align-items-center">
      <Loader size="60px" background-color="#000000"></Loader>
    </div>
  </div>
</template>

<style scoped>

</style>