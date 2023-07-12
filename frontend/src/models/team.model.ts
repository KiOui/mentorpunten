import type Account from "@/models/account.model";
import type User from "@/models/user.model";

export default interface Team {
    name: string;
    account: Account;
    members: User[];
    created: string;
    updated: string;
    image: string | null;
    accepted: boolean | null;
}