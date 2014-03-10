from c101ws.web import secureSite, insecureSite
from clarent.certificate import SecureCiphersContextFactory
from os import environ
from twisted.application.service import Service, IServiceMaker
from twisted.internet import reactor
from twisted.internet.endpoints import SSL4ServerEndpoint, TCP4ServerEndpoint
from twisted.internet.ssl import PrivateCertificate
from twisted.plugin import IPlugin
from twisted.python.usage import Options
from zope.interface import implementer


class WebsiteService(Service):
    def __init__(self, _environ=environ, _reactor=reactor):
        self._environ = environ
        self._reactor = reactor


    def startService(self):
        TCP4ServerEndpoint(self._reactor, 80).listen(insecureSite())

        with open(self._environ["CERTIFICATE_PATH"]) as f:
            pemData = f.read()
        cert = PrivateCertificate.loadPEM(pemData)
        ctxFactory = SecureCiphersContextFactory(cert.options())
        sslEndpoint = SSL4ServerEndpoint(self._reactor, 443, ctxFactory)
        sslEndpoint.listen(secureSite())
        Service.startService(self)



@implementer(IServiceMaker, IPlugin)
class WebsiteServiceMaker(object):
    tapname = "c101ws"
    options = Options
    description ="Crypto 101 website"

    def makeService(self, _options):
        return WebsiteService()
