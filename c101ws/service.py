from c101ws.web import secureSite, insecureSite
from clarent.certificate import SecureCiphersContextFactory
from os import environ
from OpenSSL.SSL import SSLv23_METHOD
from pem import certificateOptionsFromFiles
from twisted.application.service import Service, IServiceMaker
from twisted.internet import reactor
from twisted.internet.endpoints import SSL4ServerEndpoint, TCP4ServerEndpoint
from twisted.plugin import IPlugin
from twisted.python.usage import Options
from zope.interface import implementer


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
        ctxFactory = certificateOptionsFromFiles(certPath,
            method=SSLv23_METHOD)

        return SecureCiphersContextFactory(ctxFactory)



@implementer(IServiceMaker, IPlugin)
class WebsiteServiceMaker(object):
    tapname = "c101ws"
    options = Options
    description ="Crypto 101 website"

    def makeService(self, _options):
        return WebsiteService()
