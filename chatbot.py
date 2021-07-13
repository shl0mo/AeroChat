from random import *
import time

class Fila(object):
    def __init__(self):
        self.items = []
 
    def insere(self, elemento):
        self.items.append(elemento)
 
    def retira(self):
        return self.items.pop(0)
 
    def vazia(self):
        return self.items == []

    def tamanho(self):
        return len(self.items)
    
    def imprime(self, fila):
        arquivo = open('voos.txt', 'a')
        if (fila): arquivo.write("Fila de Pouso: \n")
        else: arquivo.write("Fila de Decolagem: \n")
        for i in range(0, self.tamanho()):
            arquivo.write(self.items[i][0] + "\n")
        arquivo.write("\n")
        if (not fila): arquivo.write("--------------------------------\n")
        arquivo.close()

    def contagem(self, lista_comp, companhia):
        total = 0
        identificador = lista_comp[companhia]
        for i in self.items:
            if(i[0:3] == identificador):
                total = total + 1
        return total

    def verifica(self, ident, ordem):
        for i in range(0, self.tamanho()):
            if (self.items[i][0] == ident):
                self.items[i][1] = ordem
                return True            
        return False

    def prioridades(self, ident, ordem):
        for i in range(0, self.tamanho()):
            if (self.items[i][0] ==  ident):
                self.items[i][1] = ordem
                a = 0
                while(self.items[a][1] != 0):
                    a = a + 1
                self.items.insert(a, self.items[i])
                self.items.pop(i + 1)

    def nova_decolagem(self, ident, lista_comp, lista_num):
        ident = ident[0:3]
        for i in range(0, len(lista_comp)):
            if (lista_comp[i] == ident):
                self.insere([lista_comp[i] + str(lista_num[i]),0])
                lista_num[i] = lista_num[i] + 1

def identificador(lista_comp, piloto):
    for i in lista_comp:
        for j in range(0,len(piloto)):
            if (i[0] == piloto[j] and i[1] == piloto[j + 1] and i[2] == piloto[j + 2]):
                return piloto[j:j+7]
    return []

def contem(l1, l2):
    verifica = []
    for i in l1:
        for j in l2:
            if(j == i): verifica.append(True)
            else: verifica.append(False)
    for k in verifica:
        if (k == True): return True
    return False

def sintaxe(piloto, fila):
    torre = ['Torre,', 'torre,', 'TORRE,']
    pouso = ['Pouso', 'pouso', 'POUSO']
    decolagem = ['Decolagem', 'decolagem', 'DECOLAGEM']
    emergencia = ['Emergência', 'Emergencia', 'emergência', 'emergencia', 'EMERGÊNCIA', 'EMERGENCIA']
    piloto = piloto.split(" ")
    if (contem(torre, piloto) and contem(pouso, piloto) and contem(emergencia, piloto)): return 1
    if (fila):
        if (contem(torre, piloto) and contem(pouso, piloto)): return 0
        else: return -1
    else:
        if (contem(torre, piloto) and contem(decolagem, piloto)): return 0
        else: return -1



lista_comp = ['GOL', 'TAM', 'AZU', 'ANA']
lista_num = []
fila_pouso = Fila()
fila_decolagem = Fila()
numero_pouso = randint(7,12)
a = 0
while (a < 4):
  lista_num.append(randint(1000,9999))
  a = a + 1
a = 1
while (a <= numero_pouso):
  companhia  = randint(0,3)
  total_comp = fila_pouso.contagem(lista_comp, companhia)
  while (total_comp == 5):
    companhia  = randint(0,3)
    total_comp = fila_pouso.contagem(lista_comp, companhia)
  fila_pouso.insere([lista_comp[companhia] + str(lista_num[companhia]),0])
  lista_num[companhia] = lista_num[companhia] + 1
  a = a + 1
