
from django.conf import settings

# List of apps to exclude when generating the shotgun fixtures file.
SHOTGUN_EXCLUDE = getattr(settings, "SHOTGUN_EXCLUDE", [])

# Name of the shotgun fixture file.
SHOTGUN_NAME = getattr(settings, "SHOTGUN_NAME", "shotgun.json")

# Path to the shotgun fixture file.
SHOTGUN_PATH = getattr(settings, "SHOTGUN_PATH", "")

# The first URL that the shotgun test will request.
SHOTGUN_ROOT_URL = getattr(settings, "SHOTGUN_ROOT_URL", "/")


