
from multiprocessing import reduction
import numpy as np
import matplotlib.pyplot as plt
import random
 
#Función de aptitud
def fitness(x,y):
    x=float(x)
    y=float(y)
    function_value=x**2+y**2
    function_value=float(function_value)
    return function_value
#Creamos la clase particula
class Particle:
    def __init__(self):
        self.posX = random.uniform(-5,5)
        self.posY = random.uniform(-5,5)
        self.pbestX = self.posX
        self.pbestY = self.posY
        self.pbest = 0
        self.velocityX = random.uniform(-5,5)
        self.velocityY = random.uniform(-5,5)
#Funcion para crear nuestras particulas
def createParticles(num_particles):
    particles=[]
    for i in range(num_particles):
        particles.append(Particle())
    return particles
#Función para actualizar los datos de la particula
def update(particles,gbest,inertia,self_factor,social_factor):
    size = len(particles)
    for i in range(size):
        r1 = random.randint(0,1)
        r2 = random.randint(0,1)
        particles[i].posX = inertia * particles[i].velocityX + self_factor * r1 *(particles[i].pbest - particles[i].posX ) + social_factor * r2 *(gbest - particles[i].posX)
        particles[i].posY = inertia * particles[i].velocityY + self_factor * r1 *(particles[i].pbest - particles[i].posY ) + social_factor * r2 *(gbest - particles[i].posY)
    return particles

        
#Función para imprimir los datos de las particulas
def printData(particles):
    size = len(particles)
    for i in range(size):
        print(f"Particula {i} -->Posición: {particles[i].posX},{particles[i].posY} -->Velocidad: {particles[i].velocityX},{particles[i].velocityY} -->Pbest (x,y : Valor): {particles[i].pbestX},{particles[i].pbestY}: {particles[i].pbest}")

def main():
    gbest = 10000
    iteration = 0
    #Ingresamos los parámetros de ejecución
    #Ingresamos el número de iteraciones (para la práctica son 50)
    iterations=int(input("Ingrese el número de iteraciones: "))
    #Ingresamos el número de particulas (para la práctica son 20)
    num_particles=int(input("Ingrese el número de particulas: "))
    #Ingresamos la inercia (para la práctica es 0.8)
    inertia=float(input("Ingrese la inercia: "))
    #Ingresamos el factor propio (para la práctica es 0.7)
    self_factor=float(input("Ingrese el factor propio: "))
    #Ingresamos el factor social (para la práctica es 1)
    social_factor=float(input("Ingrese el factor social: "))
    #Creamos las particulas
    particles = createParticles(num_particles)
    size = len(particles)

    #El pbest de cada particula al inicio será la posición que tengan originalmente, pues no conocen otra, así que iniciamos con eso.
    for i in range(size):
        particles[i].pbest = fitness(particles[i].posX,particles[i].posY)
        if particles[i].pbest < gbest:
            gbest=particles[i].pbest

    while True:
        #Buscamos la mejor posición y valor de la función de cada particula
        for i in range(size):
            aux = fitness(particles[i].posX,particles[i].posY)
            if aux < particles[i].pbest:
                particles[i].pbest = aux
                particles[i].pbestX = particles[i].posX
                particles[i].pbestY = particles[i].pbestY
            if particles[i].pbest < gbest:
                gbest = particles[i].pbest

        print(iteration)
        printData(particles)
        print(f"Gbest: {gbest}")
        particles=update(particles,gbest,inertia,self_factor,social_factor)
        iteration+=1
        if iteration > iterations:
            print("FIN DEL PROGRAMA")
            break

if __name__=="__main__":
    main()