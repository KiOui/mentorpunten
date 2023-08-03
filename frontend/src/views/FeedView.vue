<script setup lang="ts">
  import Header from "@/components/Header.vue";
  import SubmissionsList from "@/components/SubmissionsList.vue";
</script>

<template>
  <Header title="Mentorpunten"/>
  <div class="container mt-5">
    <SubmissionsList v-bind:submission-search-filters="[['accepted', 'true']]" v-bind:show-accepted="false"/>
  </div>
</template>
