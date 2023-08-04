<script lang="ts" setup>
import {useRouter} from "vue-router";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

const router = useRouter();

function goBack() {
  if (window.history.state.back !== null) {
    router.back();
  } else {
    router.push("/");
  }
}
</script>

<template>
  <div class="w-100 back-button-wrapper py-2">
    <nav class="feed-container mx-auto">
      <a v-on:click="goBack">
        <font-awesome-icon icon="fa-solid fa-arrow-left"/>
      </a>
    </nav>
  </div>
</template>

<style scoped>
.back-button-wrapper {
  background-color: var(--primary);
  color: var(--text-color);
}
</style>