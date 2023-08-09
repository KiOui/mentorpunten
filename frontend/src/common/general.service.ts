import type Tournament from "@/models/tournament.model";
import type Challenge from "@/models/challenge.model";

const LOGOUT_TOKEN_NAME = "logout_state";

function parseHash(hashString: string): {
    accessToken: string,
    expiresIn: string,
    tokenType: string,
    scope: string,
    state: string
} {
    let accessToken: string | null = null;
    let expiresIn: string | null = null;
    let tokenType: string | null = null;
    let scope: string | null = null;
    let state: string | null = null;
    const splitHashString = hashString.split('&');
    for (let i = 0; i < splitHashString.length; i++) {
        const item = splitHashString[i];
        const parts = item.split('=');
        if (parts.length === 2) {
            const key = parts[0];
            const value = parts[1];
            if (key === "access_token") {
                accessToken = value;
            } else if (key === "expires_in" ) {
                expiresIn = value;
            } else if (key === "token_type") {
                tokenType = value;
            } else if (key === "scope") {
                scope = value;
            } else if (key === "state") {
                state = value;
            } else {
                throw new Error("Unknown key found in return hash.")
            }
        } else {
            throw new Error("Length of key-value field is not equal to two.")
        }
    }

    if (accessToken === null) {
        throw new Error("Access token not found in hash.");
    }
    else if (expiresIn === null) {
        throw new Error("Expires in not found in hash.");
    }
    else if (tokenType === null) {
        throw new Error("Token type not found in hash.");
    }
    else if (scope === null) {
        throw new Error("Scope not found in hash.");
    }
    else if (state === null) {
        throw new Error("State not found in hash.");
    } else {
        return {
            accessToken: accessToken,
            expiresIn: expiresIn,
            tokenType: tokenType,
            scope: scope,
            state: state
        }
    }
}

function getEnvVar(name: string): string {
    // @ts-ignore
    if (window?.__env__?.[name]) {
        return window?.__env__?.[name];
    } else if (import.meta.env[name]) {
        return import.meta.env[name];
    } else {
        throw new Error(`Environment variable ${name} is not defined.`);
    }
}

function startEndTimeOfTournament(tournament: Tournament): string {
    if (tournament.active_from) {
        const start_date = new Date(tournament.active_from);
        const end_date = new Date(tournament.active_until);

        return `${start_date.toLocaleDateString("en-GB")}, ${start_date.toLocaleTimeString(
            "en-GB",
            { hour: "2-digit", minute: "2-digit" }
        )} until ${end_date.toLocaleDateString("en-GB")}, ${end_date.toLocaleTimeString(
            "en-GB",
            { hour: "2-digit", minute: "2-digit" }
        )}`;
    }
    return "";
}

function startTimeOfChallenge(challenge: Challenge): string {
    if (challenge.active_from) {
        const start_date = new Date(challenge.active_from);
        return `${start_date.toLocaleDateString("en-GB")}, ${start_date.toLocaleTimeString(
            "en-GB",
            { hour: "2-digit", minute: "2-digit" }
        )}`;
    }
    return "";
}

export { LOGOUT_TOKEN_NAME, parseHash, getEnvVar, startEndTimeOfTournament, startTimeOfChallenge };