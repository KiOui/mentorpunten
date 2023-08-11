import type User from "@/models/user.model";

export default interface UploadedFile {
    id: string;
    file: string;
    compressed_file: string | null;
    original_file_name: string;
    file_name: string;
    file_type: string;
    created_by: User | null;
    created_at: string;
}