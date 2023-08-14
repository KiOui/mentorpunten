import type Item from "@/models/item.model";
import type Transaction from "@/models/transaction.model";
import type Team from "@/models/team.model";

export default interface BoughtItem {
    id: number;
    name: string;
    price: number;
    description: string;
    item: Item | null;
    transaction: Transaction | null;
    property_of: Team;
    used: boolean;
    used_at: string;
}