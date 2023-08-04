<script setup lang="ts">
import SubmissionsList from "@/components/SubmissionsList.vue";
</script>

<template>
  <div class="text-center py-2 bg-white">
    <h1 class="alert-text">SUBMIT A CHALLENGE</h1>
  </div>
  <div class="feed my-4 mx-auto">
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

.feed {
  max-width: 630px;
}
</style>
