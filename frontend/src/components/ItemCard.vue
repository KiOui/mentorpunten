<script setup lang="ts">
    import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
    import type Item from "@/models/item.model";
    import type Team from "@/models/team.model";
    import useApiService from "@/common/api.service";
    import {ref} from "vue";
    import {useToast} from "vue-toastification";

    const emit = defineEmits(['ItemCard-afterBuyItem'])

    const props = defineProps<{item: Item, team: Team | null}>();

    const ApiService = useApiService();
    const toast = useToast();

        const buyingItem = ref<boolean>(false);

    function buyItem(item: Item) {
      if (confirm(`Are you sure you want to buy ${item.name} for ${item.price} coins?`)) {
        if (props.team !== null) {
          buyingItem.value = true;
          const formData = new FormData();
          formData.append("property_of", String(props.team.id));
          formData.append("item", String(item.id));
          ApiService.postItem(formData).then((result) => {
            toast.success(`Bought item ${result.name}!`);
          }).catch(() => {
            toast.error("An error occurred while buying the item, please try again.");
          }).finally(() => {
            buyingItem.value = false;
            emit('ItemCard-afterBuyItem');
          });
        }
      }
    }
</script>

<template>
  <div class="custom-card">
    <div class="row">
      <div class="col-8">
        <h2 class="m-0">{{ item.name }}</h2>
      </div>
      <div class="col-4 d-flex flex-row justify-content-end align-items-center">
        <font-awesome-icon icon="fa-solid fa-coins" style="color: var(--primary);" class="me-1"/><p>{{ item.price }} coins</p>
      </div>
    </div>
    <p>{{ item.description }}</p>
    <template v-if="team !== null && team.coins_account !== null">
      <button v-if="buyingItem" class="btn btn-primary mt-3">Buy this item <span class="loader ms-1"></span></button>
      <button v-else-if="team.coins_account.balance >= item.price" v-on:click="buyItem(item)" class="btn btn-primary mt-3">Buy this item</button>
      <button v-else class="btn btn-primary disabled mt-3">Buy this item</button>
    </template>
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