<script setup lang="ts">
  import Header from "@/components/Header.vue";
  import SubmissionsList from "@/components/SubmissionsList.vue";
  import {computed} from "vue";

</script>

<template>
  <router-link :to="{ name: 'Index' }" class="text-center" style="text-decoration: none;">
    <div class="text-center py-2 bg-white">
      <h1 class="alert-text">SUBMIT A CHALLENGE</h1>
    </div>
  </router-link>
</template>

<style scoped>
.alert-text {
  color: var(--primary);
  font-family: 'Gill sans MT condensed', sans-serif;
  text-decoration: none;
  margin: 0;
}
</style>
