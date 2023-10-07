import operator
import math
import random
import numpy
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# Definicion de las funciones
def protectedDiv(left, right):
    try:
        return left / right
    except ZeroDivisionError:
        return 1

pset = gp.PrimitiveSet("MAIN", 1) #Se crea una primitiva, este seria en nodo incial
pset.addPrimitive(operator.add, 2) #
pset.addPrimitive(operator.sub, 2) #
pset.addPrimitive(operator.mul, 2) #se van agregando mas nodos al arbol con su respectivo operador
pset.addPrimitive(protectedDiv, 2) #
pset.addPrimitive(operator.neg, 1) #
pset.addPrimitive(math.cos, 1)
pset.addPrimitive(math.sin, 1)
#pset.addEphemeralConstant("rand101", lambda: random.randint(-1,1))
pset.renameArguments(ARG0='x') #Renombramos las variable ARG0 y ARG1
pset.renameArguments(ARG1='y')

creator.create("FitnessMin", base.Fitness, weights=(-1.0,)) #se crea la funcion fitness
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin) #Crea el arbol

toolbox = base.Toolbox()
toolbox.register("expr", gp.genHalfAndHalf, pset=pset, min_=1, max_=2) #se crea ramped HalfAndHalf,La mitad se genera con genGrow(), la otra mitad,con genFull(). con una latura minimina de 1 y una maxima de 2
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr) #se crea la población
toolbox.register("population", tools.initRepeat, list, toolbox.individual) #repite la interacion de creacion de poblacion
toolbox.register("compile", gp.compile, pset=pset) #tranforma los individuos a su forma compilable

def evalSymbReg(individual, points,points2):    # crea funcion para evaluar
    func = toolbox.compile(expr=individual)
    # Evaluate the mean squared error between the expression
    # and the real function : x*4 + x3 + x*2 + x
    #sqerrors = ((func(x) - x*4 - x3 - x2 - x)*2 for x in points) <==================
    sqerrors = ((func(x) - func(y) - x*2 - y*2)*2 for x,y in zip(points,points2))
    return math.fsum(sqerrors) / len(points),

#Valores de toolbox
#toolbox.register("evaluate", evalSymbReg, points=puntos())
toolbox.register("evaluate", evalSymbReg, points=[x/10. for x in range(-10,10)],points2=[y/10. for y in range(-10,10)])
toolbox.register("select", tools.selTournament, tournsize=3)    #seleccion por torneo de tamaño 3
toolbox.register("mate", gp.cxOnePoint)     #metodo de cruce de 1 punto
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)    # inicializacion de mutacion
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset) # mutación de probabilidad uniforme que agrega un nuevo subárbol a un nodo

toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))

def main():     #funcion principal
    random.seed(318)    #inicializacion de semilla 

    pop = toolbox.population(n=300)#se inicializa la poblacion
    hof = tools.HallOfFame(1)#mantiene a los mejores individuos, en esta caso solo se almacena 1

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)  #valores estaticos a llenar
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 40, stats=mstats,
                                   halloffame=hof, verbose=True) #inicializa el algotimo (inividios, operadores de evolución,probabilidad de cruza,
                                                                 #probabilidad de mutacion, numero de generaciones, funciones estadisticas, 
                                                                 #mejores individuos, registrar si o no las estadisticas)
    for i in hof:       #impresion de generaciones
        print(i)
        print(evalSymbReg(i,points=[x/10. for x in range(-10,10)],points2=[y/10. for y in range(-10,10)]))
    # print log
    return pop, log, hof

if __name__ == "__main__":
    main()