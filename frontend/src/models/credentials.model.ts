export default interface Credentials {
  accessToken: string;
  expiresIn: number;
  tokenType: string;
  scope: string[];
}
