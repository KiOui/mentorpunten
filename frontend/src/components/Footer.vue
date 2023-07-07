<script setup lang="ts">
  import { useUserStore } from '@/stores/user.module';

  const store = useUserStore();

</script>

<template>
  <nav class="navbar fixed-bottom">
    <div class="container">
      <ul class="navbar-nav w-100 d-flex justify-content-center flex-row">
        <router-link :to="{ name: 'home' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-images"/>
          </li>
        </router-link>
        <router-link :to="{ name: 'challenges' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
              <font-awesome-icon icon="fa-solid fa-trophy"/>
          </li>
        </router-link>
        <router-link :to="{ name: 'statistics' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-chart-line"/>
          </li>
        </router-link>
        <router-link :to="{ name: 'profile' }" class="text-white nav-item flex-grow-1 text-center">
          <li>
            <font-awesome-icon icon="fa-solid fa-user"/>
          </li>
        </router-link>
      </ul>
    </div>
  </nav>
</template>

<style scoped>

</style>