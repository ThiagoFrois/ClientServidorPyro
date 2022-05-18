from Crypto.Signature import pkcs1_15
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

from _thread import *
import threading

from Pyro5.api import register_class_to_dict, register_dict_to_class, config

from queue import Queue
import Pyro5.api

import time

config.SERIALIZER = "serpent"

REQUISICAO = 0
LIBERACAO = 1

tokenR1 = True
tokenR2 = True

random_seed = Random.new().read

keyPairR1 = RSA.generate(1024, random_seed)
pubKeyR1 = keyPairR1.publickey().export_key()

TOKEN = "token"

hashA = SHA256.new(TOKEN.encode())
digitalSignR1 = pkcs1_15.new(keyPairR1).sign(hashA)

outSign = pubKeyR1.decode('ISO-8859-1')

data = digitalSignR1

output = data.decode('ISO-8859-1')

hashB = SHA256.new("token".encode())

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
        global firstRequest
        if t == 1:
            if tokenR1 == True:
                callback._pyroClaimOwnership()
                aux = callback.possuiChave()

                if aux:
                    print("R1: Possui chave!")
                    callback.notification(1, output, TOKEN)
                else:
                    print("R1: Não possui chave!")
                    callback.notification(1, output, TOKEN, outSign)
                tokenR1 = False
                timeR1I = time.time()
                clientCallR1 = callback
                return (outSign, output, TOKEN) 
            else:
                resource1.put(callback)
        else:
            if tokenR2 == True:
                callback._pyroClaimOwnership()
                aux = callback.possuiChave()
                if aux:
                    print("R2: Possui chave!")
                    callback.notification(2, output, TOKEN)
                else:
                    print("R2: Não possui chave!")
                    callback.notification(2, output, TOKEN, outSign)

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
        if t == 1:
            tokenR1 = True
            if not resource1.empty():
                call = resource1.get()
                call._pyroClaimOwnership()
                aux = call.possuiChave()

                if aux:
                    print("L1: Possui chave!")
                    call.notification(1, output, TOKEN)
                else:
                    print("L1: Não possui chave!")
                    call.notification(1, output, TOKEN, outSign)

                tokenR1 = False
                timeR1I = time.time()
                clientCallR1 = call
        else:
            tokenR2 = True
            if not resource2.empty():
                call = resource2.get()
                call._pyroClaimOwnership()
                aux = call.possuiChave()
                if aux:
                    print("L2: Possui chave!")
                    call.notification(2, output, TOKEN)
                else:
                    print("L2: Não possui chave!")
                    call.notification(2, output, TOKEN, outSign)
                
                tokenR2 = False
                timeR2I = time.time()
                clientCallR2 = call

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
            clientCallR1._pyroClaimOwnership()
            aux = clientCallR1.possuiChave()
            if aux:
                print("T1: Possui chave!")
                clientCallR1.notification(3, output, TOKEN)
            else:
                print("T1: Não possui chave!")
                clientCallR1.notification(3, output, TOKEN, outSign)
    if not tokenR2:
        timeR2 = time.time() - timeR2I
        if timeR2 == 3:
            clientCallR2._pyroClaimOwnership()
            aux = clientCallR2.possuiChave()
            if aux:
                print("T2: Possui chave!")
                clientCallR2.notification(4, output, TOKEN)
            else:
                print("T2: Não possui chave!")
                clientCallR2.notification(4, output, TOKEN, outSign)
