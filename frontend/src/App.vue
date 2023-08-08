<script setup lang="ts">
import { RouterView } from 'vue-router'
import Footer from "@/components/Footer.vue";
import AnnouncementHeader from "@/components/AnnouncementHeader.vue";
</script>

<template>
  <AnnouncementHeader/>
  <RouterView />
  <div class="container py-5" style="background-color: #d9d9d9;"></div>
  <Footer/>
</template>

<style scoped>

</style>
