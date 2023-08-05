

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

export { parseHash };