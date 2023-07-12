<script setup lang="ts">
defineProps({
  title: String,
});
</script>

<template>
  <nav class="navbar header">
    <div class="container">
      <h1 class="text-center w-100">{{ title }}</h1>
    </div>
  </nav>
</template>

<style scoped>
  .header {
    background-color: var(--nav-background-color);
    color: var(--nav-link-color);
  }
</style>