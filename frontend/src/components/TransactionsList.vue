<script setup lang="ts">
import {onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import {useToast} from "vue-toastification";
import Loader from "@/components/Loader.vue";
import type Transaction from "@/models/transaction.model";
import TransactionCard from "@/components/TransactionCard.vue";

const props = defineProps<{transactionSearchFilters: string[][]}>();

const ApiService = useApiService();

const toast = useToast();

let transactions = ref<Transaction[]>([]);
let transactionsLoading = ref<boolean|null>(true);
let nextDataExists = ref<boolean>(true);
let limit = ref<number>(50);

onMounted(() => {
  addNewData();
});

function getTransactionsQueryParameters(): URLSearchParams {
  const limitOffsetPaginationParameters =
    [
      ["limit", String(limit.value)],
      ["offset", String(transactions.value.length)]
    ];
  if (props.transactionSearchFilters) {
    return new URLSearchParams(props.transactionSearchFilters.concat(limitOffsetPaginationParameters));
  } else {
    return new URLSearchParams(limitOffsetPaginationParameters);
  }
}

function addNewData() {
  transactionsLoading.value = true;
  ApiService.getTransactions(getTransactionsQueryParameters()).then(result => {
    nextDataExists.value = result.next !== null;
    transactions.value = transactions.value.concat(result.results);
  }).catch(() => {
    toast.error("Failed to load transactions data, please try again.")
  }).finally(() => {
    transactionsLoading.value = false;
  })
}
</script>

<template>
  <div class="custom-card">
    <h1>transactions</h1>
    <TransactionCard v-for="transaction in transactions" v-bind:transaction="transaction" v-bind:key="transaction.id" />
    <div v-if="transactions.length === 0 && !transactionsLoading">
      <div class="alert alert-warning">
        No transactions found for this team.
      </div>
    </div>
  </div>
  <Loader v-if="transactionsLoading" size="60px" background-color="#000000"/>
  <div v-else-if="!transactionsLoading && nextDataExists" class="w-100 d-flex justify-content-center my-3">
    <button v-on:click="addNewData" class="btn btn-primary text-center">Load more</button>
  </div>
  <div v-else-if="!transactionsLoading && !nextDataExists" class="alert alert-info text-center" style="margin-top: 1rem;">
    That's it for now! Check back later!
  </div>
</template>

<style scoped>

</style>