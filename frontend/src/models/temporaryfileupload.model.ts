import type User from "@/models/user.model";
import type PresignedData from "@/models/presigneddata.model";

export default interface TemporaryFileUpload {
    id: string;
    original_file_name: string;
    file_type: string;
    created_at: string;
    created_by: User | null;
    finished_at: string | null;
    presigned_data: PresignedData;
}