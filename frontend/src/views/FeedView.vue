<script setup lang="ts">
import SubmissionsList from "@/components/SubmissionsList.vue";
</script>

<template>
  <div class="feed-container mx-auto">
    <SubmissionsList :show-accepted="false" :submission-search-filters="[['accepted', 'true']]" no-submissions-warning="No submissions yet, why don't you make the first one?"/>
  </div>
</template>

<style scoped>
.alert-text {
  color: var(--primary);
  font-family: 'Gill sans MT condensed', sans-serif;
  text-decoration: none;
  margin: 0;
}
</style>
