from c101ws.web import secureSite, insecureSite
from clarent.certificate import SecureCiphersContextFactory
from os import environ
from OpenSSL.SSL import SSLv23_METHOD
from twisted.application.service import Service, IServiceMaker
from twisted.internet import reactor
from twisted.internet.endpoints import SSL4ServerEndpoint, TCP4ServerEndpoint
from twisted.internet.ssl import PrivateCertificate
from twisted.plugin import IPlugin
from twisted.python.usage import Options
from zope.interface import implementer


class CertChainContextFactory(object):
    def __init__(self, ctxFactory, certChainPath):
        self.ctxFactory = ctxFactory
        self.certChainPath = certChainPath


    def getContext(self):
        ctx = self.ctxFactory.getContext()
        ctx.use_certificate_chain_file(self.certChainPath)
        return ctx



class WebsiteService(Service):
    def __init__(self, _environ=environ, _reactor=reactor):
        self._environ = _environ
        self._reactor = _reactor


    def privilegedStartService(self):
        TCP4ServerEndpoint(self._reactor, 8000).listen(insecureSite())

        ctxFactory = self._getCtxFactory()
        sslEndpoint = SSL4ServerEndpoint(self._reactor, 4430, ctxFactory)
        sslEndpoint.listen(secureSite(self._environ))


    def _getCtxFactory(self):
        certPath = self._environ["CERTIFICATE_PATH"]
        with open(certPath) as f:
            pemData = f.read()

        ctxFactory = PrivateCertificate.loadPEM(pemData).options()
        ctxFactory.method = SSLv23_METHOD

        ctxFactory = SecureCiphersContextFactory(ctxFactory)
        ctxFactory = CertChainContextFactory(ctxFactory, certPath)

        theContext = ctxFactory.getContext()
        return lambda: theContext



@implementer(IServiceMaker, IPlugin)
class WebsiteServiceMaker(object):
    tapname = "c101ws"
    options = Options
    description ="Crypto 101 website"

    def makeService(self, _options):
        return WebsiteService()
