from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock, mainthread
import os, time, socket
class REST():

    def __init__(self):
        self.__res = []
        self.answer = ''

    def on_success(self,req, result, *args):
        res = result
        self.__res = eval(res)

    def on_success1(self,req, result, *args):
        self.answer = result

    def getRequest(self):
        url = str('http://ladesp.ufms.br/siaf/etcpan/notificacao.php?cpf='+'00000000000')
        req = UrlRequest(url, req_headers='', on_success=self.on_success)
        req.wait()
        return self.__res

    def send_request(self, cpf, cod, *args):
        url = str('http://ladesp.ufms.br/siaf/etcpan/frequencia.php?cpf='+cpf+'&codigo='+cod)
        req = UrlRequest(url, req_headers='', on_success=self.on_success1)
        req.wait()
        return self.answer

def is_connected():
    try:
        host = socket.gethostbyname('www.google.com')
        s = socket.create_connection((host,80),(1/10))
        return True
    except:
        pass
    return False
