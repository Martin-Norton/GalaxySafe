#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
import pygame
from pygame.locals import *
import random

pygame.init()
pygame.font.init() 
pygame.mixer.music.load("paseNivel.wav") 
pygame.display.set_caption("OFIRCA 2023 - Ronda 2 - Inicio")
pantalla= pygame.display.set_mode((1152,648))
tipografia = pygame.font.SysFont('Arial', 18)
tipografiaGrande=pygame.font.SysFont('Arial', 24)
barraTimerWidth = 200  # Width de la barra timer
barraTimerHeight = 20  # Height de la barra timer
barraTimerColor = (255, 0, 0)  # Color de la barra timer
buffer = pygame.Surface((1152, 648))

global ticksAlComenzar
global cantidadDeMovimientosRestantes
global cantidadDeMovimientosActual
global zonaDeTransporte
global avatarRect
global nivelCompletado
global info_jugador_ingresada

ticksAlComenzar=pygame.time.get_ticks()
personajeActual='UAIBOT'
tiempoParaSolucionarElNivel= 55
#inicilizo un objeto clock
clock = pygame.time.Clock()
cantidadDeMovimientosActual=0
cantidadDeMovimientosRestantes=10
colorVerde,colorAzul,colorBlanco,colorNegro, colorNaranja, colorBordeaux= (11,102,35),(0,0,255),(255,255,255),(0,0,0),(239,27,126),(102,41,53)
cantidadDeCasillasPorLado=8 #Debe ser número par ya que la zona es un cuadrado
cantPixelesPorLadoCasilla=64
salirJuego = False
lstAreaProtegida=[]

imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOT.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
avatarRect=imgAvatar.get_rect()   
imgPared=pygame.transform.scale(pygame.image.load("pared.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  

imgAreaProtegida=pygame.transform.scale(pygame.image.load("areaprotegida.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
listaVirus  = ["virus1.png","virus2.png","virus3.png","virus4.png","virus5.png","virus6.png"]
imgVirus=pygame.transform.scale(pygame.image.load(str(random.choice(listaVirus))), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
imgVirusQueSeMueve=pygame.transform.scale(pygame.image.load(str(random.choice(listaVirus))), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))

virusQueSeMueveRect = imgVirusQueSeMueve.get_rect()
virusQueSeMueveRect.left =cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
virusQueSeMueveRect.top = cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado - 2)

imgVirusSinusoidal = pygame.transform.scale(pygame.image.load("virus1.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))
virusSinusoidalRect = imgVirusSinusoidal.get_rect()
velocidad_x = 2
velocidad_y = 1
x = 3 * cantPixelesPorLadoCasilla  # Coordenada X
y = 2 * cantPixelesPorLadoCasilla  # Coordenada Y

#se ingresa por primera vez la informacion del jugador  
nombreJugador = input("Ingrese su nombre: ")
cantidadDeMovimientosDeterminada=int(input('ingrese la cantidad de movimientos con los que va a jugar'))
cantidadDeMovimientosRestantes=cantidadDeMovimientosDeterminada

#SE SETEA EL CURSOR EN UNA MIRA
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

#region tablero
def crearZonaDeTransporte():

    zonaDeTransporte = [[0 for x in range(cantidadDeCasillasPorLado+1)] for y in range(cantidadDeCasillasPorLado+1)] 
    
    zonaDeTransporte[1][1] = 'pared'
    zonaDeTransporte[2][1] = 'pared'
    zonaDeTransporte[3][1] = 'pared'
    zonaDeTransporte[4][1] = 'pared'
    
    zonaDeTransporte[1][2] = 'pared'
    zonaDeTransporte[4][2] = 'pared'

    zonaDeTransporte[1][3] = 'pared'
    zonaDeTransporte[4][3] = 'pared'
    zonaDeTransporte[5][3] = 'pared'
    zonaDeTransporte[6][3] = 'pared'

    zonaDeTransporte[1][4] = 'pared'
    zonaDeTransporte[6][4] = 'pared'
   
    zonaDeTransporte[6][5] = 'pared'
    zonaDeTransporte[1][5] = 'pared'


    zonaDeTransporte[1][6] = 'pared'
    zonaDeTransporte[4][6] = 'pared'
    zonaDeTransporte[5][6] = 'pared'
    zonaDeTransporte[6][6] = 'pared'

    zonaDeTransporte[1][7] = 'pared'
    zonaDeTransporte[2][7] = 'pared'
    zonaDeTransporte[3][7] = 'pared'
    zonaDeTransporte[4][7] = 'pared'

    zonaDeTransporte[5][6] = 'pared'
    
    zonaDeTransporte[5][4] = 'jugador'
   
       
    zonaDeTransporte[4][5] = 'virus'    
    zonaDeTransporte[2][5] = 'virus'    


    lstAreaProtegida.append((3,2))
    lstAreaProtegida.append((2,6))
    
    return zonaDeTransporte

zonaDeTransporte=crearZonaDeTransporte()

def hayAreaProtegidaEn(x,y):
    punto=(x,y)
    return lstAreaProtegida.__contains__(punto)

def posicionarElemento(elemento,x,y): 
    global zonaDeTransporte
    global avatarRect
    zonaDeTransporte[x][y]=elemento
    if (elemento=='jugador'):
        r=pygame.Rect(cantPixelesPorLadoCasilla * (x),cantPixelesPorLadoCasilla * (y),cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla)
        avatarRect=r

def borrarElemento(x,y):
    global zonaDeTransporte
    zonaDeTransporte[x][y]=0

def dibujarZonaDeTransporte():     
    global zonaDeTransporte
    global avatarRect
    cnt = 0
    for i in range(1,cantidadDeCasillasPorLado+1):
        for j in range(1,cantidadDeCasillasPorLado+1):
            if cnt % 2 == 0:
                pygame.draw.rect(pantalla, colorVerde,[cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])
            else:
                pygame.draw.rect(pantalla, colorVerde, [cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i,cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla])        

            if (hayAreaProtegidaEn(j,i)==True):
                pantalla.blit(imgAreaProtegida, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i)) 
            if (zonaDeTransporte[j][i]=='jugador'):
                pantalla.blit(imgAvatar, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))     
                avatarRect=pygame.Rect(cantPixelesPorLadoCasilla * (j),cantPixelesPorLadoCasilla * (i),cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla)
            if (zonaDeTransporte[j][i]=='pared'):          
               pantalla.blit(imgPared, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))
            if (zonaDeTransporte[j][i]=='virus'):
               pantalla.blit(imgVirus, (cantPixelesPorLadoCasilla*j,cantPixelesPorLadoCasilla*i))
            cnt +=1
        cnt-=1

    pygame.draw.rect(pantalla,colorBlanco,[cantPixelesPorLadoCasilla,cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla,cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla],1)       
    pygame.display.update()

#endregion

def dibujarFondo():
    fondo = pygame.image.load("fondo.png")
    pantalla.blit(fondo, (0, 0))
    
def dibujarReglas():

    textoReglas = tipografia.render('Mueve a tu avatar con las flechas para que lleve los virus a las zonas protegidas.', False, colorBlanco)
 
    ancho=650
    alto=25
    x=64
    y=3
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    pantalla.blit(textoReglas,(x+5,y,ancho,alto))
    pygame.display.update()

def actualizarContadorDeMovimientos(num):
    global cantidadDeMovimientosActual
    global cantidadDeMovimientosRestantes
    cantidadDeMovimientosActual=cantidadDeMovimientosActual+num
    cantidadDeMovimientosRestantes=cantidadDeMovimientosRestantes-1
    
    if cantidadDeMovimientosRestantes<0:
        cantidadDeMovimientosRestantes=0
    
    ancho=350
    alto=30
    x=75+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    y=cantPixelesPorLadoCasilla*5
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    textoPasos = tipografiaGrande.render('Cantidad de movimientos: ' + str(cantidadDeMovimientosActual), False, colorBlanco)
    pantalla.blit(textoPasos,(x+5,y,ancho,alto))    
   
    y=cantPixelesPorLadoCasilla*6 
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho + 32,alto))
    textoMovimientosRestantes = tipografiaGrande.render('Cantidad de movimientos restantes: ' + str(cantidadDeMovimientosRestantes), False, colorBlanco)
    pantalla.blit(textoMovimientosRestantes,(x+5,y,ancho,alto))

    pygame.display.update()

