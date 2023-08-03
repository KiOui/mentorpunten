<script lang="ts" setup>
import {useRouter} from "vue-router";

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
    <nav class="navbar">
        <div class="container">
            <ul class="navbar-nav w-100 d-flex justify-content-start flex-row">
                <a v-on:click="goBack()">
                  <font-awesome-icon icon="fa-solid fa-arrow-left"/>
                </a>
            </ul>
        </div>
    </nav>
</template>