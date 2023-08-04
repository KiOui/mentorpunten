<script setup lang="ts">

import type Transaction from "@/models/transaction.model";

defineProps<{transaction: Transaction}>();
</script>

<template>
  <div class="d-flex justify-content-between align-items-start">
    <p>{{ transaction.description }}</p>
    <span v-if="transaction.amount < 0" class="badge bg-danger fs-6">- {{ transaction.amount * -1 }}</span>
    <span v-else-if="transaction.amount > 0" class="badge bg-success fs-6">+ {{ transaction.amount }}</span>
    <span v-else class="badge bg-info fs-6">{{ transaction.amount }}</span>
  </div>
</template>

<style scoped>

</style>