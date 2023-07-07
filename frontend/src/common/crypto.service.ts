class CryptoService {
  static base64Encode(string: string): string {
    return btoa(string)
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=+$/, "");
  }

  static getRandomString(length: number): string {
    return this.base64Encode(
      Array.prototype.map
        .call(
          window.crypto.getRandomValues(new Uint8Array(length)),
          (number: number) => {
            return String.fromCharCode(number);
          }
        )
        .join("")
        .substring(0, length)
    );
  }

  static async getSHA256(string: string): Promise<string | null> {
    const randomArray = new Uint8Array(string.length);
    for (let i = 0; i < string.length; i++) {
      randomArray[i] = string.charCodeAt(i);
    }
    return await window.crypto.subtle
      .digest("SHA-256", randomArray)
      .then((digest) => {
        return this.base64Encode(
          String.fromCharCode(...new Uint8Array(digest))
        );
      })
      .catch(() => {
        return null;
      });
  }
}

export default CryptoService;
