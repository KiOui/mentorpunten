<script setup lang="ts">
import {useRouter} from "vue-router";
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";

const props = defineProps<{showBackButton: boolean}>();

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
  <a v-if="showBackButton" v-on:click="goBack" style="position:absolute; margin-left: 1rem; margin-top: 0.75rem; color: white;">
    <font-awesome-icon icon="fa-solid fa-arrow-left"/>
  </a>
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