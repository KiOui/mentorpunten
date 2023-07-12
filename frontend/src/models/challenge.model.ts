export default interface Challenge {
    name: string;
    slug: string;
    description: string;
    image: string | null;
    disabled: boolean;
    active_from: string | null;
    active_until: string | null;
    points: number;
}