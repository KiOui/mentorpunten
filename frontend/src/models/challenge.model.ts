import type Tournament from "@/models/tournament.model";

export default interface Challenge {
    id: number;
    name: string;
    slug: string;
    description: string;
    image: string | null;
    disabled: boolean;
    active_from: string | null;
    active_until: string | null;
    points: number;
    completed: boolean | null;
    tournament: Tournament;
    submission_visibility: number;
}