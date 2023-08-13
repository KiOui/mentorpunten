<script setup lang="ts">
    import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
    import type Item from "@/models/item.model";

    defineProps<{item: Item}>();
</script>

<template>
  <div class="custom-card">
    <h2>{{ item.name }}</h2>
    <h3>{{ item.description }}</h3>
    <div class="d-flex flex-row">
      <font-awesome-icon icon="fa-solid fa-coins" style="color: var(--primary);" class="me-1"/><p>{{ item.price }} coins</p>
    </div>
  </div>
</template>

<style scoped>
</style>