a = 1
while (a <= 20 - numero_pouso):
  companhia = randint(0,3)
  total_pouso = fila_pouso.contagem(lista_comp, companhia)
  total_decolagem = fila_decolagem.contagem(lista_comp, companhia)
  while (total_pouso + total_decolagem == 5):
    companhia = randint(0,3)
    total_pouso =  fila_pouso.contagem(lista_comp, companhia)
    total_decolagem =  fila_decolagem.contagem(lista_comp, companhia)
  fila_decolagem.insere([lista_comp[companhia] + str(lista_num[companhia]),0])
  lista_num[companhia] = lista_num[companhia] + 1
  a = a + 1

solicitacao = 1
permissao = 1

fila_pouso.imprime(True)
fila_decolagem.imprime(False)
while(True):
    piloto = input("\nPiloto: ")
    ident = identificador(lista_comp, piloto)
    verifica_pouso = fila_pouso.verifica(ident, 1)
    verifica_decolagem = fila_decolagem.verifica(ident, 2)
    sintax = sintaxe(piloto, verifica_pouso)
    while(sintax == -1):
        print("Torre: Sintaxe incorreta. Reenvie a mensagem.")
        piloto = input("\nPiloto: ")
        ident = identificador(lista_comp, piloto)
        verifica_pouso = fila_pouso.verifica(ident, 1)
        verifica_decolagem = fila_decolagem.verifica(ident, 2)
        sintax = sintaxe(piloto, verifica_pouso)
    while (ident == [] or (verifica_pouso == False and verifica_decolagem == False)):
        print("Torre: Identificador de voo invalido.")
        piloto = input('\nPiloto: ')
        ident = identificador(lista_comp, piloto)
        verifica_pouso = fila_pouso.verifica(ident, 1)
        verifica_decolagem = fila_decolagem.verifica(ident, 2)
    if (verifica_pouso):
        if (sintax == 1):
            fila_pouso.prioridades(ident, solicitacao)
            solicitacao = solicitacao + 1
        primeiro = fila_pouso.items[0][0]
        if (primeiro == ident):
            obs = randint(0,100)
            a = 0
            while (obs >= 0 and obs < 26):
                if (a == 0): print("Torre: ", ident + ", aguarde para pousar. Obstáculo na pista.")
                obs = randint(0,100)
                a = a + 1
                time.sleep(5)
            print("Torre: ", ident + ", pouso autorizado.")
            obs = randint(0,100)
            a = 0	
            while(obs <= 5 and obs >= 1):
                if (a == 0): print("Torre: ", ident + ", pouso cancelado. Obstáculo na pista.")
                obs = randint(0,100)
                a = a + 1
                time.sleep(5)
            if (a != 0): print("Torre: ", ident + ", pode realizar o pouso.")
            time.sleep(5)
            print("Torre: ", ident + ", pouso realizado com sucesso.")
            fila_pouso.retira()
            fila_decolagem.nova_decolagem(primeiro, lista_comp, lista_num)
            fila_pouso.imprime(True)
            fila_decolagem.imprime(False)
        else:
                print("Torre: ", ident + ", aguarde na fila de pouso.")        
    else:
        if (ident == fila_decolagem.items[0][0]):
            print("Torre: ", ident + ", decolagem autorizada.")
            time.sleep(5)
            obs = randint(0,10)
            a = 0
            while(obs < 3 and obs >= 1):
                if (a < 1): print("Torre: ", ident + ", decolagem cancelada. Obstáculo na pista.")
                obs = randint(0,10)
                time.sleep(5)
                a = a + 1
            fila_pouso.insere([fila_decolagem.items[0][0],0])
            fila_decolagem.retira()
            if (a != 0): print("Torre: ", ident + ", pode realizar a decolagem.")
            time.sleep(5)
            print("Torre: ", ident + ", decolagem realizada com sucesso.")
            fila_pouso.imprime(True)
            fila_decolagem.imprime(False)
        else:
            print("Torre: ", ident + ", aguarde na fila de decolagem.")
