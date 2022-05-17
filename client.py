from _thread import *
import threading

import sys
import os
import Pyro5.api
from Pyro5.api import expose, callback, Daemon, Proxy, oneway

REQUISICAO = 0
LIBERACAO = 1

SAIR = '0'
REQUISITAR = '1'
LIBERAR = '2'
ATUALIZAR = '3'

token = False

pServer = Pyro5.api.Proxy("PYRONAME:server")


# Ver como receber um notificação
def pyroThread():
    daemon.requestLoop(); 

@Pyro5.api.expose
class Client(object):
    def notification(self):
        return True

callback = Client()

daemon = Daemon()
daemon.register(callback)

listener = threading.Thread(target=pyroThread, daemon=True)
listener.start()

while(True):
    print("Token is " + str(token))
    print("\nMenu:\nSair ----------- 0\nRequisitar ----- 1\nLiberar -------- 2\nAtualiza Tela -- 3\n")
    num = input("Sua escolha: ")
    os.system('clear')
    print(num)
    if num == SAIR:
        os.system('clear')
        print("Saindo...")
        break
    elif num == REQUISITAR and token != True:
        print("R")
        r = pServer.processServer(REQUISICAO)
        if r != None:
            print("Token: " + r)
            token = True
    elif num == LIBERAR and token == True:
        print("L")
        r = pServer.processServer(LIBERACAO)
        token = False
        if r != None:
            print("Token" + r)
    else:
        if num != ATUALIZAR and num != REQUISITAR and num != LIBERAR:
            print("Escolha inválida!")

