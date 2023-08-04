<script setup lang="ts">
  import useApiService from "@/common/api.service";
  import {useCredentialsStore} from "@/stores/credentials.module";

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
</script>

<template>
  <nav class="navbar fixed-bottom">
    <div class="container">
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
        <router-link :to="{ name: 'Profile' }" v-if="CredentialsStore.loggedIn" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-user"/>
          </li>
        </router-link>
        <li v-else class="nav-item flex-grow-1 text-center" @click="startLogin">
          <font-awesome-icon icon="fa-solid fa-right-to-bracket"/>
        </li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>

</style>