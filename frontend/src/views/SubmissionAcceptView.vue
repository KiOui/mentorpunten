<script setup lang="ts">
import SubmissionAcceptList from "@/components/SubmissionAcceptList.vue";
import Header from "@/components/Header.vue";
</script>

<template>
    <Header :show-back-button="false"/>
    <SubmissionAcceptList :show-accepted="true" :submission-search-filters="[['accepted', 'null']]" no-submissions-warning="No submissions yet."/>
</template>

<style scoped>
.alert-text {
  color: var(--primary);
  font-family: 'Gill sans MT condensed', sans-serif;
  text-decoration: none;
  margin: 0;
}
</style>
