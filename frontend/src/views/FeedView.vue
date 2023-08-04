<script setup lang="ts">
  import Header from "@/components/Header.vue";
  import SubmissionsList from "@/components/SubmissionsList.vue";
  import {useTournamentStore} from "@/stores/tournament.module";
  import {computed} from "vue";

  const TournamentStore = useTournamentStore();

  const headerTitle = computed(() => {
    if (TournamentStore.tournament !== null) {
      return TournamentStore.tournament.name;
    } else {
      return "Mentorpunten";
    }
  });
</script>

<template>
  <Header v-bind:title="headerTitle"/>
  <div class="container mt-5">
    <SubmissionsList v-bind:submission-search-filters="[['accepted', 'true']]" v-bind:show-accepted="false" v-bind:no-submissions-warning="'No submissions found'"/>
  </div>
</template>
