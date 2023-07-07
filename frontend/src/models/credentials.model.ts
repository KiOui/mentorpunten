export default interface Credentials {
  accessToken: string;
  expires: number;
  tokenType: string;
  scope: string[];
}
