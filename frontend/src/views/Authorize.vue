<script setup type="ts">
  import { ref, onMounted } from 'vue'
  import { useUserStore} from "@/stores/user.module";

  const store = useUserStore()

  // lifecycle hooks
  onMounted(() => {
    console.log(`The initial count is ${store.credentials}.`)
  })
</script>

<template>
  <div class="container authorize mt-5 text-center">
    <h1 class="font-oswald">Authorization in progress...</h1>
    <p>
      You will be redirected shortly, if redirection fails, please click
      <router-link :to="{ name: 'Index' }">here</router-link>
    </p>
    <div class="d-flex justify-content-center align-items-center">
      <Loader size="60px" background-color="#000000"></Loader>
    </div>
  </div>
</template>

