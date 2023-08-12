<script setup lang="ts">
import SubmissionsList from "@/components/SubmissionsList.vue";
import Header from "@/components/Header.vue";
import {useCredentialsStore} from "@/stores/credentials.module";
import useApiService from "@/common/api.service";

const CredentialsStore = useCredentialsStore();
const ApiService = useApiService();

function startLogin() {
  CredentialsStore.newRandomState();
  CredentialsStore.storeState();
  window.location.href = ApiService.getAuthorizeRedirectURL(
      CredentialsStore.stateKey,
      null,
      false
  );
}
</script>

<template>
  <Header :show-back-button="false"/>
  <div class="feed-container mx-auto">
    <SubmissionsList v-if="CredentialsStore.loggedIn" :show-accepted="false" :submission-search-filters="[['accepted', 'true']]" no-submissions-warning="No submissions yet, why don't you make the first one?"/>
    <template v-else>
      <div class="alert alert-warning mx-1">
        In order to see submissions, you need to login. You can do so with the button below.
      </div>
      <div class="d-flex justify-content-center">
        <button v-on:click="startLogin()" class="btn btn-primary">Login</button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.alert-text {
  color: var(--primary);
  font-family: 'Gill sans MT condensed', sans-serif;
  text-decoration: none;
  margin: 0;
}
</style>
