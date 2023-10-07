import pygame
import numpy as np
import time
import random

randomGame=input("Iniciar Glider con celdas aleatorias? (1=si / 0=no): ")
randomGame=int(randomGame)
#Definir la pantalla
width,height=1000,1000
screen=pygame.display.set_mode((height,width))
pygame.display.set_caption("LifeGame")
#Color de la pantalla rgb
bg=25,25,25
screen.fill(bg)
nxC,nyC=50,50
dimCW= width/nxC
dimCH= height/nyC
#Estado de las celdas. VIVAS=1 / MUERTAS=0
gameState=np.zeros((nxC,nyC))
gameState[21,21]=1
gameState[22,22]=1
gameState[22,23]=1
gameState[21,23]=1    
gameState[20,23]=1
#Ciclo for para iniciar el 30% de la maya de forma aleatoria
if randomGame==1:
    for randomState in range(0,750):
        py=random.randint(0,49)
        px=random.randint(0,49)
        gameState[py,px]=1
#Control
pauseExect=False
#Ejecucion
while True:
    newGameState=np.copy(gameState)
    #Contamos la cantidad de celdas vivas (densidad):
    liveCells = (newGameState== 1).sum()
    print("Densidad de la malla: "+str(liveCells))
    screen.fill(bg)
    time.sleep(0.2)

    #Registro de teclado
    ev=pygame.event.get()
    for event in ev:  
        if event.type==pygame.KEYDOWN:
            pauseExect=not pauseExect
        mouseClick=pygame.mouse.get_pressed()
        
        if sum(mouseClick)>0:
            posX,posY=pygame.mouse.get_pos()
            celX,celY=int(np.floor(posX/dimCW)),int(np.floor(posY/dimCH))
            newGameState[celX,celY]=1
    for y in range(0,nxC):
        for x in range(0,nyC):

            if not pauseExect:

            #VECINOS
                n_neigh=gameState[(x-1)%nxC,(y-1)%nyC]+\
                gameState[(x-1)%nxC,(y)%nyC]+\
                gameState[(x-1)%nxC,(y+1)%nyC]+\
                gameState[(x)%nxC,(y+1)%nyC]+\
                gameState[(x+1)%nxC,(y+1)%nyC]+\
                gameState[(x+1)%nxC,(y)%nyC]+\
                gameState[(x+1)%nxC,(y-1)%nyC]+\
                gameState[(x)%nxC,(y-1)%nyC]
            #REGLAS
                if gameState[x,y]==0 and n_neigh==3:
                    newGameState[x,y]=1
                elif gameState[x,y]==1 and (n_neigh<2 or n_neigh>3):
                    newGameState[x,y]=0
            #Poligonos
            poly=[((x)*dimCW,y*dimCH),
            ((x+1)*dimCW,y*dimCH),
            ((x+1)*dimCW,(y+1)*dimCH),
            ((x)*dimCW,(y+1)*dimCH) ]
            #CElDAS
            if newGameState[x,y]==0:
                pygame.draw.polygon(screen,(128,128,128),poly,1)
            else:
                pygame.draw.polygon(screen,(255,255,255),poly,0)
    #Procesado
    gameState=np.copy(newGameState)
    pygame.display.flip()
    pass