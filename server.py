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


keyPairR2 = RSA.generate(1024, random_seed)
pubKeyR2 = keyPairR2.publickey()

 
TOKEN = "token"

print("tk" + str(type(TOKEN)))

print("Tipo: " + str(type(pubKeyR1)))

hashA = SHA256.new(TOKEN.encode())
digitalSignR1 = pkcs1_15.new(keyPairR1).sign(hashA)

#digitalSignR2 = pkcs1_15.new(keyPairR2).sign(hashA)


print("digital: " + str(type(digitalSignR1)))

outSign = pubKeyR1.decode('ISO-8859-1')

print("OUt: " + str(outSign))

data = digitalSignR1


#print('\nInput:')
#print(data)
#print(type(data))
  
# converting
output = data.decode('ISO-8859-1')

# display output
#print('\nOutput:')
#print(output)
#print(type(output))


#print("\nTeste\n\n")
#print(output.encode('ISO-8859-1'))
#ds = digitalSignR1().decode()

#print("Tipo: " + repr(type(digitalSignR1)))

#print("Hash A:" + repr(hashA) + "\n")

#print("Digital signature:" + repr(digitalSignR1)+"\n")
#print("Digital signature:" + repr(digitalSignR2)+"\n")

print("\nPub: " + str(repr(pubKeyR1)) + '\n')
print("Data: " + repr(data) + '\n')

hashB = SHA256.new("token".encode())


try: 
    #pkcs1_15.new(pubKeyR1).verify(hashB, data)
    print("Assinatura Válida.")
except (ValueError, TypeError):
    print("Assinatura Inválida.")

def pyroThread():
    daemon.requestLoop(); 

timeR1I = time.time()
timeR2I = time.time()

clientCallR1 = None
clientCallR2 = None

def pubClassToDict(object):
    return {
        "__class__": "pKey",
    }

def pubDictToClass(classname, d):
    return pubKeyR1
    #return RsaKey.publickey()

#register_class_to_dict(pubKeyR1, pubClassToDict)

key = RSA.import_key(open('private_key.der').read())

print("TIPO DA CHAVE: " + str(type(key)))

#priv = "MIICWwIBAAKBgG3u4n82BqIIY7dtSIZcOYHtYv3ErijZzQaPK52HeKYxgrWH1Mvx stQI6+SMJXhJPYkWWVPTqkWtkVPC1yidqLkYT6cJSTtg9LE2QsueHKVZfjEKZfnv NJ4c07Sky9R28TXnG816VorxyrHSzocCvcfb54cswxuaD8UfocjMyK1TAgMBAAEC gYBWs2uw1oQesK0sUiU7ymqUfQtwhviwQS5A+RN19w0BTdT/pHQAsMvQDIU2yA0Z M/IzNwwWX75Pm9cdD3KvlsAkyfJCqPoPOT5Y1r0GfpaS15Hz+hLKWdu0tQfR/nq/ mFgOViMi5JdCO3OBsIYYc/8HJeXtZIUF1BjVhnWgck/ieQJBALFCHge1A4+iiJBs pVlL0pG/GYQUXRKE7+S+ega6hWa9vWui1MzQc7aO3nFPO6J6Prx7LBdKxdqWRt9Z sIWh/A8CQQCexIbOUCEyQY0kOZt4kCvRUQLe+gdYkVEIIaLGda8I86Y3YgEz/nYx z0R/7w53BmBrlqMd0Y34+W7hfhJnc8Z9AkA+GOqKSqivtgHfjqAyczSWaHsY4UVl ynp8CRqYptk7D/d+8LFZ+yC+cLiOu3IpzmeSAhiFJGXB2OmFL1d+ySuTAkBWEaQi 5D2ayP6CzNgDm+SlLI2p41FoKh8LkXB0tgeVisBo9bBBR4k7p2kzEZ192O8cZCU5 XQjiGBaMF5RSkOjhAkEAhcM6XV6yWWdqzs0SUJbLtaYK4Hv1Z89f00QWlDXN6W55 69J8n3Niy6jCTqjr3hD6HWCx0ygUulgRC29Suioi8Q=="

def signClassToDict(object):
    return {
        "__class__" : "digitalSign"
    }

def signDictToClass(classname, d):
    return bytes

#register_dict_to_class("pKey", pubDictToClass)
#register_class_to_dict(RSA.RsaKey, pubClassToDict)
#register_class_to_dict(pubKeyR1, pubClassToDict)


#register_dict_to_class("digitalSign", signDictToClass)
#register_class_to_dict(bytes, signClassToDict)

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
        #print("t = " + str(t))
        #print("Requisitar")
        if t == 1:
            if tokenR1 == True:
                #print("Entrou")
                callback._pyroClaimOwnership()
                callback.notification(1, outSign, output, TOKEN)
                tokenR1 = False
                timeR1I = time.time()
                clientCallR1 = callback
                #print("Digital signature (Teste):" + repr(digitalSignR1)+"\n")
                return (outSign, output, TOKEN) 
                #print(type(ds))
                #return output
            else:
                resource1.put(callback)
        else:
            if tokenR2 == True:
                #print("Entrou")
                callback._pyroClaimOwnership()
                callback.notification(2, outSign, output, TOKEN)
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
                call.notification(1, outSign, output, TOKEN)
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
                call.notification(2, outSign, output, TOKEN)
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
            clientCallR1.notification(3, outSign, output, TOKEN)
            #print("Notificação para o recurso 1")
    if not tokenR2:
        timeR2 = time.time() - timeR2I
        if timeR2 == 3:
            clientCallR2._pyroClaimOwnership()
            clientCallR2.notification(4, outSign, output, TOKEN)
            #print("Notificação para o recurso 2")


         
    #command = input("Desligar Servidor (S/N)?\n")
    #if command == 'S' or command == 's':
       #print("Desligando...")
       #break;


