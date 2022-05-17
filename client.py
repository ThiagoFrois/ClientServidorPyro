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


def pyroThread():
    daemon.requestLoop(); 

class Client(object):
    @expose
    @oneway
    def notification(self):
        global token
        token = True

callback = Client()

daemon = Daemon()
daemon.register(callback)

listener = threading.Thread(target=pyroThread, daemon=True)
listener.start()

while(True):
    if token:
        print("Possui o token.")
    else:
        print("Não possui o token")
    print("\nMenu:\nSair ----------- 0\nRequisitar ----- 1\nLiberar -------- 2\nAtualiza Tela -- 3\n")
    num = input("Sua escolha: ")
    os.system('clear')
    print(num)
    if num == SAIR:
        os.system('clear')
        print("Saindo...")
        break
    elif num == REQUISITAR and token != True:
        r = pServer.requisitar(1, callback)
        if r != None:
            #print("Token: " + r)
            token = True
    elif num == LIBERAR and token == True:
        r = pServer.liberar(1)
        token = False
        #if r != None:
            #print("Token" + r)
    else:
        if num != ATUALIZAR and num != REQUISITAR and num != LIBERAR:
            print("Escolha inválida!")

