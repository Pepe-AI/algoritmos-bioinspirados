import numpy as np
import random
import pandas as pd

#sintaxis: elemento: [peso,valor]
X = {
    1: [5, 10],
    2: [5, 12],
    3: [7, 17],
    4: [10, 22],
    5: [15, 25],
    6: [18, 30]}

WEIGHT_LIMIT = 40

SELECT_NUMBER=4

FINISHED_LIMIT = 5

MUTATION_PROBA=0.1

PROB_CRUZA=0.8

max_last = 0
diff_last = 10000

def init():
    generate_chromosome=np.random.randint(0,2,[10,6])
    return generate_chromosome


def is_finished(fitnesses):
    global max_last
    global diff_last
    max_current = 0
    for v in fitnesses:
        
        if v[1] > max_current:
            max_current = v[1]
            #print('max_current: ', max_current) # Obtiene el valor máximo actual
            diff = max_current-max_last # Diferencia de valor, es decir, el tamaño del cambio en la aptitud
            # Aquí se juzga que si la cantidad de cambio de dos generaciones consecutivas es menor que 5, detenga la iteración
    if diff < FINISHED_LIMIT and diff_last < FINISHED_LIMIT: 
        return True
    else:
        diff_last = diff
        max_last = max_current
        return False

def fitness(chromosome_states):
    fitnesses = []
    for chromosome_state in chromosome_states: # Atraviesa todos los cromosomas
        value_sum = 0 # Peso del artículo
        weight_sum = 0 # Valor del artículo

        for i, v in enumerate(chromosome_state): 
            #print("i:",i,"v:",v)
            if int(v) == 1:
                weight_sum += X[i + 1][0] 
                value_sum += X[i + 1][1]
        fitnesses.append([value_sum, weight_sum])
    return fitnesses

def penalty(chromosome_init, fitnesses):
    index = len(fitnesses)-1
    while index >= 0:
        index -= 1
        if fitnesses[index][1] > WEIGHT_LIMIT:
            chromosome_init=np.delete(chromosome_init,index,axis=0) # Cromosomas emergentes que no cumplen con las condiciones
            fitnesses.remove(fitnesses[index])
            #print("------antes--------",chromosome_init,"/////",fitnesses)
    return fitnesses, chromosome_init
    
def odds(fitnesses):
    index=len(fitnesses) 
    fitnesses_add=0
    fitnesses_proba=[]
    fitnesses_prob_acum=[]
    
    for i in range(index):
        fitnesses_add+=fitnesses[i][0]
                
    for i in range(index):
        fitnesses_proba.append((fitnesses[i][0])/fitnesses_add)
    #print(fitnesses_proba[0])
    fitnesses_prob_acum.append(fitnesses_proba[0])
    for i in range(1,index): 
        fitnesses_prob_acum.append(fitnesses_prob_acum[i-1]+fitnesses_proba[i])
    
    return fitnesses_proba,fitnesses_prob_acum

