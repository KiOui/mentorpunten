<script setup lang="ts">

defineProps({
  title: String,
});

</script>

<template>
  <div class="header text-center py-2">
    <h1>MENTORPUNTEN</h1>
  </div>
</template>

<style scoped>
  .header {
    background-color: var(--nav-background-color);
    color: var(--nav-link-color);
  }

  .header h1{
    font-family: 'Gill sans MT condensed', sans-serif;
    margin-bottom: 0;
  }

  .information-screen {
    background-color: var(--nav-background-color);
    color: var(--nav-link-color);
  }
</style>