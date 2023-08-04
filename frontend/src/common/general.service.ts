

function parseHash(hashString: string) {
    return hashString.split('&').reduce(function (res, item) {
        const parts = item.split('=');
        res[parts[0]] = decodeURIComponent(parts[1]);
        return res;
    }, {});
}

export { parseHash };