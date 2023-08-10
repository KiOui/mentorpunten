import type User from "@/models/user.model";

export default interface File {
    id: string;
    file: string;
    original_file_name: string;
    file_name: string;
    file_type: string;
    created_by: User | null;
    created_at: string;
}