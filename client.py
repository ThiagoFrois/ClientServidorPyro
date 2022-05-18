# Nome: Thiago Henrique Frois Menon Cunha
# Ra: 2128080

from Crypto.Signature import pkcs1_15
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

from _thread import *
import threading
import time

import signal

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

poChave = False

tokenR1 = False
tokenR2 = False

liberarR1 = False
liberarR2 = False

pServer = Pyro5.api.Proxy("PYRONAME:server")

def timeout():
    print("Reload")

signal.signal(signal.SIGALRM, timeout)

def pyroThread():
    daemon.requestLoop(); 

keyP = None

class Client(object):
    @expose
    def possuiChave(self):
        global poChave
        return poChave
    @expose
    @oneway
    def notification(self, t, asgDigi = None, msg = None, sPub = None):
        global tokenR1
        global tokenR2
        global liberarR1
        global liberarR2
        global poChave
        global keyP
        
        if not poChave:
            publica = RSA.import_key(sPub)
            keyP = sPub
            poChave = True
        else:
            publica = RSA.import_key(keyP)
 
        if asgDigi != None and msg != None:
            assina = asgDigi.encode('ISO-8859-1')
            hashB = SHA256.new(msg.encode())

            try:
                pkcs1_15.new(publica).verify(hashB, assina)
                print("\nAssinatura Válida.")
            except (ValueError, TypeError):
                print("\nAssinatura Inválida.")
                return

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
    if liberarR1:
        os.system('clear')
        print("Excedeu o tempo do recurso 1")
        pServer.liberar(1)
        liberarR1 = False

    if liberarR2:
        os.system('clear')
        print("Execedeu o tempo do recurso 2")
        pServer.liberar(2)
        liberarR2 = False

    if tokenR1:
        print("Possui o token do recurso 1.")
    else:
        print("Não possui o token do recurso 1.")

    if tokenR2:
        print("Possui o token do recurso 2.")
    else:
        print("Não possui o token do recurso 2.")

    print("Possui chave: " + str(repr(poChave)))
    print("\nMenu:\nSair ------------------------- 0\nRequisitar Recurso 1 --------- 1\nLiberar Recurso 1 ------------ 2\nRequisitar Recurso 2 --------- 3\nLiberar Recurso 2 ------------ 4\nAtualiza Tela ---------------- 5\n")
    try:
        signal.alarm(2)
        num = input("Sua escolha: ")
        signal.alarm(0)
    except:
        os.system('clear')
        continue

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

    os.system('clear')
