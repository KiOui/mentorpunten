import { defineStore } from 'pinia'

const CLOSED_ANNOUNCEMENTS_KEY = "closed_announcements";

const savedClosedAnnouncements = localStorage.getItem(CLOSED_ANNOUNCEMENTS_KEY);

export const useAnnouncementsStore = defineStore('announcements', {
    state: () => ({
        /** @type number[] */
        closedAnnouncements: savedClosedAnnouncements ? JSON.parse(savedClosedAnnouncements) : [],
    }),
    actions: {
        addAnnouncement(announcementId: number) {
            if (this.closedAnnouncements.includes(announcementId)) {
                return;
            } else {
                this.closedAnnouncements.push(announcementId);
            }
        },
        storeState(): void {
            localStorage.setItem(CLOSED_ANNOUNCEMENTS_KEY, JSON.stringify(this.closedAnnouncements));
        },
    }

});
