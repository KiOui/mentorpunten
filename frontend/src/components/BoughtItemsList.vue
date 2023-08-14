<script setup lang="ts">
import {onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import Loader from "@/components/Loader.vue";
import type BoughtItem from "@/models/boughtitem.model";
import BoughtItemCard from "@/components/BoughtItemCard.vue";

const props = defineProps<{boughtItemsSearchFilters: string[][]}>();

const ApiService = useApiService();

let boughtItems = ref<BoughtItem[]>([]);
let boughtItemsLoading = ref<boolean|null>(true);

onMounted(() => {
  refresh();
});

function refresh() {
  boughtItemsLoading.value = true;
  const urlSearchParameters = new URLSearchParams(props.boughtItemsSearchFilters);
  ApiService.getBoughtItems(urlSearchParameters).then((result) => {
    boughtItems.value = result;
    boughtItemsLoading.value = false;
  }).catch(() => {
    boughtItemsLoading.value = null;
  });
}
</script>

<template>
  <Loader v-if="boughtItemsLoading" size="60px" background-color="#000000"/>
  <div v-else-if="boughtItemsLoading === null" class="alert alert-warning mx-1">
    There was an error loading the team items, please try again.
  </div>
  <template v-else>
    <div v-if="boughtItems.length === 0" class="alert alert-warning mx-1">
      This team has not bought any items yet.
    </div>
    <BoughtItemCard v-else v-for="item in boughtItems" v-bind:key="item.id" v-bind:bought-item="item" v-on:BoughtItemCard-AfterUseItem="refresh"/>
  </template>
</template>

<style scoped>

</style>