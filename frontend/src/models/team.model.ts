import type Account from "@/models/account.model";
import type User from "@/models/user.model";
import type Tournament from "@/models/tournament.model";
import type BoughtItem from "@/models/boughtitem.model";

export default interface Team {
    id: number,
    name: string;
    points_account: Account;
    coins_account: Account | null;
    members: User[];
    tournament: Tournament;
    items: BoughtItem[];
}