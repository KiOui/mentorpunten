import type Item from "@/models/item.model";

export default interface Store {
    id: number;
    name: string;
    items: Item[];
}