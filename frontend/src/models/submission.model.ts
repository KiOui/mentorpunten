import type Challenge from "@/models/challenge.model";
import type Team from "@/models/team.model";
import type Transaction from "@/models/transaction.model";
import type File from "@/models/file.model";

export default interface Submission {
    id: number,
    challenge: Challenge;
    team: Team;
    transaction: Transaction | null;
    created: string;
    updated: string;
    file: File;
    accepted: boolean | null;
}