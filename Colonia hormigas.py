# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 00:13:38 2022

@author: pepeh
"""

import random as rn
import numpy as np
from numpy.random import choice as np_choice
from math import sqrt
import matplotlib.pyplot as plt



class AntColony(object):

    def __init__(self, distances, n_ants, n_best, n_iterations, decay, alpha=1, beta=1):
        
        self.distances  = distances
        self.pheromone = np.ones(self.distances.shape) / len(distances)
        #print(self.pheromone)
        self.all_inds = range(len(distances))
        #print(self.all_inds)
        self.n_ants = n_ants
        self.n_best = n_best
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self):
        distance_logs=[]
        shortest_path = None
        all_time_shortest_path = ("placeholder", np.inf)
        for i in range(self.n_iterations):
            all_paths = self.gen_all_paths()
            
            self.spread_pheronome(all_paths, self.n_best, shortest_path=shortest_path)# se esparcen las feromonas
            shortest_path = min(all_paths, key=lambda x: x[1])
            #print(shortest_path)
            #print(shortest_path)
            #print("-------------------",shortest_path[1])
            if shortest_path[1] < all_time_shortest_path[1]:#Aqui actualiza el mejor camino que lleva hasta el comento
                all_time_shortest_path = shortest_path
            distance_logs.append(all_time_shortest_path[1]) #se agrega a una lista el mejor camino hasta el momento para visualizar una grafica                    
        return all_time_shortest_path,distance_logs #regresa el mejor camino y el proceso del algoritmo

    def spread_pheronome(self, all_paths, n_best, shortest_path):
        sorted_paths = sorted(all_paths, key=lambda x: x[1]) #organiza de menor a mayor el valor
        #print(sorted_paths[:n_best])
        for path, dist in sorted_paths[:n_best]:           
            #print(path,"//////",dist)
            for move in path:
                #print("1/",self.distances[move])               
                self.pheromone[move] += 1.0 / self.distances[move]
                #print(self.pheromone[move])
                

    def gen_path_dist(self, path):
        total_dist = 0
        for ele in path:
            total_dist += self.distances[ele]
        return total_dist

    def gen_all_paths(self):
        all_paths = []
        for i in range(self.n_ants):
            path = self.gen_path(0)#0 = el nodo que va comenzar, PARA CADA HORMIGA
            all_paths.append((path, self.gen_path_dist(path))) #se guarda un camino por cada hormiga
        return all_paths

    def gen_path(self, start):
        path = []
        visited = set() # no deja agregar datos que ya existan 
        visited.add(start) # se añade el nodo(start), esto por que no se puede volver a visitiar un nodo 
        prev = start
        for i in range(len(self.distances) - 1): #for que va i hasta el tamaño tour(diagrama)
            move = self.pick_move(self.pheromone[prev], self.distances[prev], visited) #se pasan las feromonas(en ese momento, las distancias, conjunto de nosos visitados)
            path.append((prev, move)) #Ese movimiento se guarda en una tupla
            prev = move # nuestro proximo movimiento empezara donde termino el anterior
            visited.add(move) #se añaded le movimiento a los visitados 
        path.append((prev, start)) # una vez hecho todo el recorrido se conecta el final con el inicio   
        return path

    def pick_move(self, pheromone, dist, visited):
        pheromone = np.copy(pheromone) # hacemos una copia del valor de las feromonas
        pheromone[list(visited)] = 0 # se reinicia  a 0

        row = (pheromone ** self.alpha) * (( 1.0 / dist) ** self.beta) # la primera parte determina el peso de las feromonas y la segunda parte es la visibilidad de la arista

        norm_row = row / row.sum() #normalizando
        move = np_choice(self.all_inds, 1, p=norm_row)[0] #regresa cual es el movimiento mas corto con base a una probabilidad de cada mobvimiento
        #print(move)
        return move


#Static  Instance
distances = np.array([[np.inf, 2, 2, 5, 7, 4],
                       [2, np.inf, 4, 8, 2, 7],
                       [2, 4, np.inf, 1, 3, 8],
                       [5, 8, 1, np.inf, 2, 3],
                       [7, 2, 3, 2, np.inf, 5],
                       [7, 2, 3, 2, 1,np.inf]])

ant_colony = AntColony(distances, 6, 1, 6, 0.7, alpha=1, beta=1)
shortest_path,log = ant_colony.run()
print ("shortest_path: {}".format(shortest_path))
print("log: {}".format(log))
plt.plot(log)