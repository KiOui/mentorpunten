<script setup lang="ts">
import Header from "@/components/Header.vue";
import {onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import type Store from "@/models/store.model";
import Loader from "@/components/Loader.vue";
import ItemCard from "@/components/ItemCard.vue";
import type Tournament from "@/models/tournament.model";
import type User from "@/models/user.model";
import type Team from "@/models/team.model";

const props = defineProps<{ id: number }>();

const ApiService = useApiService();

const tournament = ref<Tournament | null>(null);
const tournamentLoading = ref<boolean | null>(true);

const store = ref<Store | null>(null);
const storeLoading = ref<boolean | null>(null);

const user = ref<User | null>(null);
const userLoading = ref<boolean | null>(true);

const team = ref<Team | null>(null);
const teamLoading = ref<boolean | null>(true);

onMounted(() => {
  const tournamentPromise = ApiService.getTournament(props.id).then((result) => {
    tournament.value = result;
    tournamentLoading.value = false;
  }).catch(() => {
    tournamentLoading.value = null;
  });

  tournamentPromise.then(() => {
    if (tournament.value !== null && tournament.value.store !== null) {
      ApiService.getStore(tournament.value.store).then((result) => {
        store.value = result;
        storeLoading.value = false;
      }).catch(() => {
        storeLoading.value = null;
      });
    } else {
      storeLoading.value = false;
    }
  });

  const userPromise = ApiService.getUsersMe().then(result => {
    user.value = result;
    userLoading.value = false;
  }).catch(() => {
    userLoading.value = null;
    teamLoading.value = false;
  });

  userPromise.then(() => {
    refresh();
  });
});

function refresh() {
  teamLoading.value = true;
  if (user.value !== null) {
    const urlSearchParams = new URLSearchParams([["members", String(user.value.id)], ["tournament", String(props.id)]]);
    ApiService.getChallengesTeams(urlSearchParams).then(result => {
      if (result.length > 0) {
        team.value = result[0];
      }
      teamLoading.value = false;
    }).catch(() => {
      teamLoading.value = null;
    });
  } else {
    teamLoading.value = false;
  }
}
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto">
    <Loader v-if="tournamentLoading === true || storeLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="tournamentLoading === null" class="alert alert-warning">
      Failed to load tournament, please try again.
    </div>
    <div v-else-if="storeLoading === null" class="alert alert-warning">
      Failed to load store, please try again.
    </div>
    <template v-else-if="tournament !== null">
      <div v-if="store === null" class="alert alert-warning mx-1">
        There is no store registered for this tournament so your points can not be spent
      </div>
      <template v-else>
        <div class="custom-card text-center">
          <h1>{{ store.name}}</h1>
          <h4>{{ tournament.name }}</h4>
          <Loader v-if="teamLoading === true" size="60px" background-color="#000000"/>
          <div v-if="team !== null" class="mt-2">
            <p>
              {{ team.name }}
            </p>
            <template v-if="team.coins_account !== null">
              <p>
                <font-awesome-icon icon="fa-solid fa-coins" style="color: var(--primary);"/> {{ team.coins_account.balance }} coins
              </p>
              <router-link :to="{ name: 'Team', params: { id: team.id }}" class="link" style="text-decoration: none;">View Bought Items</router-link>
            </template>
          </div>
        </div>
        <div v-if="store.items.length === 0" class="alert alert-warning mx-1">
          No items found in this store.
        </div>
        <ItemCard v-else v-for="item in store.items" v-on:ItemCard-afterBuyItem="refresh()" v-bind:item="item" v-bind:team="team" v-bind:key="item.id"/>
      </template>
    </template>
  </div>
</template>

<style scoped>

</style>