def dibujarCartelIndicadorRonda():
    textoFelicitacion = tipografiaGrande.render('Ronda 2', False, colorBlanco)
    ancho=160
    alto=50
    x=350+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    y=5
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    pantalla.blit(textoFelicitacion,(x+5,y,ancho,alto))
    pygame.display.update()

#dibuja un cartel muy parecido al de ronda donde muestra el nombre del jugador en curso
def dibujarCartelNombreJugador():
    textoFelicitacion = tipografiaGrande.render('Jugador: {}'.format(nombreJugador), False, colorBlanco)
    ancho=160
    alto=50
    x=350+(cantidadDeCasillasPorLado*cantPixelesPorLadoCasilla)
    y=55
    pygame.draw.rect(pantalla,colorBordeaux,(x,y,ancho,alto))
    pantalla.blit(textoFelicitacion,(x+5,y,ancho,alto))
    pygame.display.update()  

def dibujarTodo():
    dibujarFondo()
    dibujarZonaDeTransporte()
    dibujarCartelIndicadorRonda()
    dibujarCartelNombreJugador()
    dibujarReglas()
      
    pygame.display.update()

dibujarTodo()

def estaSolucionado():
    global nivelCompletado
    global zonaDeTransporte

    cantVirusSobreAreasProtegidas=0

    for punto in lstAreaProtegida:
        x=punto[0]
        y=punto[1]
        if zonaDeTransporte[x][y]=='virus':
            cantVirusSobreAreasProtegidas=cantVirusSobreAreasProtegidas+1       

    if (cantVirusSobreAreasProtegidas==len(lstAreaProtegida)):
        nivelCompletado=True
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("paseNivel.wav"))
    else:
        nivelCompletado=False
    dibujarCartelIndicadorRonda()
    dibujarReglas()
    verificarSiTerminoElJuego()
     
#region Movimientos jugador
def irALaDerechaConUAIBOT():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j+1][i]==0):
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeMovimientos(1)
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break                
                if(zonaDeTransporte[j+1][i]=='virus') and not ((zonaDeTransporte[j+2][i]=='pared') or (zonaDeTransporte[j+2][i]=='virus')):                  
                    posicionarElemento('virus',j+2,i)
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeMovimientos(1)
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break

def irArribaConUAIBOT():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j][i-1]==0):
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeMovimientos(1)                  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                if(zonaDeTransporte[j][i-1]=='virus') and not ((zonaDeTransporte[j][i-2]=='pared') or (zonaDeTransporte[j][i-2]=='virus')):
                    posicionarElemento('virus',j,i-2)
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeMovimientos(1)                 
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break

def irAbajoConUAIBOT():
    global zonaDeTransporte
    for j in range(1,cantidadDeCasillasPorLado):
        for i in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j][i+1]==0):
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeMovimientos(1)         
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                if(zonaDeTransporte[j][i+1]=='virus') and not ((zonaDeTransporte[j][i+2]=='pared') or (zonaDeTransporte[j][i+2]=='virus')):
                    posicionarElemento('virus',j,i+2)
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeMovimientos(1)       
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break

def irALaIzquierdaConUAIBOT():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j-1][i]==0):
                    posicionarElemento('jugador',j-1,i)              
                    actualizarContadorDeMovimientos(1)
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                if(zonaDeTransporte[j-1][i]=='virus') and not ((zonaDeTransporte[j-2][i]=='pared') or (zonaDeTransporte[j-2][i]=='virus') ):
                    posicionarElemento('virus',j-2,i)
                    posicionarElemento('jugador',j-1,i)
                    actualizarContadorDeMovimientos(1)  
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break

