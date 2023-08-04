<script setup lang="ts">
  import Header from "@/components/Header.vue";
  import SubmissionsList from "@/components/SubmissionsList.vue";
  import {computed} from "vue";

</script>

<template>
  <router-link :to="{ name: 'Index' }" class="text-white nav-item flex-grow-1 text-center">
    <div class="text-center py-2">
      <h1 class="alert-text">SUBMIT A CHALLENGE</h1>
    </div>
  </router-link>
</template>

<style scoped>
.alert-text {
  color: var(--primary);
  font-family: 'Gill sans MT condensed', sans-serif;
}
</style>
