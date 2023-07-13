<script lang="ts" setup>
import {useUserStore} from '@/stores/user.module';
import useApiService from "@/common/api.service";
import {onMounted, ref, toRef} from 'vue';
import Navbar from "@/components/Navbar.vue";
import Challenge from "@/models/challenge.model";
import Loader from "@/components/Loader.vue";

const props = defineProps<{id: number}>();

    const store = useUserStore();
    const ApiService = useApiService(store);
    let challenge = ref<Challenge | null>(null);
    const id = toRef(props, 'id');

    const imageFile = ref<File | null>(null);
    const imageField = ref<HTMLInputElement | null>(null);

    onMounted(() => {
      ApiService.getChallenge(id.value).then(result => {
        challenge.value = result;
      });
    });

    function changeImageFile(event: Event) {
      const files: FileList | null = (<HTMLInputElement>event.target).files;
      if (files === null || files.length === 0) {
        return;
      }
      imageFile.value = files[0];
    }

    function startUpload() {
      if (challenge.value !== null && imageFile.value !== null) {
        const formData = new FormData();
        formData.append("challenge", String(challenge.value.id));
        formData.append("image", imageFile.value, imageFile.value.name);
        ApiService.postChallengesSubmissions(formData).then(response => {
          console.log(response);
        }).catch(e => {
          console.log(e);
        }).finally(() => {
          imageFile.value = null;
          if (imageField.value !== null) {
            imageField.value.value = "";
          }
        });
      }
    }
</script>

<template>
    <Navbar/>
    <Loader v-if="challenge === null" size="60px" background-color="#000000"/>
    <div v-else class="container mt-5">
        <div class="card my-2">
            <div class="card-body">
              <div class="row">
                <div class="col-8">
                  <h3 class="card-title">{{ challenge.name }}</h3>
                </div>
                <div class="col-4 text-end">
                  <span class="badge bg-success fs-6">{{ challenge.points }} points</span>
                </div>
              </div>
                <p>
                  {{ challenge.description }}
                </p>
                <form class="input-group mt-3">
                  <label for="image" class="w-100 mb-2">Make a picture</label>
                  <input v-on:change="changeImageFile($event)" ref="imageField" type="file" class="form-control" id="image" capture="user" accept="image/*" aria-label="Upload">
                  <button v-on:click="startUpload()" class="btn btn-primary" type="button">Submit</button>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>