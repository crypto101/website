from c101ws.web import secureSite, insecureSite
from clarent.certificate import SecureCiphersContextFactory
from os import environ
from twisted.application.service import Service, ServiceMaker
from twisted.internet import reactor
from twisted.internet.endpoints import SSL4ServerEndpoint, TCP4ServerEndpoint
from twisted.internet.ssl import PrivateCertificate
from twisted.python.usage import Options


class Service(Service):
    def __init__(self):
        self._httpEndpoint = TCP4ServerEndpoint(reactor, 80)
        cert = PrivateCertificate.loadPEM(environ.get("CERTIFICATE"))
        ctxFactory = SecureCiphersContextFactory(cert.options())
        self._tlsEndpoint = SSL4ServerEndpoint(reactor, 443, ctxFactory)


    def startService(self):
        self._httpEndpoint.listen(insecureSite())
        self._tlsEndpoint.listen(secureSite())



class ServiceMaker(ServiceMaker):
    tapname = "c101ws"
    options = Options
    description ="Crypto 101 website"


    def makeService(self, _options):
        return Service()
