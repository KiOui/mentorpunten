<script setup lang="ts">

import type Transaction from "@/models/transaction.model";

defineProps<{transaction: Transaction}>();
</script>

<template>
  <div class="d-flex justify-content-between align-items-start" style="margin-top: 0.25rem;">
    <h4>{{ transaction.description }}</h4>
    <h4 v-if="transaction.amount < 0">- {{ transaction.amount * -1 }}</h4>
    <h4 v-else-if="transaction.amount > 0">+ {{ transaction.amount }}</h4>
    <h4 v-else>{{ transaction.amount }}</h4>
  </div>
</template>

<style scoped>

</style>