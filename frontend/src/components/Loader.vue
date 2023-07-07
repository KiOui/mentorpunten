<template>
  <div class="spinner" :style="{ width: size, height: size }">
    <div
      class="double-bounce1"
      :style="{ 'background-color': backgroundColor }"
    ></div>
    <div
      class="double-bounce2"
      :style="{ 'background-color': backgroundColor }"
    ></div>
  </div>
</template>

<script>
export default {
  name: "Loader",
  props: {
    size: String,
    backgroundColor: String,
  },
};
</script>

<style>
.spinner {
  position: relative;
  margin: 100px auto;
}

.double-bounce1,
.double-bounce2 {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  opacity: 0.6;
  position: absolute;
  top: 0;
  left: 0;

  -webkit-animation: sk-bounce 2s infinite ease-in-out;
  animation: sk-bounce 2s infinite ease-in-out;
}

.double-bounce2 {
  -webkit-animation-delay: -1s;
  animation-delay: -1s;
}

@-webkit-keyframes sk-bounce {
  0%,
  100% {
    -webkit-transform: scale(0);
  }
  50% {
    -webkit-transform: scale(1);
  }
}

@keyframes sk-bounce {
  0%,
  100% {
    transform: scale(0);
    -webkit-transform: scale(0);
  }
  50% {
    transform: scale(1);
    -webkit-transform: scale(1);
  }
}
</style>
