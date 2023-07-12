import type User from "@/models/user.model";
import type Team from "@/models/team.model";

export default interface ChallengeUser {
    user: User;
    team: Team;
}