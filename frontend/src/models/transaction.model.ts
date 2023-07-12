export default interface Transaction {
    id: string;
    account: number;
    amount: number;
    timestamp: string;
    description: string;
    processor: number;
    balance_after: number;
}