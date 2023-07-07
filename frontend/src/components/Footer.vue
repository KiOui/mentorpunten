<script setup lang="ts">
  import { useUserStore } from '@/stores/user.module';
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from "vue";

  const store = useUserStore();
  const ApiService = useApiService(store);

  let user = ref(null);

  function startLogin() {
    store.newRandomState();
    store.storeState();
    window.location.href = ApiService.getAuthorizeRedirectURL(
        store.stateKey,
        null,
        false
    );
  }

  onMounted(() => {
    ApiService.getUsersMe().then(response => {
      if (response.status === 200) {
        return response;
      } else {
        throw response;
      }
    }).then(
        result => result.json()
    ).then(data => {
      user.value = data;
      console.log(user);
    });
  });
</script>

<template>
  <nav class="navbar fixed-bottom">
    <div class="container">
      <ul class="navbar-nav w-100 d-flex justify-content-center flex-row">
        <li class="nav-item flex-grow-1 text-center">
          <font-awesome-icon icon="fa-solid fa-images"/>
        </li>
        <li class="nav-item flex-grow-1 text-center">
          <font-awesome-icon icon="fa-solid fa-trophy"/>
        </li>
        <li class="nav-item flex-grow-1 text-center">
          <font-awesome-icon icon="fa-solid fa-chart-line"/>
        </li>
        <li v-if="store.loggedIn" class="nav-item flex-grow-1 text-center">
          <font-awesome-icon icon="fa-solid fa-user"/>
        </li>
        <li v-else class="nav-item flex-grow-1 text-center">
          <a href="#" @click="startLogin" class="nav-item">
            <font-awesome-icon icon="fa-solid fa-right-to-bracket"/>
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>

</style>