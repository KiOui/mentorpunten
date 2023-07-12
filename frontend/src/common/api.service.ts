import type Announcement from "@/models/announcement.model";
import type User from "@/models/user.model";
import type Submission from "@/models/submission.model";
import {useUserStore} from "@/stores/user.module";
import type ChallengeUser from "@/models/challengeUser.model";
import type Challenge from "@/models/challenge.model";
import type _Challenge from "@/models/api/_challenge.model";

class _ApiService {
  authorizationEndpoint: string;
  baseUri: string;
  clientId: string;
  redirectUri: string;
  authStore: ReturnType<typeof useUserStore>;

  constructor(
    clientId: string,
    baseUri: string,
    authorizationEndpoint: string,
    redirectUri: string,
    authStore: ReturnType<typeof useUserStore>,
  ) {
    this.clientId = clientId;
    this.baseUri = baseUri;
    this.authorizationEndpoint = authorizationEndpoint;
    this.redirectUri = redirectUri;
    this.authStore = authStore;
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

  getAuthorizationHeader(): Headers {
    const requestHeaders = new Headers();
    const accessToken = this.authStore.accessToken;
    if (accessToken !== null) {
      requestHeaders.set("Authorization", `Bearer ${accessToken}`);
    }
    return requestHeaders;
  }

  async getAnnouncements(): Promise<Announcement[]> {
    return this.get<Announcement[]>("/announcements/");
  }

  async getUsersMe(): Promise<User> {
    return this.get<User>("/users/me/");
  }

  async getChallengesSubmissions(): Promise<Submission[]> {
    return this.get<Submission[]>("/challenges/submissions/");
  }

  async postChallengesSubmissions(data: object): Promise<Submission> {
    return this.post<Submission>("/challenges/submissions/", data);
  }

  async getChallengesUsersMe(): Promise<ChallengeUser> {
    return this.get<ChallengeUser>("/challenges/users/me/");
  }

  async getChallenges(): Promise<Challenge[]> {
    return this.get<Challenge[]>("/challenges/");
  }

  async getChallenge(id: number): Promise<Challenge> {
    return this.get<Challenge>(`/challenges/${id}/`);
  }

  async fetch<T>(resource: string, method: string, data: object|null): Promise<T> {
    let apiCall = null;
    if (data !== null) {
      apiCall = fetch(`${this.baseUri}/api/v1${resource}`, {
        method: method,
        headers: this.getAuthorizationHeader(),
        body: JSON.stringify(data),
      });
    } else {
       apiCall = fetch(`${this.baseUri}/api/v1${resource}`, {
        method: method,
        headers: this.getAuthorizationHeader()
      });
    }
    return apiCall.then(response => {
      if (response.ok) {
        return response;
      } else {
        throw response;
      }
    }).then(result => {
      return result.json() as Promise<T>;
    });
  }

  async get<T>(resource: string): Promise<T> {
    return this.fetch<T>(resource, 'GET', null);
  }

  async post<T>(resource: string, data: object): Promise<T> {
    return this.fetch<T>(resource, 'POST', data);
  }

  async put<T>(resource: string, data: object): Promise<T> {
    return this.fetch<T>(resource, 'PUT', data);
  }

  async patch<T>(resource: string, data: object): Promise<T> {
    return this.fetch<T>(resource, 'PATCH', data);
  }

  async delete<T>(resource: string): Promise<T> {
    return this.fetch<T>(resource, 'DELETE', null);
  }
}

const useApiService = (authStore: ReturnType<typeof useUserStore>) => {
  return new _ApiService(
      import.meta.env.VITE_API_OAUTH_CLIENT_ID,
      import.meta.env.VITE_API_BASE_URI,
      import.meta.env.VITE_API_AUTHORIZATION_ENDPOINT,
      import.meta.env.VITE_API_OAUTH_REDIRECT_URI,
      authStore
  )
}

export default useApiService;
