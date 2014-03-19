from c101ws.web import insecureSite, secureSite, _withHSTS
from twisted.trial.unittest import SynchronousTestCase
from twisted.web.http_headers import Headers
from twisted.web.util import Redirect


class FakeRequest(object):
    def __init__(self, path):
        self.path = path
        self.prepath = []
        self.postpath = path.split("/")

        self.responseHeaders = Headers()
        self.requestHeaders = Headers()



class SecureSiteTests(SynchronousTestCase):
    def test_doesntDisplayTracebacks(self):
        site = secureSite({"STATIC_PATH": ""})
        self.assertFalse(site.displayTracebacks)



class HSTSTests(SynchronousTestCase):
    def test_withHSTS(self):
        requestFactoryWithHSTS = _withHSTS(FakeRequest)
        headers = requestFactoryWithHSTS("path").responseHeaders
        value, = headers.getRawHeaders("Strict-Transport-Security")
        self.assertEqual(value, "max-age=31536000")



class InsecureSiteTests(SynchronousTestCase):
    def setUp(self):
        self.site = insecureSite()


    def test_redirectsToSecureSite(self):
        """Requests made to the site redirect to the secure site.

        """
        self.assertRedirectsToSecureSite("/")
        self.assertRedirectsToSecureSite("/a/b/c")


    def assertRedirectsToSecureSite(self, path):
        """Asserts that a request to this path would have resulted in a
        redirect to the secure website.

        """
        request = FakeRequest(path)
        resource = self.site.getResourceFor(request)
        self.assertTrue(isinstance(resource, Redirect))
        self.assertEqual(resource.url, "https://www.crypto101.io")
