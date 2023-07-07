import { defineStore } from 'pinia'

const TOKEN_KEY = "credentials";

const savedCredentials = localStorage.getItem(TOKEN_KEY);

console.log(savedCredentials);

export const useUserStore = defineStore('user', {
    state: () => ({
        /** @type Credentials */
        credentials: JSON.parse(savedCredentials),
    }),
    getters: {
        loggedIn(state) {
            return state.credentials !== null;
        }
    },
    actions: {
        logOut() {
            this.state.credentials = null;
        }
    }

});
