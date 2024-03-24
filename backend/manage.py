#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

def main():
    # Set the DJANGO_SETTINGS_MODULE environment variable
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.local")

    try:
        # Import Django only if it's available
        import django
        if not django.get_version():
            raise ImportError("Django is not installed.")
    except ImportError as exc:
        # Raise a more informative error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment? You can install "
            "Django using 'pip install Django'."
        ) from exc

    # Execute the command
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
