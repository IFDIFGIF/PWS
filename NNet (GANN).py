import numpy as np
import math
import random

NEURAL_NET_SHAPE = (4, 3, 3, 2)

TRAINING = [
    ( np.matrix([1.0, 0.0, 1.0, 0.0]) , np.matrix([0.666, 0.666]) ),
    ( np.matrix([0.0, 1.0, 0.0, 1.0]) , np.matrix([0.123, 0.321]) ),
    ( np.matrix([0.0, 1.0, 1.0, 0.0]) , np.matrix([0.789, 0.111]) ),
    ( np.matrix([1.0, 0.0, 0.0, 1.0]) , np.matrix([0.5, 0.5]) )
    ]

weights = []

#Neural Net
def sigma(val):
    return 1/(1+math.exp(-val))
  
def sigmoid( matrix ):
    m = matrix.copy()
    for x in range(m.shape[0]):
        for y in range(m.shape[1]):
          m.itemset(x,y,sigma(m.item(x,y)))
    return m
  
def calc( i ):
    l = i
    for w in weights:
        l = sigmoid( l * w )
    return l
  
def loadDNA( dna ):
    global weights
    weights = [
        np.matrix( [[dna[0], dna[1], dna[2]], [dna[3], dna[4], dna[5]], [dna[6], dna[7], dna[8]], [dna[9], dna[10], dna[11]]] ),
        np.matrix( [[dna[12], dna[13], dna[14]], [dna[15], dna[16], dna[17]], [dna[18], dna[19], dna[20]]] ),
        np.matrix( [[dna[21], dna[22]], [dna[23], dna[24]], [dna[25], dna[26]]] )
    ]

#Genetic Algorithm
def generateDNA():
    return [random.random()*2-1 for i in range(27)]
  
def mutateDNA( dna ):
    tDna = dna.copy()
    for i in range(len(tDna)):
        if random.randint(0,20) == 0:
          tDna[i] = tDna[i] + random.random()*2-1
    return tDna
  
def off(m1, m2):
    return abs(m1.item(0,0) - m2.item(0,0)) + abs(m1.item(0,1) - m2.item(0,1))

def evaluate( dna ):
    loadDNA( dna )
    return sum([off(calc(t[0]), t[1]) for t in TRAINING])
  
#GANN LOOP
generation = [generateDNA() for i in range(200)]
for gen in range(500):
    generation.sort(key=evaluate)
    generation = generation[:20]*10
    print("generation " + str(gen) + ": " + str(evaluate(generation[0])))
    generation = [mutateDNA(i) for i in generation]
