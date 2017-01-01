# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import sys
import os
import time
import shutil
from datetime import datetime

class Ini_GPIO(object):
    def __init__(self):
        self.GPIOList = [40, 38, 37, 36, 35]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
    def outGpio(self):
        for i in self.GPIOList:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)
    def inGpio(self):
        GPIO.setup(15, GPIO.IN)
    def clearGpio(self):
        GPIO.cleanup()
        
class Programas(object):
    def __init__(self, programa):
        if programa == "MS":
            self.tipo = "Muito Sujas"
            self.tempo = 240
            self.ciclo = 360
        elif programa == "PE":
            self.tipo = "Pesadas"
            self.tempo = 210
            self.ciclo = 315
        elif programa == "BR":
            self.tipo = "Brancas"
            self.tempo = 180
            self.ciclo = 270
        elif programa == "JE":
            self.tipo = "Jeans"
            self.tempo = 150
            self.ciclo = 225
        elif programa == "ED":
            self.tipo = "Edredom"
            self.tempo = 130
            self.ciclo = 180
        elif programa == "CO":
            self.tipo = "Coloridas"
            self.tempo = 90
            self.ciclo = 135
        elif programa == "DE":
            self.tipo = "Delicadas"
            self.tempo = 60
            self.ciclo = 90
        elif programa == "RA":
            self.tipo = "Rápido"
            self.tempo = 30
            self.ciclo = 45
        elif programa == "EX":
            self.tipo = "Enxágue"
            self.tempo = 5
            self.ciclo = 0
        elif programa == "CE":
            self.tipo = "Centrifugação"
            self.tempo = 8
            self.ciclo = 1
        else:
            self.tipo = "Nada Selecionado"
            self.tempo = -1
            self.ciclo = -1
    def pTipo(self):
        return self.tipo
    def pTempo(self):
        return self.tempo
    def pCiclo(self):
        return self.ciclo

class Arquivo(object):
    def __init__(self, programa, tempo):
        self.prog = programa
        self.tempo = tempo
        self.first_time = time.time()
        self.local = '/var/www/html/Programas/status.txt'
    def iArquivo(self, turbo):
        self.turbo = turbo
        date = datetime.now()
        if self.turbo == "True":
            self.turbo = "Sim"
        else:
            self.turbo = "Não"
        arq = open(self.local, 'w')
        texto = []
        texto.append('===========================================================')
        texto.append('\n')
        texto.append('Inicializado Máquina...')
        texto.append('\n')
        texto.append('Programa Usado: ')
        texto.append(self.prog)
        texto.append('\n')
        texto.append('Turbo Lavagem: ');
        texto.append(self.turbo);
        texto.append('\n');
        texto.append('Tempo de Batimento da Roupa: ')
        texto.append(str(self.tempo))
        texto.append(' minutos!')
        texto.append('\n')
        texto.append('Data: ')
        texto.append(date.today().strftime("%d/%m/%Y"))
        texto.append('\n')
        texto.append('Hora de Inicio: ')
        texto.append(date.today().strftime("%H:%M:%S"))
        texto.append('\n')
        texto.append('===========================================================')
        arq.writelines(texto)
        arq.close()
    def gMensagem(self, mensagem):
        date = datetime.now()
        arq = open(self.local, 'r')
        texto = arq.readlines()
        texto.append('\n')
        texto.append(date.today().strftime("%H:%M:%S: "))
        texto.append(mensagem)
        arq = open(self.local, 'w')
        arq.writelines(texto)
        arq.close()
    def fArquivo(self):
        date = datetime.now()
        second_time = time.time()
        diferenca_tempo = second_time - self.first_time
        arq = open(self.local, 'r')
        texto = arq.readlines()
        texto.append('\n')
        texto.append('===========================================================')
        texto.append('\n')
        texto.append('Hora de Finalização: ')
        texto.append(date.today().strftime("%H:%M:%S"))
        texto.append('\n')
        texto.append('Tempo decorrido: ')
        texto.append(str(int(diferenca_tempo/60)))
        texto.append(' Minutos.')
        texto.append('\n')
        texto.append('===========================================================')
        arq = open(self.local, 'w')
        arq.writelines(texto)
        arq.close()
    def dArquivo(self):
        date = datetime.now()
        shutil.move(self.local, "/var/www/html/Historico/"+date.today().strftime("%d%m%Y%H%M%S")+".txt")

