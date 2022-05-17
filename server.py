from _thread import *
import threading

from queue import Queue
import Pyro5.api

import time

REQUISICAO = 0
LIBERACAO = 1

tokenR1 = True
tokenR2 = True

def pyroThread():
    daemon.requestLoop(); 

timeR1I = time.time()
timeR2I = time.time()

clientCallR1 = None
clientCallR2 = None

@Pyro5.api.expose
class Server(object):
    def requisitar(self, t, callback):
        global tokenR1
        global tokenR2
        global timeR1I
        global timeR2I
        global clientCallR1
        global clientCallR2
        #print("t = " + str(t))
        #print("Requisitar")
        if t == 1:
            if tokenR1 == True:
                #print("Entrou")
                callback._pyroClaimOwnership()
                callback.notification(1)
                tokenR1 = False
                timeR1I = time.time()
                clientCallR1 = callback
            else:
                resource1.put(callback)
        else:
            if tokenR2 == True:
                #print("Entrou")
                callback._pyroClaimOwnership()
                callback.notification(2)
                tokenR2 = False
                timeR2I = time.time()
                clientCallR2 = callback
            else:
                resource2.put(callback)
    
    def liberar(self, t):
        global tokenR1
        global tokenR2
        global clientCallR1
        global clientCallR2
        global teste
        global timeR1I
        global timeR2I
        #print("Liberar")
        #print("Token is " + str(token))
        if t == 1:
            tokenR1 = True
            if not resource1.empty():
                #print("Liberar recurso 1")
                call = resource1.get()
                call._pyroClaimOwnership()
                call.notification(1)
                tokenR1 = False
                timeR1I = time.time()
                #print(timeR1I)
                clientCallR1 = call
                #print("Token is " + str(token))
        else:
            tokenR2 = True
            if not resource2.empty():
                call = resource2.get()
                call._pyroClaimOwnership()
                call.notification(2)
                tokenR2 = False
                timeR2I = time.time()
                clientCallR2 = call
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
    
    if not tokenR1:
        timeR1 = time.time() - timeR1I
       
        if timeR1 == 5:
            #print(timeR1I)
            clientCallR1._pyroClaimOwnership()
            clientCallR1.notification(3)
            #print("Notificação para o recurso 1")
    if not tokenR2:
        timeR2 = time.time() - timeR2I
        if timeR2 == 3:
            clientCallR2._pyroClaimOwnership()
            clientCallR2.notification(4)
            #print("Notificação para o recurso 2")


         
    #command = input("Desligar Servidor (S/N)?\n")
    #if command == 'S' or command == 's':
       #print("Desligando...")
       #break;


