from _thread import *
import threading

import sys
import os
import Pyro5.api
from Pyro5.api import expose, callback, Daemon, Proxy, oneway

REQUISICAO = 0
LIBERACAO = 1

SAIR = '0'
REQUISITAR_R1 = '1'
LIBERAR_R1 = '2'
REQUISITAR_R2 = '3'
LIBERAR_R2 = '4'
ATUALIZAR = '5'

tokenR1 = False
tokenR2 = False

pServer = Pyro5.api.Proxy("PYRONAME:server")


def pyroThread():
    daemon.requestLoop(); 

class Client(object):
    @expose
    @oneway
    def notification(self, t):
        global tokenR1
        global tokenR2
        if t == 1:
            tokenR1 = True
        else:
            tokenR2 = True

callback = Client()

daemon = Daemon()
daemon.register(callback)

listener = threading.Thread(target=pyroThread, daemon=True)
listener.start()

while(True):
    if tokenR1:
        print("Possui o token do recurso 1.")
    else:
        print("Não possui o token do recurso 1.")

    if tokenR2:
        print("Possui o token do recurso 2.")
    else:
        print("Não possui o token do recurso 2.")

    print("\nMenu:\nSair ------------------------- 0\nRequisitar Recurso 1 --------- 1\nLiberar Recurso 1 ------------ 2\nRequisitar Recurso 2 --------- 3\nLiberar Recurso 2 ------------ 4\nAtualiza Tela ---------------- 5\n")
    num = input("Sua escolha: ")
    os.system('clear')
    print(num)
    if num == SAIR:
        os.system('clear')
        print("Saindo...")
        break
    elif num == REQUISITAR_R1 and tokenR1 != True:
        pServer.requisitar(1, callback)
    elif num == LIBERAR_R1 and tokenR1 == True:
        pServer.liberar(1)
        tokenR1 = False
    elif num == REQUISITAR_R2 and tokenR2 != True:
        pServer.requisitar(2, callback)
    elif num == LIBERAR_R2 and tokenR2 == True:
        pServer.liberar(2)
        tokenR2 = False
    else:
        if num != ATUALIZAR and num != REQUISITAR_R1 and num != LIBERAR_R1 and num != REQUISITAR_R2 and num != LIBERAR_R2:
            print("Escolha inválida!")

