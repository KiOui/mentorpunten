<script setup lang="ts">
import Header from "@/components/Header.vue";
import {onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import type Store from "@/models/store.model";
import Loader from "@/components/Loader.vue";
import ItemCard from "@/components/ItemCard.vue";

const props = defineProps<{ id: number }>();

const ApiService = useApiService();

const store = ref<Store | null>(null);
const storeLoading = ref<boolean | null>(true);

onMounted(() => {
  ApiService.getStore(props.id).then(result => {
    store.value = result;
    storeLoading.value = false;
  }).catch(() => {
    storeLoading.value = null;
  });
});
</script>

<template>
  <Header :show-back-button="true"/>
  <div class="feed-container mx-auto">
    <Loader v-if="storeLoading === true" size="60px" background-color="#000000"/>
    <div v-else-if="storeLoading === null" class="alert alert-warning">
      Failed to load store, please try again.
    </div>
    <template v-else-if="store !== null">
      <div v-if="store.items.length === 0" class="alert alert-warning">
        No items found in this store.
      </div>
      <ItemCard v-else v-for="item in store.items" v-bind:item="item" v-bind:key="item.id"/>
    </template>
  </div>
</template>

<style scoped>

</style>