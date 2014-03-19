from c101ws.web import secureSite, insecureSite
from json import load
from os import environ
from pem import certificateOptionsFromFiles, DiffieHellmanParameters
from twisted.application.service import Service, IServiceMaker
from twisted.internet import reactor
from twisted.internet.endpoints import SSL4ServerEndpoint, TCP4ServerEndpoint
from twisted.plugin import IPlugin
from twisted.python.filepath import FilePath
from twisted.python.usage import Options
from zope.interface import implementer


class WebsiteService(Service):
    def __init__(self, _environ=environ, _reactor=reactor):
        self._environ = _environ
        self._reactor = _reactor


    def privilegedStartService(self):
        self._loadEnviron()

        TCP4ServerEndpoint(self._reactor, 80).listen(insecureSite())

        ctxFactory = self._getCtxFactory()
        sslEndpoint = SSL4ServerEndpoint(self._reactor, 443, ctxFactory)
        sslEndpoint.listen(secureSite(self._environ))


    def _getCtxFactory(self):
        dhParamPath = FilePath(self._environ["DH_PARAMETERS_PATH"])
        dhParameters = DiffieHellmanParameters.fromFile(dhParamPath)

        ctxFactory = certificateOptionsFromFiles(
            self._environ["CERTIFICATE_PATH"],
            dhParameters=dhParameters)

        return ctxFactory


    def _loadEnvVars(self):
        """
        Load a bunch of environment local environemnt variables.
        """
        with open(self._environ["ENV_VARS_PATH"]) as f:
            envVars = load(f)
        self._environ.update(envVars)



@implementer(IServiceMaker, IPlugin)
class WebsiteServiceMaker(object):
    tapname = "c101ws"
    options = Options
    description ="Crypto 101 website"

    def makeService(self, _options):
        return WebsiteService()
