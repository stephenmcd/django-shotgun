
import os

from django.core.management.base import CommandError
from django.core.management.commands import dumpdata
from django.conf import settings

from django_shotgun.utils import fixtures_file_path


class Command(dumpdata.Command):
    
    def handle(self, *args, **kwargs):
        """
        Call the ``dumpdata`` management command and store the output of it 
        into the shotgun fixtures file in the current project.
        """
        exclude = kwargs.pop("exclude", [])
        if "contenttypes" not in exclude:
            exclude.append("contenttypes")
        kwargs["exclude"] = exclude
        settings = __import__(os.environ["DJANGO_SETTINGS_MODULE"])
        project_path = os.path.dirname(os.path.abspath(settings.__file__))
        try:
            with open(fixtures_file_path(), "w") as f:
                f.write(dumpdata.Command.handle(self, *args, **kwargs))
        except Exception, e:
            raise CommandError(e)
