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

liberarR1 = False
liberarR2 = False

pServer = Pyro5.api.Proxy("PYRONAME:server")


def pyroThread():
    daemon.requestLoop(); 

class Client(object):
    @expose
    @oneway
    def notification(self, t):
        global tokenR1
        global tokenR2
        global liberarR1
        global liberarR2
        if t == 1:
            tokenR1 = True
        elif t == 2:
            tokenR2 = True
        elif t == 3:
            tokenR1 = False
            liberarR1 = True
        elif t == 4:
            tokenR2 = False
            liberarR2 = True

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

    if liberarR1:
        os.system('clear')
        print("Excedeu o tempo do recurso 1")
        pServer.liberar(1)
        liberarR1 = False
        continue

    if liberarR2:
        print("Execedeu o tempo do recurso 2")
        pServer.liberar(2)
        liberarR2 = False
        continue

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
    #else:
        #if num != ATUALIZAR and num != REQUISITAR_R1 and num != LIBERAR_R1 and num != REQUISITAR_R2 and num != LIBERAR_R2:
            #print("Escolha inválida!")

