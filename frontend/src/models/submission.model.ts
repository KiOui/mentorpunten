import type Challenge from "@/models/challenge.model";
import type Team from "@/models/team.model";
import type Transaction from "@/models/transaction.model";
import type UploadedFile from "@/models/uploadedfile.model";

export default interface Submission {
    id: number,
    challenge: Challenge;
    team: Team;
    points_transaction: Transaction | null;
    coins_transaction: Transaction | null;
    created: string;
    updated: string;
    file: UploadedFile;
    accepted: boolean | null;
}