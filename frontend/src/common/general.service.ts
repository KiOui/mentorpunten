

function parseHash(hashString: string): {
    access_token: string,
    expires_in: string,
    token_type: string,
    scope: string,
    state: string
} {
    const returnValue: { access_token: string | null, expires_in: string | null, token_type: string | null, scope: string | null, state: string | null } = {
        "access_token": null,
        "expires_in": null,
        "token_type": null,
        "scope": null,
        "state": null
    }
    const splittedHashString = hashString.split('&');
    for (let i = 0; i < splittedHashString.length; i++) {
        const item = splittedHashString[i];
        const parts = item.split('=');
        if (parts.length === 2) {
            const key = parts[0];
            const value = parts[1];
            if (key === "access_token") {
                returnValue.access_token = value;
            } else if (key === "expires_in" ) {
                returnValue.expires_in = value;
            } else if (key === "token_type") {
                returnValue.token_type = value;
            } else if (key === "scope") {
                returnValue.scope = value;
            } else if (key === "state") {
                returnValue.state = value;
            } else {
                throw new Error("Unknown key found in return hash.")
            }
        } else {
            throw new Error("Length of key-value field is not equal to two.")
        }
    }

    const objectKeys = Object.keys(returnValue);
    for (let i = 0; i < objectKeys.length; i++) {
        const key = objectKeys[i];
        if (returnValue[key] === null) {
            throw new Error("One of the fields is not defined.")
        }
    }
    return returnValue;
}

export { parseHash };