def irALaDerechaConUAIBOTA():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if(zonaDeTransporte[j-1][i]=='virus') and (zonaDeTransporte[j+1][i]==0):                                     
                    posicionarElemento('jugador',j+1,i)
                    posicionarElemento('virus',j,i)
                    actualizarContadorDeMovimientos(1) 
                    borrarElemento(j-1,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                elif (zonaDeTransporte[j+1][i]==0):
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeMovimientos(1)        
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break

def irArribaConUAIBOTA():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if(zonaDeTransporte[j][i+1]=='virus') and (zonaDeTransporte[j][i-1]==0):                                     
                    posicionarElemento('jugador',j,i-1)
                    posicionarElemento('virus',j,i)
                    actualizarContadorDeMovimientos(1)
                    borrarElemento(j,i+1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                elif (zonaDeTransporte[j][i-1]==0):
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeMovimientos(1)
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break

def irAbajoConUAIBOTA():
    global zonaDeTransporte
    for j in range(1,cantidadDeCasillasPorLado):
        for i in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if(zonaDeTransporte[j][i-1]=='virus') and (zonaDeTransporte[j][i+1]==0):                                     
                    posicionarElemento('jugador',j,i+1)
                    posicionarElemento('virus',j,i)
                    actualizarContadorDeMovimientos(1)          
                    borrarElemento(j,i-1)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                elif (zonaDeTransporte[j][i+1]==0):
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeMovimientos(1)           
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break

def irALaIzquierdaConUAIBOTA():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if(zonaDeTransporte[j+1][i]=='virus') and (zonaDeTransporte[j-1][i]==0):                                     
                    posicionarElemento('jugador',j-1,i)
                    posicionarElemento('virus',j,i)
                    actualizarContadorDeMovimientos(1)  
                    borrarElemento(j+1,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                elif (zonaDeTransporte[j-1][i]==0):
                    posicionarElemento('jugador',j-1,i)
                    actualizarContadorDeMovimientos(1)
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break

def irALaDerechaConUAIBOTIN():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j+1][i]==0):
                    posicionarElemento('jugador',j+1,i)
                    actualizarContadorDeMovimientos(1)
              
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                elif j+2<(len(zonaDeTransporte[j])):
                    if(zonaDeTransporte[j+2][i]==0) and (zonaDeTransporte[j+1][i]=='virus'):
                        posicionarElemento('jugador',j+2,i)
                        actualizarContadorDeMovimientos(1)               
                        borrarElemento(j,i)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                        break 

def irArribaConUAIBOTIN():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j][i-1]==0):
                    posicionarElemento('jugador',j,i-1)
                    actualizarContadorDeMovimientos(1)
         
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                elif i-2<(len(zonaDeTransporte[i])):
                     if((zonaDeTransporte[j][i-2]==0) and (zonaDeTransporte[j][i-1]=='virus')):
                        posicionarElemento('jugador',j,i-2)
                        actualizarContadorDeMovimientos(1)      
                        borrarElemento(j,i)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                        break 

def irAbajoConUAIBOTIN():
    global zonaDeTransporte
    for j in range(1,cantidadDeCasillasPorLado):
        for i in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):              
                if (zonaDeTransporte[j][i+1]==0):
                    posicionarElemento('jugador',j,i+1)
                    actualizarContadorDeMovimientos(1)      
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                elif i+2<(len(zonaDeTransporte[i])):
                    if((zonaDeTransporte[j][i+2]==0) and (zonaDeTransporte[j][i+1]=='virus')):
                        posicionarElemento('jugador',j,i+2)
                        actualizarContadorDeMovimientos(1)                 
                        borrarElemento(j,i)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                        break 

def irALaIzquierdaConUAIBOTIN():
    global zonaDeTransporte
    for i in range(1,cantidadDeCasillasPorLado):
        for j in range(1,cantidadDeCasillasPorLado):
            if (zonaDeTransporte[j][i]=='jugador'):
                if (zonaDeTransporte[j-1][i]==0):
                    posicionarElemento('jugador',j-1,i)
                    actualizarContadorDeMovimientos(1)           
                    borrarElemento(j,i)
                    pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                    break
                elif j-2<(len(zonaDeTransporte[j])):
                    if(zonaDeTransporte[j-2][i]==0 and zonaDeTransporte[j-1][i]=='virus'):
                        posicionarElemento('jugador',j-2,i)
                        actualizarContadorDeMovimientos(1)
              
                        borrarElemento(j,i)
                        pygame.mixer.Channel(1).play(pygame.mixer.Sound("mover.wav"))
                        break 
