from c101ws.service import WebsiteService, WebsiteServiceMaker
from clarent.certificate import SecureCiphersContextFactory
from OpenSSL.SSL import SSLv23_METHOD
from os.path import dirname, join
from twisted.application.service import IService, IServiceMaker
from twisted.plugin import IPlugin
from twisted.trial.unittest import SynchronousTestCase
from zope.interface.verify import verifyObject


class ServiceTests(SynchronousTestCase):
    def setUp(self):
        def localPath(name):
            return join(dirname(__file__), name)

        self.service = WebsiteService(_environ={
            "CERTIFICATE_PATH": localPath("test-cert-chain.pem"),
            "DH_PARAMETERS_PATH": localPath("test-dh-parameters.pem")
        })


    def test_contextFactory(self):
        """The context factory produces pragmatic, secure SSL contexts.

        """
        ctxFactory = self.service._getCtxFactory()
        self.assertIdentical(type(ctxFactory), SecureCiphersContextFactory)

        certOptions = ctxFactory.ctxFactory
        self.assertEqual(certOptions.method, SSLv23_METHOD)

        ctxFactory.getContext()


    def test_interfaces(self):
        """The service class implements IService.

        """
        verifyObject(IService, self.service)



class ServiceMakerTests(SynchronousTestCase):
    def test_interfaces(self):
        """The serivce maker implements both IServiceMaker and IPlugin.

        """
        sm = WebsiteServiceMaker()
        verifyObject(IServiceMaker, sm)
        verifyObject(IPlugin, sm)
