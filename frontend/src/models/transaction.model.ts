import type Account from "@/models/account.model";

export default interface Transaction {
    id: string;
    account: Account;
    amount: number;
    timestamp: string;
    description: string;
    processor: number;
    balance_after: number;
}