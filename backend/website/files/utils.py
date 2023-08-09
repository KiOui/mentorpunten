from pathlib import Path
import uuid
from django.urls import reverse
from django.conf import settings


def get_random_filename(current_filename):
    """Get a random filename by overwriting the filename with a random string."""
    extension = Path(current_filename).suffix
    unique_id = uuid.uuid4()
    return f"{unique_id}{extension}"

# Create your models here.
def file_generate_upload_path(instance, filename):
    return f"files/{instance.file_name}"

def file_generate_local_upload_url(*, file_id: str):
    url = reverse("v1:files:files_upload_local", kwargs={"file_id": file_id})
    app_domain: str = settings.APP_DOMAIN
    return f"{app_domain}{url}"