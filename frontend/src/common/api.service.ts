import type {StoreDefinition} from "pinia";

class _ApiService {
  authorizationEndpoint: string;
  baseUri: string;
  clientId: string;
  redirectUri: string;
  store: StoreDefinition;

  constructor(
    clientId: string,
    baseUri: string,
    authorizationEndpoint: string,
    redirectUri: string,
    store: StoreDefinition
  ) {
    this.clientId = clientId;
    this.baseUri = baseUri;
    this.authorizationEndpoint = authorizationEndpoint;
    this.redirectUri = redirectUri;
    this.store = store;
  }

  getAuthorizationUri(): string {
    return `${this.baseUri}${this.authorizationEndpoint}`;
  }

  getAuthorizeRedirectURL(
    state: null | string,
    codeChallenge: null | string,
    isSHA256Challenge = false
  ): string {
    const authURL = new URL(this.getAuthorizationUri());
    authURL.searchParams.append("client_id", this.clientId);
    authURL.searchParams.append("redirect_uri", this.redirectUri);
    authURL.searchParams.append("response_type", "token");
    if (state !== null) {
      authURL.searchParams.append("state", state);
    }
    if (codeChallenge !== null) {
      authURL.searchParams.append("code_challenge", codeChallenge);
      if (isSHA256Challenge) {
        authURL.searchParams.append("code_challenge_method", "S256");
      } else {
        authURL.searchParams.append("code_challenge_method", "plain");
      }
    }
    return authURL.href;
  }

  async getUsersMe(): Promise<Response> {
    return this.get("/users/me/");
  }

  async get(resource: string): Promise<Response> {
    return fetch(`${this.baseUri}/api/v1${resource}`, {
      method: 'GET',
      headers: {
        Authorization: `${this.store.tokenType} ${this.store.accessToken}`,
      },
    });
  }

  async post(resource: string, data: object): Promise<Response> {
    return fetch(`${this.baseUri}/api/v1${resource}`, {
      method: 'POST',
      headers: {
        Authorization: `${this.store.tokenType} ${this.store.accessToken}`,
      },
      body: JSON.stringify(data),
    });
  }

  async put(resource: string, data: object): Promise<Response> {
    return fetch(`${this.baseUri}/api/v1${resource}`, {
      method: 'PUT',
      headers: {
        Authorization: `${this.store.tokenType} ${this.store.accessToken}`,
      },
      body: JSON.stringify(data),
    });
  }

  async patch(resource: string, data: object): Promise<Response> {
    return fetch(`${this.baseUri}/api/v1${resource}`, {
      method: 'PATCH',
      headers: {
        Authorization: `${this.store.tokenType} ${this.store.accessToken}`,
      },
      body: JSON.stringify(data),
    });
  }

  async delete(resource: string): Promise<Response> {
    return fetch(`${this.baseUri}/api/v1${resource}`, {
      method: 'DELETE',
      headers: {
        Authorization: `${this.store.tokenType} ${this.store.accessToken}`,
      },
    });
  }
}

const useApiService = (store) => {
  return new _ApiService(
      import.meta.env.VITE_API_OAUTH_CLIENT_ID,
      import.meta.env.VITE_API_BASE_URI,
      import.meta.env.VITE_API_AUTHORIZATION_ENDPOINT,
      import.meta.env.VITE_API_OAUTH_REDIRECT_URI,
      store
  )
}

export default useApiService;
