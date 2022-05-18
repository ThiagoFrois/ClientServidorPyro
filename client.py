from Crypto.Signature import pkcs1_15
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random

import base64

from _thread import *
import threading
import time

import signal


import sys
import os
import Pyro5.api
from Pyro5.api import expose, callback, Daemon, Proxy, oneway, register_class_to_dict, register_dict_to_class

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

exe = False

def timeout():
    print("Reload")

signal.signal(signal.SIGALRM, timeout)

def pyroThread():
    daemon.requestLoop(); 

def pubClassToDict(object):
    return {
        "__class__": "pKey",
    }

def pubDictToClass(classname, d):
    return RSA.RsaKey

def signClassToDict(object):
    return {
        "__class__" : "digitalSign"
    }

def signDictToClass(classname, d):
    return bytes

#register_dict_to_class("pKey", pubDictToClass)
#register_class_to_dict(RSA.RsaKey, pubClassToDict)

#register_dict_to_class("digitalSign", signDictToClass)
#register_class_to_dict(bytes, signClassToDict)

keyP = None

class Client(object):
    @expose
    def possuiChave(self):
        global poChave
        #print("\nCHAVE: " + str(repr(possuiChave)))
        return False
    @expose
    @oneway
    def notification(self, t, asgDigi = None, msg = None, sPub = None):
        global tokenR1
        global tokenR2
        global liberarR1
        global liberarR2
        global poChave
        global keyP
       
        #print("---------- " + str(repr(sPub)))
        #print("CHAVE: " + str(repr(poChave)))
        if not poChave:
            publica = RSA.import_key(sPub)
            keyP = sPub
            #poChave = True
            #print(publica)
            #print('\n\n')
            #print(str(repr(sPub)))
            #print('\n\n')

        else:
            #print('\n\n')
            #print("Já existe")
            #print(str(repr(keyP)))
            #print('\n\n')
            #print(t)
            publica = RSA.import_key(keyP)
            #print(publica)
 


        if asgDigi != None and msg != None:
            #print("Teste")
            publica = RSA.import_key(sPub)
            assina = asgDigi.encode('ISO-8859-1')
            hashB = SHA256.new(msg.encode())

            try:
                pkcs1_15.new(publica).verify(hashB, assina)
                print("\nAssinatura Válida.")
            except (ValueError, TypeError):
                print("\nAssinatura Inválida.")
                #return


        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAbbbbb")
        if t == 1:
            tokenR1 = True
        elif t == 2:
            tokenR2 = True
        elif t == 3:
            #print("KKKKkkkKKKkkkKKKHFHDA")
            tokenR1 = False
            liberarR1 = True
            #print('\n\n\n\n')
            #print(tokenR1)
            #print('\n\n\n\n')
        elif t == 4:
            tokenR2 = False
            liberarR2 = True

callback = Client()

daemon = Daemon()
daemon.register(callback)

listener = threading.Thread(target=pyroThread, daemon=True)
listener.start()
i = 0
num = 5
while(True):
    #print("OLA")
    if liberarR1:
        os.system('clear')
        print("Excedeu o tempo do recurso 1")
        pServer.liberar(1)
        liberarR1 = False
        #exe = False

    if liberarR2:
        os.system('clear')
        print("Execedeu o tempo do recurso 2")
        pServer.liberar(2)
        liberarR2 = False
        #exe = False

    if not exe:
        #os.system('clear')
                
        #try:
        #signal(1)
        if tokenR1:
            print("Possui o token do recurso 1.")
        else:
            print("Não possui o token do recurso 1.")

        if tokenR2:
            print("Possui o token do recurso 2.")
        else:
            print("Não possui o token do recurso 2.")

        #print('\n')
        #print("Possui chave: " + str(repr(possuiChave)))
        #print('\n')
        print("\nMenu:\nSair ------------------------- 0\nRequisitar Recurso 1 --------- 1\nLiberar Recurso 1 ------------ 2\nRequisitar Recurso 2 --------- 3\nLiberar Recurso 2 ------------ 4\nAtualiza Tela ---------------- 5\n")
        try:
            #signal.setitimer(0.5)
            signal.alarm(2)
            num = input("Sua escolha: ")
            #signal.setitimer(0)
            signal.alarm(0)
        except:
            os.system('clear')
            continue
        #signal(0)
        #except:
            #Exception

    #if num == REQUISITAR_R1 or num == REQUISITAR_R2:
        #possuiChave = True

    if num == SAIR:
        os.system('clear')
        print("Saindo...")
        break
    elif num == REQUISITAR_R1 and tokenR1 != True:
        #exe = True
        pServer.requisitar(1, callback)
        
        #print('\n')
        #print(r)
        #print('\n')

        #mB = base64.b64encode(r['data'].encode('utf-8'))
        #print(repr(mB))
        #tk = "tken"
        #print(type(tk))
        #print(tk)
        '''
        if r != None:
            d = r[2]
            hashM = SHA256.new(d.encode())
            #dSign = bytes(r[1]['data'], 'utf-8')
            sg = r[1].encode('ISO-8859-1')
            #print("Tipo: " + str(r[2]) + '\n')
            #print("\nPubO: " + str(repr(r[0]) + '\n'))
            #print("\nPub: " + repr(r[0].encode('ISO-8859-1')) + '\n')
            #print("Data: " + repr(sg) + '\n')
            try: 
                pub = RSA.import_key(r[0])

                #print("Public Key: " + str(repr(pub)))
                #print("Entrou")
                pkcs1_15.new(pub).verify(hashM, sg)
                #print("Assinatura Válida.")
                #time.sleep(1)
            except (ValueError, TypeError):
                print("Assinatura Inválida.")
        '''
        #if r != None:
            #print("Recebeu a chave pública.")
            #print((bytes(r[1]['data'], 'utf-8')))
            #print("Digital signature:" + str(repr(r.encode('ISO-8859-1'))+"\n"))
            #break
    elif num == LIBERAR_R1 and tokenR1 == True:
        #exe = True
        pServer.liberar(1)
        tokenR1 = False
    elif num == REQUISITAR_R2 and tokenR2 != True:
        #exe = True
        pServer.requisitar(2, callback)
    elif num == LIBERAR_R2 and tokenR2 == True:
        #exe = True
        pServer.liberar(2)
        tokenR2 = False

    os.system('clear')
    #else:
        #if num != ATUALIZAR and num != REQUISITAR_R1 and num != LIBERAR_R1 and num != REQUISITAR_R2 and num != LIBERAR_R2:
            #print("Escolha inválida!")

