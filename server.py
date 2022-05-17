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
    def requisitar(self, t, callback):
        global token
        if token == True:
            token = False
            #print("Token is " + str(token))
            return "True"
        else:
            #print("Token is " + str(token))
            if t == 1:
                resource1.put(callback)
            #elif t == 2:
                #resource2.put(callback)
    def liberar(self, t):
        global token
        token = True
        #print("Token is " + str(token))
        if not resource1.empty():
            call = resource1.get()
            call._pyroClaimOwnership()
            call.notification()
            token = False
            #print("Token is " + str(token))

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


