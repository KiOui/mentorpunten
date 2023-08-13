export default interface Tournament {
    id: number;
    name: string;
    slug: string;
    active_from: string;
    active_until: string;
    store: number | null;
}