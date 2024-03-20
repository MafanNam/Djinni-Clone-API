import os

from django.core.exceptions import ValidationError


def validate_file_size(file_obj, mb_limit=5):
    if file_obj.size > mb_limit * 1024 * 1024:
        raise ValidationError(f"Max size for file {mb_limit}MB")


def delete_old_file(path_file):
    """Delete old file"""
    if os.path.exists(path_file):
        os.remove(path_file)


def get_path_upload_image_company(instance, filename):
    return f"companies/{instance.name}_{instance.user.id}/{filename}"


def get_path_upload_image_candidate(instance, filename):
    return f"users/candidates/{instance.user.id}/{filename}"


def get_path_upload_image_recruiter(instance, filename):
    return f"users/recruiters/{instance.user.id}/{filename}"
