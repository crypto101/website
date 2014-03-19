from c101ws.service import WebsiteService, WebsiteServiceMaker
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
            "ENV_VARS_PATH": localPath("env-vars.json"),
            "CERTIFICATE_PATH": localPath("test-cert-chain.pem"),
            "DH_PARAMETERS_PATH": localPath("test-dh-parameters.pem")
        })


    def test_loadEnvVars(self):
        self.assertNotIn("LOADED_ENV_VAR_KEY", self.service._environ)
        self.service._loadEnvVars()
        self.assertEqual(self.service._environ["LOADED_ENV_VAR_KEY"],
                         "LOADED_ENV_VAR_VALUE")


    def test_contextFactory(self):
        """The context factory produces pragmatic, secure SSL contexts.

        """
        ctxFactory = self.service._getCtxFactory()
        self.assertEqual(ctxFactory.method, SSLv23_METHOD)
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
