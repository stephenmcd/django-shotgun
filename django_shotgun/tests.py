
import os
from HTMLParser import HTMLParser, HTMLParseError

from django.test import TestCase
import requests

from django_shotgun.settings import FIXTURE_NAME, FIXTURE_PATH, ROOT_URL


external = lambda u: u.lower().startswith(("http://", "https://", "mailto:"))


class DjangoParser(HTMLParser):
    """
    HTML parser that parses URLs from anchors and forms in a Django-driven
    HTML page.
    """

    def __init__(self, url):
        """
        URLs and forms are stored in lists. Also store the page's URL in case
        if a form with no action, then the page's URL is used as the action.
        """
        self.url = url
        self.urls = []
        self.forms = []
        HTMLParser.__init__(self)

    def valid_url(self, url):
        return url.startswith(ROOT_URL) and "/__debug__/" not in url

    def prefix_host(self, url):
        if url and external(ROOT_URL) and not external(url):
            url = ROOT_URL.rstrip("/") + "/" + url.lstrip("/")
        return url

    def handle_starttag(self, tag, attrs):
        """
        Add anchor HREFs as URLs and build the list of forms by attaching
        each of the form field names and values to it.
        """
        attrs = dict(attrs)
        if tag == "a":
            url = self.prefix_host(attrs.get("href", ""))
            if self.valid_url(url):
                self.urls.append(url.split("#")[0])
        elif tag == "form":
            url = self.prefix_host(attrs.get("action", "") or self.url)
            if self.valid_url(url):
                self.forms.append({"action": url, "fields": {}})
        elif tag in ("input", "select", "textarea"):
            name = attrs.get("name", "")
            if name and self.forms:
                value = ""
                if name == "csrfmiddlewaretoken":
                    value = attrs.get("value", "")
                self.forms[-1]["fields"][name] = value


class Tests(TestCase):
    """
    Runs the DjangoParser over the entire site testing for HTTP error codes.
    """

    fixtures = [os.path.join(FIXTURE_PATH, FIXTURE_NAME)]

    def test_site(self):
        """
        Attempt to test every valid URL on the site by maintaing two lists,
        a list of URLs still to check (``todo``), and a list of those that
        have been checked (``done``). As each URL is checked it is taken from
        the ``todo`` list and put onto the ``done`` list. Checking a URL
        will parse new URLs from the given page and these are added to the
        ``todo`` list if they're not yet checked. This process continues
        until the ``todo`` list is empty.

        Each URL is a pair containing the URL and form field data if the URL
        was parsed as a form action. When dealing with a form URL test it by
        performing both a GET and POST with the form data.
        """
        todo = [(ROOT_URL, None)] # Start URL
        done = []
        while True:
            url, data = todo.pop(0)
            done.append((url, data))
            # Build a list of responses, since a form URL will be tested
            # more than once via POST and GET.
            if external(url):
                client = requests
                kwargs = {}
            else:
                client = self.client
                kwargs = {"follow": True}
            if not data:
                responses = [client.get(url, **kwargs)]
            else:
                responses = [
                    client.get(url, data=data, **kwargs),
                    client.post(url, data=data, **kwargs),
                ]
            urls = []
            forms = []
            # Test each response code and build lists of URLs and forms from
            # the parsed HTML.
            for response in responses:
                self.assertEqual(response.status_code, 200)
                parser = DjangoParser(url)
                try:
                    parser.feed(response.content)
                except HTMLParseError:
                    pass
                urls.extend(parser.urls)
                forms.extend(parser.forms)
            for url in urls:
                url = (url, None)
                if url not in todo and url not in done:
                    todo.append(url)
            for form in forms:
                # Add the form twice, once with test data and once without.
                no_data = form["fields"]
                test_data = dict((k, v if v else "test") for k, v in
                    no_data.items())
                urls = [
                    (form["action"], no_data),
                    (form["action"], test_data),
                ]
                for url in urls:
                    if url not in todo and url not in done:
                        todo.append(url)
            if not todo:
                break

