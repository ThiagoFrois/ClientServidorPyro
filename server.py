from _thread import *
import threading

from queue import Queue
import Pyro5.api

REQUISICAO = 0
LIBERACAO = 1

tokenR1 = True
tokenR2 = True

def pyroThread():
    daemon.requestLoop(); 


# Preciso criar os outros if's para os recurso dois
@Pyro5.api.expose
class Server(object):
    def requisitar(self, t, callback):
        global tokenR1
        global tokenR2
        #print("t = " + str(t))
        if t == 1:
            if tokenR1 == True:
                #print("Entrou")
                callback._pyroClaimOwnership()
                callback.notification(1)
                tokenR1 = False
            else:
                resource1.put(callback)
        else:
            if tokenR2 == True:
                #print("Entrou")
                callback._pyroClaimOwnership()
                callback.notification(2)
                tokenR2 = False
            else:
                resource2.put(callback)
    
    def liberar(self, t):
        global tokenR1
        global tokenR2
        #print("Token is " + str(token))
        if t == 1:
            tokenR1 = True
            if not resource1.empty():
                call = resource1.get()
                call._pyroClaimOwnership()
                call.notification(1)
                tokenR1 = False
                #print("Token is " + str(token))
        else:
            tokenR2 = True
            if not resource2.empty():
                call = resource2.get()
                call._pyroClaimOwnership()
                call.notification(2)
                tokenR2 = False
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


