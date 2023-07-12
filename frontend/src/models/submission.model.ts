import type Challenge from "@/models/challenge.model";
import type Team from "@/models/team.model";

export default interface Submission {
    challenge: Challenge;
    team: Team;
    created: string;
    updated: string;
    image: string;
    accepted: boolean | null;
}