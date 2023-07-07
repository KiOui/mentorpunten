<script setup lang="ts">
  import {useUserStore} from "@/stores/user.module";
  import useApiService from "@/common/api.service";

  const store = useUserStore();
  const ApiService = useApiService(store);

  ApiService.getUsersMe().then(result => {
    return result.json();
  }).then(data => {
    console.log(data);
  })
</script>

<template>
  <main>

  </main>
</template>
