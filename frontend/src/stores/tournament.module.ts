import { defineStore } from 'pinia'
import type Tournament from "@/models/tournament.model";

const TOURNAMENT_KEY = "tournament";

const savedTournament = localStorage.getItem(TOURNAMENT_KEY);

export const useTournamentStore = defineStore('tournament', {
    state: () => ({
        /** @type Tournament|null */
        savedTournament: savedTournament ? JSON.parse(savedTournament) : null,
    }),
    getters: {
        tournament(state): null|Tournament {
            return state.savedTournament;
        },
        tournamentSelected(state): boolean {
            return state.savedTournament !== null;
        }
    },
    actions: {
        removeSelectedTournament() {
            this.savedTournament = null;
        },
        storeState(): void {
            localStorage.setItem(TOURNAMENT_KEY, JSON.stringify(this.savedTournament));
        },
        storeNewTournament(tournament: Tournament) {
            this.savedTournament = tournament;
        },
    }

});
