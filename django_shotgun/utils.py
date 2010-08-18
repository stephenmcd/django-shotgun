
import os


def fixtures_file_path():
    """
    Return the absolute path to the shotgun fixtures file. Uses the same path 
    as the project's settings module.
    """
    settings_module = __import__(os.environ["DJANGO_SETTINGS_MODULE"])
    project_path = os.path.dirname(os.path.abspath(settings_module.__file__))
    return os.path.join(project_path, "shotgun.json")

    