def crossover(fitnesses_prob_acum,chromosome_init):
   random_padre1=random.random()  
   random_padre2=random.random()  
   random_cruza=random.random()
   
   index=len(fitnesses_prob_acum)
   
   for i in range(index):
       if random_padre1<fitnesses_prob_acum[i]:    
           #print(fitnesses_prob_acum[i])
           flag=fitnesses_prob_acum[i]
           padre1=chromosome_init[i]
           #print("----",i)
           break
       
   index2=len(fitnesses_prob_acum)
   for i in range(index2):
       if random_padre2<fitnesses_prob_acum[i] and flag!=fitnesses_prob_acum[i]: 
           #print(fitnesses_prob_acum[i])#and padre1 != fitnesses_prob_acum[i]:
           padre2=chromosome_init[i]
           #print("-----",i)
          # print("entre")
           break
       else:
          padre2=padre1 
   #print(padre2)    
   #if padre2==0:
       
   
   more_apto=[]
   more_apto.append(padre1)
   more_apto.append(padre2)
   
   if random_cruza<PROB_CRUZA:
     half = len(padre1)//2
     A=padre1[:half]
     B=padre1[half:]
     A_1=padre2[:half]
     B_1=padre2[half:]
     cruza_1=np.append(A,B_1)
     cruza_2=np.append(B,A_1)
   else:
       cruza_1=padre1
       cruza_2=padre2

   for i in range(len(cruza_1)):
        random_mut=random.random()
        if random_mut<MUTATION_PROBA:
            if cruza_1[i]==1:
                cruza_1[i]=0
            else:
                cruza_1[i]=1
                
        
   for i in range(len(cruza_2)):
        random_mut=random.random()
        if random_mut<MUTATION_PROBA:
            if cruza_2[i]==1:
                cruza_2[i]=0
            else:
                cruza_2[i]=1
                
    
   more_apto.append(cruza_1)
   more_apto.append(cruza_2)   
   
   more_apto1=np.array(more_apto)
   generation_fitnesses=fitness(more_apto1)
   print(more_apto1,generation_fitnesses)  
     
   #generation_newF,generation_new=penalty(more_apto1,generation_fitnesses)
   #print(generation_newF)
   #two_better=[[],[]]
   #array = np.zeros(shape=(2,6))
   two_better = np.empty((2, 6), int)
   two_better1= np.empty(shape=1)
   two_better2= np.empty(shape=1)
   
   print("aqui",len(more_apto1),len(generation_fitnesses))
   
   flag1=0
   for i in range(0,len(more_apto1)):
      #print("generation_newF",generation_newF[i][0],">","flag1",flag1)
      if generation_fitnesses[i][0]>=flag1: #actualizacion de la flag
           flag1=generation_fitnesses[i][0]
           #print("----------",generation_new[i])
           #two_better[0]=generation_new[i]
           two_better1= more_apto1[i]
           #np.concatenate(array,generation_new[i])
           #array[0]= generation_new[i]
   
   flag2=0
   for j in range(0,len(more_apto1)):       
         #print("generation_newF",generation_newF[j][0],">","flag2",flag2,"/////",flag1)
         if generation_fitnesses[j][0]>=flag2 and flag1!=generation_fitnesses[j][0]:
           flag2=generation_fitnesses[j][0]
           #print("----------",generation_new[i])
           two_better2=more_apto1[j] 
           #two_better= np.append(two_better, np.array([generation_new[i]]), axis=0)
   if flag2==0:
     two_better2=two_better1   
   
           
      
   #Two_Better=np.array(two_better) 
   #print(generation_new)  
   #print(generation_newF)    
   #print("numpy:",two_better1,two_better2)
   
   two_better=np.append(two_better,np.array([two_better1,two_better2]) , axis=0)
   
 
   return two_better   
  


if __name__ == '__main__':
    chromosome_init=init()
    print("Poblacion inicial: \n",chromosome_init)
    print("fitness de la poblacion inicial",fitness(chromosome_init))
    print("================================================")

    next_generation = np.empty((0, 6), int)
    n=50
    while n>0:
        n-=1
        fitnesses = fitness(chromosome_init)
        if is_finished(fitnesses):
            break                 
        fitnesses, chromosome_init = penalty(chromosome_init, fitnesses)
        fitnesses_proba,fitnesses_prob_acum=odds(fitnesses)
        
        
        for i in range(5):
            Two_better=crossover(fitnesses_prob_acum, chromosome_init) 
            next_generation=np.append(next_generation, np.array([Two_better[0]]), axis=0)
            next_generation=np.append(next_generation, np.array([Two_better[1]]), axis=0)
            
        for i in range(len(chromosome_init)):
            chromosome_init[i]=next_generation[i]
        next_generation = np.empty((0, 6), int)
        
    max_backpack=fitness(chromosome_init)
    fitnesses_pack, chromosome_init = penalty(chromosome_init, max_backpack)
    print("la mejor generacion",chromosome_init)
    max_value=1
    print("fitness de la mejor generacion",fitnesses_pack)