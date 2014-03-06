
from setuptools import setup, find_packages


setup(
    name = "django-shotgun",
    version = __import__("django_shotgun").__version__,
    author = "Stephen McDonald",
    author_email = "stephen.mc@gmail.com",
    description = ("A Django application for testing entire sites."),
    long_description = open("README.rst").read(),
    url = "http://github.com/stephenmcd/django-shotgun",
    zip_safe = False,
    packages = find_packages(),
    install_requires=["sphinx-me", "requests"],
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
    ]
)
