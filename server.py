# Nome: Thiago Henrique Frois Menon Cunha
# Ra: 2128080

# Importa biblioteca para a assinatura digital
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

# Importa a biblioteca para threads
from _thread import *
import threading

# Importa a biblioteca para filas
from queue import Queue
import Pyro5.api

# Importa a biblioteca para realizar o timeout
import time

# Constante para recurso 1
RECURSO1 = 1

tokenR1 = True # Token para o recurso 1
tokenR2 = True # Token para o recurso 2

# Cria uma chave RSA
random_seed = Random.new().read
keyPair = RSA.generate(1024, random_seed)
pubKeyR = keyPair.publickey().export_key()

# Mensagem que será enviada na notificação para verificar assinatura digital
TOKEN = "token"

# Cria o hash do token
hashA = SHA256.new(TOKEN.encode())

# Cria assinatura digital para o hash
digitalSign = pkcs1_15.new(keyPair).sign(hashA)

# Realiza o decode na chave pública
pubKey = pubKeyR.decode('ISO-8859-1')

# Realiza o decode na assinatura digital
digiSign = digitalSign.decode('ISO-8859-1')

# Thread para o pyro5
def pyroThread():
    daemon.requestLoop(); 

#Controles de tempo para realizar o timeout
timeR1I = time.time()
timeR2I = time.time()

# Clientes usando cada recurso
clientCallR1 = None
clientCallR2 = None

@Pyro5.api.expose
class Server(object):
    # Requisitar recurso
    def requisitar(self, t, callback):
        global tokenR1
        global tokenR2
        global timeR1I
        global timeR2I
        global clientCallR1
        global clientCallR2
        global firstRequest
        if t == RECURSO1: # Recurso 1
            if tokenR1 == True: # Recurso disponível
                callback._pyroClaimOwnership()
                aux = callback.possuiChave() # Verifica se o client já possui a chave pública

                if aux:
                    print("R1: Possui chave!")
                    callback.notification(1, digiSign, TOKEN) # Concede o token
                else:
                    print("R1: Não possui chave!")
                    callback.notification(1, digiSign, TOKEN, pubKey) # Concede o token
                tokenR1 = False
                timeR1I = time.time() # Inicia timer de uso do recurso pelo client
                clientCallR1 = callback
            else: # Recurso não disponível
                resource1.put(callback) # Coloca o client na fila do recurso 1
        else: # Recurso 2
            if tokenR2 == True: # Recurso disponível
                callback._pyroClaimOwnership()
                aux = callback.possuiChave() # Verifica se o client já possui a chave pública 
                if aux:
                    print("R2: Possui chave!")
                    callback.notification(2, digiSign, TOKEN) # Concede o token
                else:
                    print("R2: Não possui chave!")
                    callback.notification(2, digiSign, TOKEN, pubKey) # Concede o token

                tokenR2 = False
                timeR2I = time.time() # Inicia timer de uso do recurso pelo client
                clientCallR2 = callback
            else: # Recurso não disponível
                resource2.put(callback) # Coloca o client na fila do recurso 2
    
    # Liberar recurso
    def liberar(self, t):
        global tokenR1
        global tokenR2
        global clientCallR1
        global clientCallR2
        global teste
        global timeR1I
        global timeR2I
        if t == RECURSO1: # Recurso 1
            tokenR1 = True # Token devolvido
            if not resource1.empty(): # Recurso esperando liberação
                call = resource1.get() # Obtém o primeiro client da fila do recurso 1
                call._pyroClaimOwnership()
                aux = call.possuiChave() # Verifica se o client já possui a chave pública

                if aux:
                    print("L1: Possui chave!")
                    call.notification(1, digiSign, TOKEN) # Apaga token no client (vai para false)
                else:
                    print("L1: Não possui chave!")
                    call.notification(1, digiSign, TOKEN, pubKey) # Apaga token no client (vai para false)

                tokenR1 = False # Enviou o token para outro client na fila do recurso 1
                timeR1I = time.time() # Inicia timer de uso do recurso pelo client
                clientCallR1 = call # Salva o client que está utilizando o recurso
        else: # Recurso 2
            tokenR2 = True
            if not resource2.empty(): # Recurso esperando liberação
                call = resource2.get() # Obtém o primeiro client da fila do recurso 2
                call._pyroClaimOwnership()
                aux = call.possuiChave() # Verifica se o client já possui a chave pública
                if aux:
                    print("L2: Possui chave!")
                    call.notification(2, digiSign, TOKEN) # Apaga token no client (vai para false)
                else:
                    print("L2: Não possui chave!")
                    call.notification(2, digiSign, TOKEN, pubKey) # Apaga token no client (vai para false)
                
                tokenR2 = False # Enviou o token para outro client na fila do recurso 2
                timeR2I = time.time() # Inicia timer de uso do recurso pelo client
                clientCallR2 = call # Salva o client que está utilizando o recurso


# Configura servidor de nomes
daemon = Pyro5.server.Daemon() 
ns = Pyro5.api.locate_ns()
uri = daemon.register(Server)
ns.register("server", uri)

# Filas dos recursos
resource1 = Queue()
resource2 = Queue()

# Configura thread do pyro5
listener = threading.Thread(target=pyroThread, daemon=True)
listener.start()

# Laço de controle do servidor
print("Pronto")
while(True):
    
    if not tokenR1: # Verifica se algum client está usando o recurso 1
        timeR1 = time.time() - timeR1I
       
        if timeR1 == 5: # Verifica se o client atingiu o tempo de uso do recurso
            clientCallR1._pyroClaimOwnership()
            aux = clientCallR1.possuiChave() # Verifica se o client já possui a chave pública
            if aux:
                print("T1: Possui chave!")
                clientCallR1.notification(3, digiSign, TOKEN) # Notifica o client para liberar o recurso 1
            else:
                print("T1: Não possui chave!")
                clientCallR1.notification(3, digiSign, TOKEN, pubKey) # Notifica o client para liberar o recurso 1
    if not tokenR2: # Verifica se algum client está usando o recurso 1
        timeR2 = time.time() - timeR2I
        if timeR2 == 3: # Verifica se o client atingiu o tempo de uso do recurso
            clientCallR2._pyroClaimOwnership()
            aux = clientCallR2.possuiChave() # Verifica se o client já possui a chave pública
            if aux:
                print("T2: Possui chave!")
                clientCallR2.notification(4, digiSign, TOKEN) # Notifica o client para liberar o recurso 2
            else:
                print("T2: Não possui chave!")
                clientCallR2.notification(4, digiSign, TOKEN, pubKey) # Notifica o client para liberar o recurso 2