#endregion

def guardar_en_ranking(nombre_jugador, cantidad_movimientos):
    try:
        with open('ranking.txt', 'a') as archivo:
            archivo.write(f'{nombre_jugador}: {cantidad_movimientos}\n')
    except IOError as e:
        print('Error al guardar en el archivo:', str(e))

def barraDeTiempo():
    global estaSinMovimientos
    tiempo_transcurrido = (pygame.time.get_ticks() - ticksAlComenzar) // 1000
    tiempo_restante = tiempoParaSolucionarElNivel - tiempo_transcurrido
    if tiempo_restante <= 0:
        resetearJuego()
        print('se acabo el tiempo!')
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("gameOver.wav"))
    # Calcula el ancho de la barra restante en función del tiempo restante
    remaining_percentage = (tiempo_restante / tiempoParaSolucionarElNivel)
    remaining_width = int(remaining_percentage * barraTimerWidth)
    remaining_rect = pygame.Rect(370, 100, remaining_width, barraTimerHeight)
    pygame.draw.rect(pantalla, barraTimerColor, remaining_rect)  # Dibuja la barra restante

    # Muestra el porcentaje de tiempo restante en la pantalla
    tipografia = pygame.font.Font(None, 36)
    textoPorcentaje = tipografia.render(f"{remaining_percentage * 100:.1f}%", True, colorNegro)
    porcentajeRect = textoPorcentaje.get_rect()
    porcentajeRect.left = 480
    porcentajeRect.top = 100
    pantalla.blit(textoPorcentaje, porcentajeRect)
    pygame.display.update()
    
def resetearJuego():
    global zonaDeTransporte, cantidadDeMovimientosRestantes, cantidadDeMovimientosActual, ticksAlComenzar
    virusQueSeMueveRect.left =cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
    virusQueSeMueveRect.top = cantPixelesPorLadoCasilla * (cantidadDeCasillasPorLado - 2)
           
    zonaDeTransporte=crearZonaDeTransporte()
    cantidadDeMovimientosActual=0
    cantidadDeMovimientosRestantes=cantidadDeMovimientosDeterminada

    ticksAlComenzar=pygame.time.get_ticks()
    tiempo_transcurrido = (pygame.time.get_ticks() - ticksAlComenzar) // 1000
    tiempo_restante = tiempoParaSolucionarElNivel - tiempo_transcurrido
    guardar_en_ranking(nombreJugador, cantidadDeMovimientosActual)
    dibujarTodo()

def verificarSiTerminoElJuego():
    global nivelCompletado
    if (nivelCompletado==True):
        guardar_en_ranking(nombreJugador, cantidadDeMovimientosActual)
        resetearJuego()

def estaSinMovimientos():
    global cantidadDeMovimientosRestantes
    if (nivelCompletado==False) and (int(cantidadDeMovimientosRestantes)<=0):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("gameOver.wav"))
        resetearJuego()

#verifica el disparo
def verificarDisparo():
    mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
    if mouseRect.colliderect(virusQueSeMueveRect):
        virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
def cambiarNombreJugador():
    nombreJugador = input("Ingrese su nombre: ")
    cantidadDeMovimientosDeterminada=int(input('ingrese la cantidad de movimientos con los que va a jugar '))
    cantidadDeMovimientosRestantes=cantidadDeMovimientosDeterminada


