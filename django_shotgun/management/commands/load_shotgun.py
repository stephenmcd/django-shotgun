
import os
from optparse import make_option

from django.core.management.base import CommandError
from django.core.management.commands import dumpdata
from django.conf import settings


class Command(dumpdata.Command):
    
    option_list = dumpdata.Command.option_list + (
        make_option("--path", default="", dest="path",
            help="Specifies the path to save the shotgun fixtures."),
    )

    def handle(self, *args, **kwargs):
        """
        Call the ``dumpdata`` management command and store the output of it 
        into the shotgun fixtures file in the current project.
        """
        if "contenttypes" not in kwargs["exclude"]:
            kwargs["exclude"].append("contenttypes")
        if not kwargs["path"]:
            s = __import__(os.environ["DJANGO_SETTINGS_MODULE"])
            kwargs["path"] = os.path.dirname(os.path.abspath(s.__file__))
        try:
            with open(os.path.join(kwargs["path"], "shotgun.json"), "w") as f:
                f.write(dumpdata.Command.handle(self, *args, **kwargs))
        except Exception, e:
            raise CommandError(e)
