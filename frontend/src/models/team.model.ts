import type Account from "@/models/account.model";
import type User from "@/models/user.model";
import type Tournament from "@/models/tournament.model";

export default interface Team {
    id: number,
    name: string;
    account: Account;
    members: User[];
    tournament: Tournament;
}