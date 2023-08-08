<script setup lang="ts">


import {computed, onMounted, ref} from "vue";
import useApiService from "@/common/api.service";
import type Announcement from "@/models/announcement.model";
import {useAnnouncementsStore} from "@/stores/announcements.module";

const ApiService = useApiService();
const AnnouncementService = useAnnouncementsStore();

const announcements = ref<Announcement[]>([]);

onMounted(() => {
  ApiService.getAnnouncements().then(result => {
    announcements.value = result;
  }).catch(() => {});
});

const announcementsExcludingClosedOnes = computed(() => {
  return announcements.value.filter((announcement) => {
    return !AnnouncementService.closedAnnouncements.includes(announcement.id);
  });
});

function closeAnnouncement(announcementId: number) {
  AnnouncementService.addAnnouncement(announcementId);
  AnnouncementService.storeState();
}
</script>

<template>
  <div class="w-100 announcement-container">
    <div class="container">
      <div v-for="announcement in announcementsExcludingClosedOnes" class="announcement" v-bind:key="announcement.id" v-bind:id='`announcement-${announcement.id}`'>
        <i v-bind:class="`fas fa-${announcement.icon} me-3`"></i> <div v-html="announcement.content" class="announcement-content"></div>
        <button type="button" class="btn-close ms-3" aria-label="Close" v-on:click="closeAnnouncement(announcement.id)"></button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.announcement-container {
  background: var(--primary-shade);
}

.announcement {
  display: flex;
  justify-content: center;
  align-items: center;
  color: var(--primary-contrast);
  text-align: center;
  padding: 0.5rem 1rem;
}

.announcement .btn-close {
  color: var(--primary-contrast);
}
</style>