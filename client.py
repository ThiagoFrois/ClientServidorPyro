# Nome: Thiago Henrique Frois Menon Cunha
# Ra: 2128080

# Importa biblioteca para a assinatura digital
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

# Importa a biblioteca para threads
from _thread import *
import threading

# Importa a biblioteca para atualizar a tela a cada x segundos
import signal

# Importa biblioteca para limpar tela
import os

# Importa biblioteca Pyro5
from Pyro5.api import expose, callback, Daemon, oneway, Proxy

# Constantes para o menu
SAIR = '0'
REQUISITAR_R1 = '1'
LIBERAR_R1 = '2'
REQUISITAR_R2 = '3'
LIBERAR_R2 = '4'
ATUALIZAR = '5'

# Booleano para controle se já foi guardada a chave pública
haveKey = False

# Booleanos para controlar se possui o token de algum dos recursos
tokenR1 = False
tokenR2 = False

# Booleanos para controle se chegou um notificação do servidor em relação ao tempo de uso do recurso
liberarR1 = False
liberarR2 = False

# Proxy para o servidor
pServer = Proxy("PYRONAME:server")

# Função timeout
def timeout():
    print("Reload")

# Configura sinal de alerta com o timeout
signal.signal(signal.SIGALRM, timeout)

# Função thread para o pyro5
def pyroThread():
    daemon.requestLoop(); 

# Chave pública
keyP = None 

class Client(object):
    # Função para o servidor verificar se o cliente já possui a chave pública
    @expose
    def possuiChave(self):
        global haveKey
        return haveKey
    # Função para o client receber notificações
    @expose
    @oneway
    def notification(self, t, asgDigi = None, msg = None, sPub = None):
        global tokenR1
        global tokenR2
        global liberarR1
        global liberarR2
        global haveKey
        global keyP
        
        # Condicionais para verificar se possui ou não a chave pública
        if not haveKey: # Não possui chave pública
            publica = RSA.import_key(sPub) # Converte para o tipo RSA
            keyP = sPub # Salva a chave pública
            haveKey = True
        else: # Possui chave pública
            publica = RSA.import_key(keyP) # Converte para o tipo RSA
 
        # Condicionais para verificar se a assinatura digital é válida
        if asgDigi != None and msg != None:
            assina = asgDigi.encode('ISO-8859-1') # Converte para o tipo signature (assinatura digital)
            hashB = SHA256.new(msg.encode()) # Cria o hash da mensagem recebida

            try: # Se a comparação é válida a chave é válida
                pkcs1_15.new(publica).verify(hashB, assina)
                print("\nAssinatura Válida.")
            except (ValueError, TypeError): # Se a comparação é inválida a chave é inválida
                print("\nAssinatura Inválida.")
                #return

        # Condicionais das notificações
        if t == 1: # Requisitar recurso 1
            tokenR1 = True
        elif t == 2: # Requisitar recurso 2
            tokenR2 = True
        elif t == 3: # Liberar recurso 1
            tokenR1 = False
            liberarR1 = True
        elif t == 4: # LIberar recurso 2
            tokenR2 = False
            liberarR2 = True

# Registra o client em um daemon para habilitar o recebimento de notificações
callback = Client()
daemon = Daemon()
daemon.register(callback)

# Configura e inicia o thread do pyro5
listener = threading.Thread(target=pyroThread, daemon=True)
listener.start()

# Laço de controle do client
while(True):
    # Condicionais para verificar se houve uma notificação do servidor para liberação do recurso
    if liberarR1: # Acorreu uma notificação para liberação do recurso 1
        os.system('clear')
        print("Excedeu o tempo do recurso 1")
        pServer.liberar(1) # Libera recurso 1
        liberarR1 = False

    if liberarR2: # Acorreu uma notificação para liberação do recurso 2
        os.system('clear')
        print("Execedeu o tempo do recurso 2")
        pServer.liberar(2) # Libera recurso 2
        liberarR2 = False

    # Imprime quais token o client possui e quais não
    if tokenR1:
        print("Possui o token do recurso 1.")
    else:
        print("Não possui o token do recurso 1.")

    if tokenR2:
        print("Possui o token do recurso 2.")
    else:
        print("Não possui o token do recurso 2.")

    # Imprime o menu de opções e espera a seleção da opção
    print("Possui chave: " + str(repr(haveKey)))
    print("\nMenu:\nSair ------------------------- 0\nRequisitar Recurso 1 --------- 1\nLiberar Recurso 1 ------------ 2\nRequisitar Recurso 2 --------- 3\nLiberar Recurso 2 ------------ 4\nAtualiza Tela ---------------- 5\n")
    
    # Atualiza a tela a cada 2 segundos
    try: # Se nenhum input foi digitado dentro de dois segundos realiza o except
        signal.alarm(2)
        num = input("Sua escolha: ")
        signal.alarm(0)
    except:
        os.system('clear')
        continue

    # Condicionais do menu
    if num == SAIR: # Fecha o programa do client
        os.system('clear')
        print("Saindo...")
        break
    elif num == REQUISITAR_R1 and tokenR1 != True: # Verifica se o client pode requisitar o recurso 1
        pServer.requisitar(1, callback)
    elif num == LIBERAR_R1 and tokenR1 == True: # Verifica se o client pode liberar o recurso 1
        pServer.liberar(1)
        tokenR1 = False
    elif num == REQUISITAR_R2 and tokenR2 != True: # Verifica se o client pode requisitar o recurso 2
        pServer.requisitar(2, callback)
    elif num == LIBERAR_R2 and tokenR2 == True: # Verifica se o client pode liebrar o recurso 2
        pServer.liberar(2)
        tokenR2 = False

    os.system('clear')
