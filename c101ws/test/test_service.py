from os.path import dirname, join
from c101ws.service import WebsiteService, WebsiteServiceMaker
from twisted.application.service import IService, IServiceMaker
from twisted.plugin import IPlugin
from twisted.trial.unittest import SynchronousTestCase
from zope.interface.verify import verifyObject


class ServiceTests(SynchronousTestCase):
    def setUp(self):
        certPath = join(dirname(__file__), "test-cert-chain.pem")
        self.service = WebsiteService(_environ={"CERTIFICATE_PATH": certPath})


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
