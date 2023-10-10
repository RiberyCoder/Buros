from suds.client import Client
from suds.wsse import *
from suds.transport.https import HttpAuthenticated
from suds.transport import TransportError
from urllib.request import HTTPSHandler
import ssl
global ssl
import urllib
global urllib
global TransportError
class HttpHeaderModify(HttpAuthenticated):
    def u2handlers(self):
        try:
            global HttpAuthenticated, HTTPSHandler
            # use handlers from superclass
            handlers = HttpAuthenticated.u2handlers(self)
            # create custom ssl context, e.g.:
            ctx = ssl._create_unverified_context()
            # configure context as needed...
            ctx.check_hostname = False
            # add a https handler using the custom context
            var=HTTPSHandler(context=ctx)
            handlers.append(var)
            return handlers
        except Exception as e:
            PrintException()
            raise e


    def open(self, request):
        try:
            #global ssl
            # This restores the same behavior as before.
            #context = ssl._create_unverified_context()
            #print (context)
            #urllib.urlopen("https://no-valid-cert", context=context)
            url = request.url
            #u2request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})
            u2request = urllib.request.Request(url, None, headers={'User-Agent': 'Mozilla'})
            self.proxy = self.options.proxy
            return self.u2open(u2request)
        except Exception as e:
            PrintException()
            raise TransportError(str(e))
try:
	transport = HttpHeaderModify()
	ws_INFOCRED = GetVar('ws_INFOCRED')
	#prod
	#client = Client("https://www.infocred.bo/BICService/BICService.svc?wsdl", transport=transport, timeout=10)
	print (transport)
	client = Client(""+ws_INFOCRED+"", transport=transport, timeout=100)
	client.set_options(headers={'User-Agent': 'Mozilla'})
	username=GetVar('userInfocred')
	password=GetVar('passInfocred')
	#Parametros para las clase Titular
	titipdoc=GetVar('titularTipoDocumento')
	tidoc=GetVar('titularDocumento')
	tinom=GetVar('titularNombre')
	#Parametros para la clase Usuario
	usnom = GetVar('usuarioNombreCompleto')
	usdoc = GetVar('usuarioDocumento')
	#Funcionalidad
	security = Security()
	token = UsernameToken(username, password)
	security.tokens.append(token)
	client.set_options(wsse=security)
	titular = client.factory.create('Titular')
	titular.TipoDocumento = titipdoc
	titular.Documento = tidoc
	titular.NombreCompleto = tinom
	usuario = client.factory.create('Usuario')
	usuario.NombreCompleto = usnom
	usuario.Documento = usdoc
	result = client.service.GetInfoPlusIJ(titular,usuario,True)
	SetVar('dataInfocred',result)
	print(result)
except Exception as e:
	PrintException()
	raise e