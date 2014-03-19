from c101ws.mailgun import SubscribeResource
from os import environ
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.util import Redirect


def secureSite(_environ=environ):
    """Builds the secure (HTTPS, port 443) site.

    """
    root = File(_environ["STATIC_PATH"])
    root.putChild("subscribe", SubscribeResource("announce@crypto101.io"))

    site = Site(root)
    site.displayTracebacks = False
    site.requestFactory = _withHSTS(site.requestFactory)
    return site


def _withHSTS(requestFactory):
    """
    Builds a request factory that sets HSTS (HTTP Strict Transport
    Security) headers, by wrapping another request factory.

    """
    def makeHSTSRequest(*a, **kw):
        request = requestFactory(*a, **kw)
        request.responseHeaders.setRawHeaders(
            "Strict-Transport-Security", ["max-age=31536000"])
        return request

    return makeHSTSRequest



def insecureSite():
    """Builds the insecure (HTTP, port 80) site.

    """
    return Site(Redirect("https://www.crypto101.io"))
