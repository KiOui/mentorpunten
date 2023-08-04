<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Footer from "@/components/Footer.vue";
import Header from "@/components/Header.vue";
</script>

<template>
  <Header/>
  <RouterView />
  <div class="container py-5" style="background-color: #d9d9d9;"></div>
  <Footer/>
</template>

<style scoped>

</style>
