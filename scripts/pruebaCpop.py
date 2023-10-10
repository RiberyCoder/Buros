try:
    from suds.client import Client
    from suds.transport.https import WindowsHttpAuthenticated

    WSDL_URL='https://beco128.baneco.com.bo/wsrpa/wscpop.asmx'
    client = Client(url=WSDL_URL + "?wsdl")
    from suds.sax.element import Element
    from suds.sax.attribute import Attribute
    
    ssnp = Element("soap:Header")
    token_el = Element('cTkTokn')
    token_el.append(Element("Token").setText("c5738789-9b32-4f5a-bc5f-755e84e35e9c"))
    token_el.append(Element("User").setText("RPA"))
    token_el.append(Element("Password").setText("12345"))
    token_el.append(Attribute("xmlns", "http://tempuri.org/"))
    ssnp.append(token_el)
    print(ssnp)
    tokenCpop = GetVar('tokenCpop')
    print(tokenCpop)
    client.set_options(soapheaders={"cTkTokn":{"Token":tokenCpop, "User":"RPA", "Password":"12345"}})
    
    c = client.service.OBTENER_CPOP_RBCPO()
    SetVar('consulta',c)
except Exception as e:
    PrintException()
    raise e