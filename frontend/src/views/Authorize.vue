<script setup lang="ts">
  import { onMounted } from 'vue'
  import { useCredentialsStore } from "@/stores/credentials.module";
  import Loader from "@/components/Loader.vue";
  import { parseHash } from "@/common/general.service";
  import router from "@/router";

  const CredentialsStore = useCredentialsStore();

  function authorize() {
    try {
      const url = new URL(String(window.location));
      if (url.searchParams.get("error")) {
        alert(`Authorization failed: ${url.searchParams.get("error")}`);
      }
      else {
        let parsedHash;
        try {
          parsedHash = parseHash(url.hash.substring(1));
        } catch (e) {
          alert(`An error occurred while parsing the response from the authentication server: ${e}. Please try again.`);
          return;
        }
        let stateKey = parsedHash.state;
        if (stateKey === CredentialsStore.stateKey) {
          let accessToken = parsedHash.accessToken;
          let tokenType = parsedHash.tokenType;
          let scope = parsedHash.scope.split("+");
          let expires = Date.now() + (Number(parsedHash.expiresIn) * 1000) - 1000;
          CredentialsStore.login({
            accessToken, expires, tokenType, scope
          });
          CredentialsStore.storeState();
          router.push({ name: "Index" });
        } else {
          alert("State key did not match, please try again...");
        }
      }
    } catch (e) {
      alert("Authorization failed, please try again...");
    }
  }

  onMounted(() => {
    authorize();
  });
</script>

<template>
  <div class="container authorize mt-5 text-center">
    <h1 class="font-oswald">Authorization in progress...</h1>
    <p>
      You will be redirected shortly, if redirection fails, please click
      <router-link :to="{ name: 'Index' }">here</router-link>
    </p>
    <div class="d-flex justify-content-center align-items-center">
      <Loader size="60px" background-color="#000000"></Loader>
    </div>
  </div>
</template>

