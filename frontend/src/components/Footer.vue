<script setup lang="ts">
  import { useUserStore } from '@/stores/user.module';
  import useApiService from "@/common/api.service";
  import {onMounted, ref} from "vue";

  const store = useUserStore();
  const ApiService = useApiService(store);

  let user = ref(null);

  function startLogin() {
    console.log("startLogin");
    store.newRandomState();
    store.storeState();
    window.location.href = ApiService.getAuthorizeRedirectURL(
        store.stateKey,
        null,
        false
    );
  }

  onMounted(() => {
    if (!store.loggedIn) {
      return;
    }

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
        <router-link :to="{ name: 'Index' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-images"/>
          </li>
        </router-link>
        <router-link :to="{ name: 'Challenges' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
              <font-awesome-icon icon="fa-solid fa-trophy"/>
          </li>
        </router-link>
        <router-link :to="{ name: 'Statistics' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-chart-line"/>
          </li>
        </router-link>
        <router-link :to="{ name: 'Profile' }" v-if="store.loggedIn" class="text-white nav-item flex-grow-1 text-center">
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