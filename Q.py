import random

#to keep track of index in Qel(l)
class Q:
    def __init__(self):
        self.index = self.i = 0
        self.screen = None
        self.clock = None

#replaces substring with another string
def Qreplace(s,p,c,l=1):
    return s[:p] + c + s[p+l:]
Qrp = Qreplace

#return random number between 0 and n
def Qran(n=None):
    if not n == None: return random.randint(0,n);
    else: return random.random()

#retrieve random element, stores index in Q.index
def Qelement(l):
    Q.index = Q.i = Qran(len(l)-1)
    return l[Q.i]
Qel = Qelement

#chance of 1 in n to return True
def Qchance(n):
    return not Qran(n-1)

#returns a range length n or of length of length n
def Qrange(n):
    if type(n) == int: return range(n)
    else: return range(len(n))
Qr = Qrange

#creates temporary list of tuples to access index
def Qlist(l):
    return [(l[i],i) for i in Qr(l)]
Ql = Qlist

#retrieves input,
#and if the input is convertable into an int it will return that.
def Qinput(t):
    Q = input(t)
    try: return int(Q)
    except: return Q

#runs through all values specified,
#and stores the output of the function when applied to those numbers
#EG: Qgetall(lambda x,y:x+y,3,3)
#will result in [0, 1, 2, 1, 2, 3, 2, 3, 4]
def Qall(*args):
    try: return [[x]+y for x in range(args[0]) for y in Qall(*args[1:])]
    except: return [[x] for x in range(*args)]

def Qgetall(func, *n):
    return [func(*a) for a in Qall(*n)]

Qn = Qneg = lambda x: not x
Qb = Qbool = lambda x: bool(x)
Qno = Qnone = lambda x: None

def Qnany(l):
    return any(map(Qn, l))

Q = Q()

try:
    import pygame as pyg
    print('Qpygame loaded.')
    def QshowScreen(dim=(600,600)):
        Q.screen = pyg.display.set_mode(dim)
        Q.clock = pyg.time.Clock()
    Qss = QshowScreen
    def QquitScreen():
        pyg.display.quit()
    Qqs = QquitScreen
    def QdrawLine(pos1,pos2,col=(255,255,255)):
        pyg.draw.line(Q.screen,col,pos1,pos2)
    Qdl = QdrawLine
    def QflipDisplay(t=60):
        for i in pyg.event.get(): pass
        pyg.display.flip()
        Q.screen.fill((0,0,0))
        return Q.clock.tick(t)
    Qfd = QflipDisplay
except: pass

try:
    import numpy as np
    print('Qnumpy loaded.')
except: pass

if __name__ != "__main__": print("Using Q v3.7")
else: print("Working fine!")
