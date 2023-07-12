import { defineStore } from 'pinia'
import CryptoService from "@/common/crypto.service";

const TOKEN_KEY = "credentials";
const OAUTH_STATE_KEY = "oauth_state";

const savedCredentials = localStorage.getItem(TOKEN_KEY);
const savedStateKey = localStorage.getItem(OAUTH_STATE_KEY);

export const useUserStore = defineStore('user', {
    state: () => ({
        /** @type Credentials|null */
        credentials: savedCredentials ? JSON.parse(savedCredentials) : null,
        /** @type string|null */
        stateKey: savedStateKey ? JSON.parse(savedStateKey) : null,
    }),
    getters: {
        accessToken(state): null|string {
            if (state.credentials === null || state.credentials.expires < Date.now()) {
                return null;
            } else {
                return state.credentials.accessToken;
            }
        },
        loggedIn(state): boolean {
            return state.credentials !== null && state.credentials.expires >= Date.now();
        }
    },
    actions: {
        logOut() {
            this.credentials = null;
        },
        storeState(): void {
            localStorage.setItem(TOKEN_KEY, JSON.stringify(this.credentials));
            localStorage.setItem(OAUTH_STATE_KEY, JSON.stringify(this.stateKey));
        },
        newRandomState(): void {
            this.stateKey = CryptoService.getRandomString(12);
        },
        login(payload: {accessToken: string; expires: number; tokenType: string; scope: string[]}) {
            const { accessToken, expires, tokenType, scope } = payload;
            this.credentials = {
                ...this.credentials,
                accessToken: accessToken,
                expires: expires,
                tokenType: tokenType,
                scope: scope,
            };
        },
    }

});
