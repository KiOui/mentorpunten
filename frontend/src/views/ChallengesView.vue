<script setup lang="ts">
  import ChallengeCard from "@/components/ChallengeCard.vue";
  import {useUserStore} from "@/stores/user.module";
  import useApiService from "@/common/api.service";

  const store = useUserStore();
  const ApiService = useApiService(store);

  ApiService.getUsersMe();
</script>

<template>
  <main>
    <div class="container">
      <ChallengeCard/>
      <ChallengeCard/>
      <ChallengeCard/>
    </div>
  </main>
</template>
