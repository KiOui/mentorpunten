<script setup lang="ts">
import type BoughtItem from "@/models/boughtitem.model";
import useApiService from "@/common/api.service";
import {ref} from "vue";
import {useToast} from "vue-toastification";

defineProps<{boughtItem: BoughtItem}>();

const emit = defineEmits(['BoughtItemCard-afterUseItem'])

const ApiService = useApiService();

const toast = useToast();

const loading = ref<boolean>(false);

function useItem(item: BoughtItem) {
  if (item.used) {
    return;
  }

  if (confirm(`Are you sure you want to use ${item.name}?`)) {
    loading.value = true;
    const formData = new FormData();
    formData.append("used", "true");
    ApiService.patchBoughtItem(item.id, formData).then(() => {
      toast.success(`Successfully used item ${item.name}!`);
    }).catch(() => {
      toast.error(`Failed to use ${item.name}, please try again.`);
    }).finally(() => {
      emit('BoughtItemCard-afterUseItem');
    });
  }
}
</script>

<template>
  <div class="custom-card" :class="{ disabled: boughtItem.used }">
    <div class="row">
      <div class="col-md-8">
        <h2>{{ boughtItem.name }}</h2>
      </div>
      <div class="col-md-4 d-flex justify-content-md-end align-items-center mb-md-0 mb-2">
        <div v-if="boughtItem.used" class="badge bg-danger">
          Used
        </div>
        <div v-else class="badge bg-success">
          Not used
        </div>
      </div>
    </div>
    <p class="fst-italic mb-3" style="font-size: 10pt;">Bought for {{ boughtItem.price }} coins</p>
    <p>
      {{ boughtItem.description }}
    </p>
    <button v-if="loading" class="btn btn-primary disabled">
      Use this item <span class="loader"></span>
    </button>
    <button v-else-if="!boughtItem.used" v-on:click="useItem(boughtItem)" class="btn btn-primary">
      Use this item
    </button>
  </div>
</template>

<style scoped>
.loader {
  width: 20px;
  height: 20px;
  padding: 0;
  border: 2px solid var(--text-color);
  border-bottom-color: var(--background-shade);
  border-radius: 50%;
  display: inline-block;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>