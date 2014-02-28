from c101ws.mailgun import SubscribeResource
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.util import Redirect


def secureSite(staticPath):
    """Builds the secure (HTTPS, port 443) site.

    """
    root = File(staticPath)
    root.putChild("subscribe", SubscribeResource())
    return Site(root)


def insecureSite():
    """Builds the insecure (HTTP, port 80) site.

    """
    return Site(Redirect("https://www.crypto101.io"))
