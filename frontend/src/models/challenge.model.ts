export default interface Challenge {
    name: string;
    slug: string;
    description: string;
    image: string | null;
    disabled: boolean;
    activeFrom: string | null;
    activeUntil: string | null;
    points: number;
}