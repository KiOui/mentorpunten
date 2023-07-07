<script setup lang="ts">
  import { useUserStore } from '@/stores/user.module';

  const store = useUserStore();


</script>

<template>
  <nav class="navbar fixed-bottom">
    <div class="container">
      <ul class="navbar-nav w-100 d-flex justify-content-center flex-row">
        <li class="nav-item flex-grow-1 text-center">
          <font-awesome-icon icon="fa-solid fa-images"/>
        </li>
        <li class="nav-item flex-grow-1 text-center">
          <font-awesome-icon icon="fa-solid fa-trophy"/>
        </li>
        <li class="nav-item flex-grow-1 text-center">
          <font-awesome-icon icon="fa-solid fa-chart-line"/>
        </li>
        <li class="nav-item flex-grow-1 text-center">
          <font-awesome-icon icon="fa-solid fa-user"/>
        </li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>

</style>