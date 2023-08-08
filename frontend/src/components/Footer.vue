<script setup lang="ts"> /* eslint-disable-line vue/multi-word-component-names */
import useApiService from '@/common/api.service';
import { useCredentialsStore } from '@/stores/credentials.module';
import { onMounted, ref } from 'vue';
import type User from '@/models/user.model';

const ApiService = useApiService();
const store = useCredentialsStore();

let user = ref<User|null>(null);
let userLoading = ref<boolean|null>(true);

let user_can_change_submission = false;

onMounted(() => {
    const userPromise = ApiService.getUsersMe().then(userData => {
      user.value = userData;
      userLoading.value = false;
    }).catch(() => {
      userLoading.value = null;
    });

    userPromise.then(() => {
      if (user.value !== null) {
        user_can_change_submission = (user.value?.user_permissions.filter(function(x) { return x[1] == 'Can change submission'}).length > 0); 
        console.log(user_can_change_submission);
      } else {
        userLoading.value = false;
      }
    });
    
  }
)
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
        <router-link v-if="user_can_change_submission" :to="{ name: 'SubmissionAccept' }" class="text-white nav-item flex-grow-1 text-center">
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