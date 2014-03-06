
from django.conf import settings

# A list of app names to exclude when generating the shotgun fixtures file.
EXCLUDE_APPS = getattr(settings, "SHOTGUN_EXCLUDE_APPS", [])

# Name of the shotgun fixture file.
FIXTURE_NAME = getattr(settings, "SHOTGUN_FIXTURE_NAME", "shotgun.json")

# Path to the shotgun fixture file.
FIXTURE_PATH = getattr(settings, "SHOTGUN_FIXTURE_PATH", "")

# The first URL that the shotgun test will request.
ROOT_URL = getattr(settings, "SHOTGUN_ROOT_URL", "/")


