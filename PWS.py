import pygame, random
import Q
pygame.init()

#----------[START DEFINE]----------

#ALGORITHM CONSTANTS
popSize = 300
popSlice = 10
mutChance = 3
mutAdd = 10

#FIELD CONSTANTS
startPos = (0,0)
startLength = 50
fruitAmount = 10
maze = ["0000000000",
        "0101010101",
        "0000000000",
        "1010101010",
        "0000000000",
        "0101010101",
        "0000000000",
        "1010101010",
        "0000000000",
        "0101010101"]

#KEYBINDS
resetKey = pygame.K_r
quitKey = pygame.K_ESCAPE
pathKey = pygame.K_s
fruitKey = pygame.K_g

#-----------[END DEFINE]-----------

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Pac-Man!")
pygame.display.set_icon(pygame.image.load("pacman.png"))
done = False
clock = pygame.time.Clock()

blockx,blocky = 600/10,600/10

mazeblit = pygame.Surface((600,600))

for y in range(len(maze)):
    for x in range(len(maze[y])):
        if maze[y][x] == "1":
            pygame.draw.rect(mazeblit, (0,128,0), (x*blockx,y*blocky,blockx,blocky))

class Pacman:
    def __init__(self):
        self.pacman = pygame.image.load("pacman.png")
        self.pacman.convert_alpha()
        self.posx = startPos[0]
        self.posy = startPos[1]
    def draw(self,s):
        s.blit(self.pacman,(self.posx*60,self.posy*60))

pacman = Pacman()

keypresses = 0

def evaluate(command):
    global keypresses, path
    for c in command:
        keypresses += 1
        try:
            if c == "r":
                if not maze[pacman.posy][pacman.posx+1] == "1":
                    pacman.posx += 1
                    path += "r"
            elif c == "l":
                if not maze[pacman.posy][pacman.posx-1] == "1" and pacman.posx-1 >= 0:
                    pacman.posx -= 1
                    path += "l"
            elif c == "u":
                if not maze[pacman.posy-1][pacman.posx] == "1" and pacman.posy-1 >= 0:
                    pacman.posy -= 1
                    path += "u"
            elif c == "d":
                if not maze[pacman.posy+1][pacman.posx] == "1":
                    pacman.posy += 1
                    path += "d"
            checkForFruits()
        except IndexError: pass;

fruits = []
reloadFruits = fruits.copy()

def genFruits():
    global fruits,reloadFruits
    fruits = []
    for i in range(fruitAmount):
        while True:
            lx,ly = random.randint(0,9),random.randint(0,9)
            if maze[ly][lx] == "0" and not (lx,ly) in fruits:
                fruits.append( (lx,ly) )
                break
    reloadFruits = fruits.copy()

fruitcount = 0

def checkForFruits():
    global fruitcount
    p = (pacman.posx,pacman.posy)
    if p in fruits:
        fruits.remove(p)
        fruitcount += 1

def getFitness(dna):
    global fruits,pacman,keypresses,fruitcount,path
    fruits = reloadFruits.copy()
    pacman = Pacman()
    keypresses = 0
    fruitcount = 0
    path = ""
    evaluate(dna)
    if fruitcount == fruitAmount:
        return fruitcount + fruitcount/keypresses
    else:
        return fruitcount

def mutate(gen):
    tGen = gen.copy()
    for dna in tGen:
        while Q.Qchance(mutChance):
            if Q.Qchance(mutAdd):
                if Q.Qchance(2):
                    p = Q.Qran(len(dna[0])-1)
                    dna[0] = Q.Qreplace(dna[0],p,dna[0][p]+Q.Qel("lrud"))
                else:
                    dna[0] = Q.Qreplace(dna[0],Q.Qran(len(dna[0])-1),"")
            else:
                dna[0] = Q.Qreplace(dna[0],Q.Qran(49),Q.Qel("lrud"))
    return tGen

initBatch = ["".join([Q.Qel("lrud") for i in range(startLength)]) for i in range(popSize)]
generation = [[i,0] for i in initBatch]

showpath = True
path = ""
#path = "rrrddddldduulldddddrrrrrrrrur"

genFruits()
gen = 0

while not done:
    sGen = generation.copy()
    generation = mutate(generation)
    generation = [[i[0],getFitness(i[0])] for i in generation]
    generation = sorted(generation,key=lambda x:-x[1])
    generation = generation[:int(popSize/popSlice/2)]*int(popSlice)
    generation = generation[:int(len(generation)/2)]+sGen[:int(len(generation)/2)]

    generation = sorted(generation,key=lambda x:-x[1])
    
    gen += 1
    print(gen, generation[0])

    getFitness(generation[0][0])
    
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == fruitKey:
                genFruits()
            elif event.key == resetKey:
                gen = 0
                initBatch = ["".join([Q.Qel("lrud") for i in range(startLength)]) for i in range(popSize)]
                generation = [[i,0] for i in initBatch]
            elif event.key == pathKey:
                showpath = not showpath
            elif event.key == quitKey:
                done = True

    screen.blit(mazeblit, (0,0))

    for f in reloadFruits:
        pygame.draw.rect(screen, (0,255,255), (f[0]*60+20,f[1]*60+20,20,20))

    if showpath:
        tPath = "s"+path+"e"
        rposx = 0
        rposy = 0
        for char in tPath:
            if char == "s":
                pygame.draw.rect(screen, (255,0,255), (rposx*60+25,rposy*60+25,10,10))
            if char == "r":
                rposx += 1
                pygame.draw.rect(screen, (0,255,0), (rposx*60+25,rposy*60+25,10,10))
                pygame.draw.rect(screen, (255,255,255), ((rposx-1)*60+35,rposy*60+28,50,4))
            if char == "l":
                rposx -= 1
                pygame.draw.rect(screen, (0,255,0), (rposx*60+25,rposy*60+25,10,10))
                pygame.draw.rect(screen, (255,255,255), ((rposx+1)*60-25,rposy*60+28,50,4))
            if char == "u":
                rposy -= 1
                pygame.draw.rect(screen, (0,255,0), (rposx*60+25,rposy*60+25,10,10))
                pygame.draw.rect(screen, (255,255,255), (rposx*60+28,(rposy+1)*60-25,4,50))
            if char == "d":
                rposy += 1
                pygame.draw.rect(screen, (0,255,0), (rposx*60+25,rposy*60+25,10,10))
                pygame.draw.rect(screen, (255,255,255), (rposx*60+28,(rposy-1)*60+35,4,50))
            if char == "e":
                pygame.draw.rect(screen, (255,0,0), (rposx*60+25,rposy*60+25,10,10))

    pacman.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.display.quit()
