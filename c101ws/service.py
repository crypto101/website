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


class Service(Service):
    def __init__(self, _environ=environ):
        self._httpEndpoint = TCP4ServerEndpoint(reactor, 80)
        with open(_environ["CERTIFICATE_PATH"]) as f:
            pemData = f.read()
        cert = PrivateCertificate.loadPEM(pemData)
        ctxFactory = SecureCiphersContextFactory(cert.options())
        self._tlsEndpoint = SSL4ServerEndpoint(reactor, 443, ctxFactory)


    def startService(self):
        self._httpEndpoint.listen(insecureSite())
        self._tlsEndpoint.listen(secureSite())



@implementer(IServiceMaker, IPlugin)
class ServiceMaker(object):
    tapname = "c101ws"
    options = Options
    description ="Crypto 101 website"

    def makeService(self, _options):
        return Service()
