<script setup lang="ts">
import {useRouter} from "vue-router";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import useApiService from "@/common/api.service";
import {useCredentialsStore} from "@/stores/credentials.module";

defineProps<{showBackButton: boolean}>();

const CredentialsStore = useCredentialsStore();

const ApiService = useApiService();

function startLogin(): void {
  CredentialsStore.newRandomState();
  CredentialsStore.storeState();
  window.location.href = ApiService.getAuthorizeRedirectURL(
      CredentialsStore.stateKey,
      null,
      false
  );
}

const router = useRouter();

function goBack() {
  if (window.history.state.back !== null) {
    router.back();
  } else {
    router.push("/");
  }
}

</script>

<template>
  <div class="header">
    <div class="feed-container mx-auto d-flex justify-content-between">
      <div class="col-1 d-flex align-items-center" style="padding-left: 1rem;">
        <a v-if="showBackButton" v-on:click="goBack">
          <font-awesome-icon icon="fa-solid fa-arrow-left"/>
        </a>
      </div>
      <div class="col-10">
        <h1 class="text-center">MENTORPUNTEN</h1>
      </div>
      <div class="col-1 d-flex align-items-center">
        <router-link :to="{ name: 'Profile' }" v-if="CredentialsStore.loggedIn" class="text-white">
          <font-awesome-icon icon="fa-solid fa-user"/>
        </router-link>
        <a v-else @click="startLogin">
          <font-awesome-icon icon="fa-solid fa-right-to-bracket"/>
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
  .header {
    background-color: var(--nav-background-color);
    color: var(--nav-link-color);
  }

  .header h1{
    font-family: 'Gill sans MT condensed', sans-serif;
    margin-bottom: 0;
  }

  .information-screen {
    background-color: var(--nav-background-color);
    color: var(--nav-link-color);
  }
</style>