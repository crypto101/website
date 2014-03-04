from c101ws.mailgun import SubscribeResource
from os import environ
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.util import Redirect


def secureSite(_environ=environ):
    """Builds the secure (HTTPS, port 443) site.

    """
    root = File(_environ["STATIC_PATH"])
    root.putChild("subscribe", SubscribeResource())
    return Site(root)


def insecureSite():
    """Builds the insecure (HTTP, port 80) site.

    """
    return Site(Redirect("https://www.crypto101.io"))
