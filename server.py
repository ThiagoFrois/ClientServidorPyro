from _thread import *
import threading

from queue import Queue
import Pyro5.api

REQUISICAO = 0
LIBERACAO = 1

token = True

def pyroThread():
    daemon.requestLoop(); 


# Preciso criar os outros if's para os recurso dois
@Pyro5.api.expose
class Server(object):
    def processServer(self, t):
        global token
        if t == REQUISICAO and token == True:
            token = False
            print("Token is " + str(token))
            return "True"
        elif t == REQUISICAO and token == False:
            print("Token is " + str(token))
        elif t == LIBERACAO:
            token = True
            print("Token is " + str(token))

daemon = Pyro5.server.Daemon() 
ns = Pyro5.api.locate_ns()
uri = daemon.register(Server)
ns.register("server", uri)

resource1 = Queue()
resource2 = Queue()

listener = threading.Thread(target=pyroThread, daemon=True)
listener.start()

print("Pronto")

while(True):
    command = input("Desligar Servidor (S/N)?\n")
    if command == 'S' or command == 's':
       print("Desligando...")
       break;


