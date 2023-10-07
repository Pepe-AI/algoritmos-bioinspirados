import numpy as np
import math
import random
import fitness


limitePob=5

pobinicial=np.random.randint(0,2,[5,4])
        
print("poblacion inicial:\n",pobinicial)
longitud=len(pobinicial)

decimal=[0,0,0,0,0]
proba_sel=[0,0,0,0,0]
proba_sel_acum=[0,0,0,0,0]
h=1
g=0
t=0
maxi=1
individuos=""
fdex=[0,0,0,0,0]
#padre1_proba=0
#padre2_proba=0
p_c=0.85
p_m=0.1
padre1=[]
padre2=[]
arr_mutacion=[]
decimal_opc=[0,0]
fitness_opc=[0,0]
nueva_gen=np.empty((5, 4), int)

while maxi<=10:
    for i in range(0,longitud):   
        for j in range(0,longitud-1):
            if pobinicial[i][j]==1:
                individuos+="1"
            else:
                individuos+="0"
       
        c=int(str(individuos), 2)    
        decimal[i]=c
        individuos=""    
    
    
    for i in range(0,longitud):
        fdex[i]=fitness.fitness(decimal[i])
        
    
    total=sum(fdex)
    
    
    for i in range(0,longitud):
        proba_sel[i]=fdex[i]/total    
    
    
    
    proba_sel_acum[0]=proba_sel[0]  
    for i in range(0,longitud-1):
        proba_sel_acum[i+1]=proba_sel_acum[i]+proba_sel[h]
        h+=1
    h=1
      
    
    while t<=2:                
        x1=random.random()
        posicion1=0
        for j in range(0,longitud):
            if proba_sel_acum[j]>x1:
                padre1=proba_sel_acum[j]
                posicion1=j
                break
        
        x2=random.random()
        posicion2=0
        for j in range(0,longitud):
            if proba_sel_acum[j] and padre1!=proba_sel_acum[j]>x2:
                padre2=proba_sel_acum[j]
                posicion2=j
                break
        
        #probabilidad de cruza
        proba_cruce=np.random.random()
        if proba_cruce<=p_c:
            print("cruce aprobado")
            corte=2
            #cruce(creacion de hijos)
            hijo=pobinicial[posicion1]
            hijo1=pobinicial[posicion2]
            for i in range(corte,longitud-1):
                k=hijo[i]
                hijo[i]=hijo1[i]
                hijo1[i]=k
               
            
            arr_mutacion= np.random.uniform(0,1,4).tolist()
            arr_mutacion1= np.random.uniform(0,1,4).tolist()
            #mutacion  
            for i in range(0,3):
                if arr_mutacion[i]<p_m:
                    if hijo[i]==1:
                        hijo[i]=0
                    else:
                        hijo[i]=1
            for i in range(0,3):
                if arr_mutacion1[i]<p_m:
                    if hijo1[i]==1:
                        hijo1[i]=0
                    else:
                        hijo1[i]=1
            
            
            len_hijo=len(hijo)
            decimal_opc[0]=fitness.bi_dec(hijo,len_hijo)
            decimal_opc[1]=fitness.bi_dec(hijo1,len_hijo)
            #decimal_hijos=[decimal_opc[],decimal_opc1]
              
             
            
            for i in range(0,2):
                fitness_opc[i]=fitness.fitness(decimal_opc[i])
                
            
            if t==2:
                if fdex[posicion1]<=fdex[posicion2]:
                    mejor_padre=fdex[posicion2]
                    mejor_padre_bi=pobinicial[posicion2]            
                else:
                    mejor_padre=fdex[posicion1]
                    mejor_padre_bi=pobinicial[posicion1]
                if fitness_opc[0]<=fitness_opc[1]:           
                    mejor_hijo=fitness_opc[1]
                    mejor_hijo_bi=hijo1
                else:
                    mejor_hijo=fitness_opc[0]
                    mejor_hijo_bi=hijo
                if mejor_padre<=mejor_hijo:
                    nueva_gen[4]=mejor_hijo_bi
                else:
                    nueva_gen[4]=mejor_padre_bi
                
                break
            
            if fdex[posicion1]<=fdex[posicion2]:
                
                nueva_gen[g]=pobinicial[posicion2]
            else:
                nueva_gen[g]=pobinicial[posicion1]
                
                
            if fitness_opc[0]<=fitness_opc[1]:
                
                nueva_gen[g+1]=hijo   
            else:
                nueva_gen[g+1]=hijo1
            g=g+2
            t=t+1
        else:
            if t==2:
                if fdex[posicion1]<=fdex[posicion2]:                  
                    nueva_gen[4]=pobinicial[posicion2]
                else:
                    nueva_gen[4]=pobinicial[posicion1]
                break
                    
            if fdex[posicion1]<=fdex[posicion2]:
                
                nueva_gen[g]=pobinicial[posicion2]
            else:
                nueva_gen[g]=pobinicial[posicion1]
                
                
            if fitness_opc[0]<=fitness_opc[1]:
                
                nueva_gen[g+1]=hijo   
            else:
                nueva_gen[g+1]=hijo1
            break                           
            
            print("cruce no aprobado")    
            nueva_gen[g]=pobinicial[posicion1]
            nueva_gen[g+1]=pobinicial[posicion2]
            g=g+2
            t=t+1
        
        #corte
        
    print("generacion: ",maxi)
    print(nueva_gen)
    print("fitnes")
    print(fdex)
    maxi=maxi+1
    pobinicial=nueva_gen
    proba_sel_acum=[0,0,0,0,0]
    proba_sel=[0,0,0,0,0]
    fdex=[0,0,0,0,0]
    decimal_opc=[0,0]
    fitness_opc=[0,0]
    t=0
    g=0


