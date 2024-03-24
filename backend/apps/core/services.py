import os
from typing import Any

from django.core.exceptions import ValidationError

def validate_file_size(file_obj, mb_limit: int = 10) -> None:
    if file_obj.size > mb_limit * 1024 * 1024:
        raise ValidationError(f"Max file size {mb_limit}MB")

def delete_old_file(path_file: str) -> None:
    """Delete old file."""
    if os.path.exists(path_file):
        os.remove(path_file)

def get_path_upload_image_company(instance, filename: str = "") -> str:
    return os.path.join("companies", f"{instance.name}_{instance.user.id}", filename)

def get_path_upload_cv_file_contact_cv(instance, filename: str = "") -> str:
    return os.path.join("users", "candidates", str(instance.user.id), "cv", filename)

def get_path_upload_image_candidate(instance, filename: str = "") -> str:
    return os.path.join("users", "candidates", str(instance.user.id), filename)

def get_path_upload_image_recruiter(instance, filename: str = "") -> str:
    return os.path.join("users", "recruiters", str(instance.user.id), filename)
