<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Footer from "@/components/Footer.vue";
</script>

<template>
  <RouterView />
  <div class="my-5"></div>
  <footer>
    <Footer/>
  </footer>
</template>

<style scoped>

</style>