while not salirJuego:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            salirJuego = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            barraDeTiempo()
            verificarDisparo()
        if event.type == pygame.KEYDOWN:
            barraDeTiempo()
            if event.key == pygame.K_RIGHT:
                match personajeActual:
                    case "UAIBOT":    
                        irALaDerechaConUAIBOT()
                    case "UAIBOTA":
                         irALaDerechaConUAIBOTA()
                    case "UAIBOTINA":
                         irALaDerechaConUAIBOTIN()   
                    case "UAIBOTINO":
                         irALaDerechaConUAIBOTIN()                          
            elif event.key == pygame.K_LEFT:
                match personajeActual:
                    case "UAIBOT":    
                        irALaIzquierdaConUAIBOT()
                    case "UAIBOTA":
                         irALaIzquierdaConUAIBOTA()  
                    case "UAIBOTINA":
                         irALaIzquierdaConUAIBOTIN() 
                    case "UAIBOTINO":
                         irALaIzquierdaConUAIBOTIN() 
            elif event.key == pygame.K_UP:
                match personajeActual:
                    case "UAIBOT":    
                        irArribaConUAIBOT()
                    case "UAIBOTA":
                         irArribaConUAIBOTA() 
                    case "UAIBOTINA":
                         irArribaConUAIBOTIN()  
                    case "UAIBOTINO":
                         irArribaConUAIBOTIN()  
            elif event.key == pygame.K_DOWN:
                match personajeActual:
                    case "UAIBOT":    
                        irAbajoConUAIBOT()
                    case "UAIBOTA":
                         irAbajoConUAIBOTA() 
                    case "UAIBOTINA":
                         irAbajoConUAIBOTIN()  
                    case "UAIBOTINO":
                         irAbajoConUAIBOTIN()  
            elif event.key == pygame.K_r:
                resetearJuego()
            elif event.key == pygame.K_e:
                match personajeActual:
                    case "UAIBOT":          
                        imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOTA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTA"
                    case "UAIBOTA":
                        imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOTINA.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTINA"
                    case "UAIBOTINA":
                        imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOTINO.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOTINO"
                    case "UAIBOTINO":
                        imgAvatar=pygame.transform.scale(pygame.image.load("UAIBOT.png"), (cantPixelesPorLadoCasilla, cantPixelesPorLadoCasilla))  
                        personajeActual="UAIBOT"
        dibujarFondo()
        dibujarZonaDeTransporte()
        dibujarCartelIndicadorRonda()
        dibujarCartelNombreJugador()
        dibujarReglas()
            
        virusQueSeMueveRect.left = virusQueSeMueveRect.left - 1 
        pantalla.blit(imgVirusQueSeMueve, (virusQueSeMueveRect.left, virusQueSeMueveRect.top))   

        #RegionVirusSinusoidal
        # Actualiza la posición del virusSinusoidal según el patrón sinusoidal
        x += velocidad_x
        y += velocidad_y
        # Verifica si el virusSinusoidal ha alcanzado los límites del área protegida
        if x < cantPixelesPorLadoCasilla or x > 6 * cantPixelesPorLadoCasilla:
            velocidad_x *= -1  # Cambia la dirección en el eje X si se alcanzan los límites
        if y < cantPixelesPorLadoCasilla or y > 6 * cantPixelesPorLadoCasilla:
            velocidad_y *= -1  # Cambia la dirección en el eje Y si se alcanzan los límites
        # Actualiza la posición del rectángulo del virusSinusoidal
        virusSinusoidalRect.left = x
        virusSinusoidalRect.top = y
        # Dibuja el virusSinusoidal en su nueva posición
        pantalla.blit(imgVirusSinusoidal, virusSinusoidalRect)
        #resetea el juego si el virus soinusoidal toca al jugador
        if virusSinusoidalRect.colliderect(avatarRect):
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("gameOver.wav"))
            resetearJuego()
        #endregion
        
        estaSolucionado()
        estaSinMovimientos()
        pygame.display.flip
         
    
    if virusQueSeMueveRect.colliderect(avatarRect):
        pygame.mixer.Channel(1).play(pygame.mixer.Sound("gameOver.wav"))
        resetearJuego()
        
    if (virusQueSeMueveRect.left < cantPixelesPorLadoCasilla):
        virusQueSeMueveRect.left = cantPixelesPorLadoCasilla * cantidadDeCasillasPorLado
         
pygame.quit()
