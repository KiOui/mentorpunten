<script setup lang="ts"> /* eslint-disable-line vue/multi-word-component-names */
import useApiService from '@/common/api.service';
import {computed, onMounted, ref} from 'vue';
import type User from '@/models/user.model';
import {useCredentialsStore} from "@/stores/credentials.module";

const ApiService = useApiService();
const CredentialsStore = useCredentialsStore();

let user = ref<User|null>(null);
let userLoading = ref<boolean|null>(true);

onMounted(() => {
  if (CredentialsStore.loggedIn) {
    ApiService.getUsersMe().then(userData => {
      user.value = userData;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });
  } else {
    userLoading.value = false;
  }
});

const userCanChangeSubmission = computed(() => {
  if (user.value === null) {
    return false;
  } else {
    return user.value.user_permissions.map((permission) => {
      return permission === 'challenges.change_submission';
    }).reduce((previousValue, currentValue) => {
      return previousValue || currentValue;
    }, false);
  }
});
</script>

<template>
  <nav class="navbar fixed-bottom">
    <div class="feed-container mx-auto w-100">
      <ul class="navbar-nav w-100 d-flex justify-content-center flex-row">
        <router-link :to="{ name: 'Index' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-images"/>
          </li>
        </router-link>
        <router-link :to="{ name: 'Tournaments' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
              <font-awesome-icon icon="fa-solid fa-trophy"/>
          </li>
        </router-link>
        <router-link :to="{ name: 'Statistics' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-chart-line"/>
          </li>
        </router-link>
        <router-link v-if="userCanChangeSubmission" :to="{ name: 'SubmissionAccept' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-check"/>
          </li>
        </router-link>
      </ul>
    </div>
  </nav>
</template>

<style scoped>

</style>