class Funcoes(object):
    def fVerNivelAgua(self):
        if GPIO.input(15) == GPIO.HIGH:
            #Maquina Vazia
            return False
        else:
            #Maquina Cheia
            return True
    def fEncher(self): ### Usa 1 Rele
        while GPIO.input(15) == GPIO.HIGH: 
            GPIO.output(40,GPIO.LOW)
            time.sleep(1)
        GPIO.output(40,GPIO.HIGH)
    def fBater(self, turbo): ### Usa 2 Reles
        self.turbo = turbo
        if self.turbo == "True":
            tr = 5
            tp = 10
        else:
            tr = 3
            tp = 17
        GPIO.output(38,GPIO.LOW)
        time.sleep(tr)
        GPIO.output(38,GPIO.HIGH)
        time.sleep(tp)
        GPIO.output(37,GPIO.LOW)
        time.sleep(tr)
        GPIO.output(37,GPIO.HIGH)
        time.sleep(tp)     
    def fEnxaguar(self): ### Usa 1 Rele
        GPIO.output(36,GPIO.LOW)
        time.sleep(240)
        GPIO.output(36,GPIO.HIGH)
    def fAmaciante(self):### Usa 2 Reles
        while GPIO.input(15) == GPIO.HIGH:
            GPIO.output(40,GPIO.LOW)
            GPIO.output(35,GPIO.LOW)
            time.sleep(1)
        GPIO.output(40,GPIO.HIGH)
        GPIO.output(35,GPIO.HIGH)       
    def fCentrifugar(self): ### Usa 2 Rele
            GPIO.output(36,GPIO.LOW)
            time.sleep(90)
            GPIO.output(38,GPIO.LOW)
            time.sleep(20)
            for i in range (0, 14):
                GPIO.output(38,GPIO.LOW)
                time.sleep(15)
                GPIO.output(38,GPIO.HIGH)
                time.sleep(5)
            GPIO.output(38,GPIO.HIGH)
            time.sleep(120)
            GPIO.output(36,GPIO.HIGH)
            time.sleep(120)

class Batimento(object):
    def __init__(self, programa, turbo):    
        self.programa = programa
        self.turbo = turbo
        self.programas = Programas(self.programa)
        self.ini_gpio = Ini_GPIO()
        self.funcoes = Funcoes()
        self.arquivo = Arquivo(self.programas.pTipo(), self.programas.pCiclo())
        self.ini_gpio.outGpio()
        self.ini_gpio.inGpio()
        if self.programas.pTipo() == "Nada Selecionado":
            exit()
        ##Programa Normal
        self.arquivo.iArquivo(self.turbo)      
    def bAgitar(self):
        self.arquivo.gMensagem("A maquina esta iniciando!")
        if self.funcoes.fVerNivelAgua() == False:
            self.arquivo.gMensagem("A maquina esta sem àgua!")
            self.arquivo.gMensagem("A maquina esta enchendo de àgua!")
            self.funcoes.fEncher()
        else:
            self.arquivo.gMensagem("A maquina já esta cheia de àgua!")
        molho = 24
        self.arquivo.gMensagem("A maquina esta batendo a roupa!")
        for a in range(0, self.programas.pCiclo()):
            self.funcoes.fBater(self.turbo)
            if GPIO.input(15) == GPIO.HIGH:
                self.arquivo.gMensagem("Nivel de àgua alterado!")
                self.arquivo.gMensagem("A maquina esta enchendo de àgua!")
                self.funcoes.fEncher()
                self.arquivo.gMensagem("A maquina começou a bater a roupa novamente!")
            if a == molho:
                self.arquivo.gMensagem("A maquina está de molho!")
                time.sleep(300)
                molho = molho + 24
                self.arquivo.gMensagem("A maquina terminou o molho!")
                self.arquivo.gMensagem("A maquina começou a bater a roupa novamente!")
        self.arquivo.gMensagem("A maquina terminou de bater a bater a roupa!")
        self.funcoes.fEnxaguar()
        self.bCentrifugacao()
        self.bEnxague()
    def bEnxague(self):
        if self.funcoes.fVerNivelAgua() == False:
            self.arquivo.gMensagem("A maquina esta enchendo de àgua com amaciante!")
            self.funcoes.fAmaciante()
            self.arquivo.gMensagem("A maquina esta cheia de àgua com amaciante!")
        else:
            self.arquivo.gMensagem("A maquina esta cheia de àgua com amaciante!")        
        self.arquivo.gMensagem("A maquina começou a bater a roupa!")
        for a in range(0,20):
            self.funcoes.fBater(self.turbo)
            if self.funcoes.fVerNivelAgua() == False:
                self.arquivo.gMensagem("Nivel de àgua alterado!")
                self.arquivo.gMensagem("A maquina esta enchendo de àgua!")
                self.funcoes.fAmaciante()
                self.arquivo.gMensagem("A maquina começou a bater a roupa novamente!")
        self.arquivo.gMensagem("A maquina terminou de bater a bater a roupa!")
        self.arquivo.gMensagem("A maquina iniciou o processo de enxágue!")
        self.funcoes.fEnxaguar()
        self.arquivo.gMensagem("A maquina terminou o processo de enxágue!")
        self.bCentrifugacao()
    def bCentrifugacao(self):
        self.arquivo.gMensagem("A maquina iniciará a centrifugação!")
        if self.funcoes.fVerNivelAgua() == True:
            self.arquivo.gMensagem("A maquina ainda esta com água!")
            self.arquivo.gMensagem("A maquina ainda enxaguando novamente!")
            self.funcoes.fEnxaguar()
            if self.funcoes.fVerNivelAgua() == True:
                self.arquivo.gMensagem("Problemas na eletrobomba, saindo do programa!")
        else:
            self.funcoes.fCentrifugar()
            self.arquivo.gMensagem("A maquina terminou a centrifugação!")          
    def bFimArquivo(self):
        self.arquivo.fArquivo()
        time.sleep(60)
        self.arquivo.dArquivo()
        self.ini_gpio.clearGpio()
        exit()
###################################

batimento = Batimento(sys.argv[1], sys.argv[2])
if sys.argv[1] == "EX":
    batimento.bEnxague()
elif sys.argv[1] == "CE":
    batimento.bCentrifugacao()
else:
    batimento.bAgitar()
batimento.bFimArquivo()
