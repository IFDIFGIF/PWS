import pygame, math, random, ast
pygame.init()
pygame.font.init()

#variables1
generation = []
generations = 0
cities = []

#load specific cities to be found in 'TSPlastCities.txt'.
#To create TSPlastCities.txt, set to False.
#If False, every new generation will write their cities in this file.
loadFromFile = False

#Algorithm constants
mut = 0.5
popSize = 1000
selectionTop = 100

#add a graph (toggleable with G)
graph = True

#graph variables init
dispGraph = False
graphData = [[0,0]]*600
top = 1
low = 1000

clock = pygame.time.Clock()

screen = pygame.display.set_mode((1200, [600,800][int(graph)]))
done = False

#Calculates total distance between points based on a DNA list.
def evaluate(listy):
    l = listy + [listy[0]]
    tSum = 0
    for i in range(len(listy)):
        xdif = cities[l[i]][0]-cities[l[i+1]][0]
        ydif = cities[l[i]][1]-cities[l[i+1]][1]
        tSum += (xdif**2+ydif**2)**0.5
    return tSum

#with a chance of mut, a random piece of the DNA list gets flipped.
def mutate(val,mut):
    val = val[:]
    if random.random() <= mut:
        for voldemort in range(random.randint(1,int(2/mut))):
            p = random.randint(0,len(val)-1)
            q = random.randint(0,len(val)-1)
            if p > q:
                p,q = q,p
            val = val[:p] + val[p:q+1][::-1] + val[q+1:]
    return val

#loads or generates new cities and resets the generation
def newTSP(useFile=False):
    global generation, cities, generations
    if useFile:
        f = open("TSPlastCities.txt","r")
        cities = ast.literal_eval(f.readline())
        f.close()
    else:
        cities = []
        for c in range(50):
            cities.append((random.randint(0,100),random.randint(0,100)))
        f = open("TSPlastCities.txt","w")
        f.write(str(cities))
        f.close()
    generations = 0
    generation = [ list(range(50)) for i in range(popSize) ]

#update the graph's data
def addGraph(val,boolean):
    if boolean:
        graphData[599][1] = val
    else:
        graphData.remove(graphData[0])
        graphData.append([val,0])

#actually draw the graph, and simultaneously
#checks the bounds so it can adjust the graph
def drawGraph(gens):
    global top, low
    p = top+1
    q = low-1
    top,low = 1,1000
    for i in range(len(graphData)-1):
        if graphData[i][0] > top:
            top = graphData[i][0]
        if graphData[i][1] > top:
            top = graphData[i][1]
        if graphData[i][0] < low:
            low = graphData[i][0]
        if graphData[i][1] < low:
            low = graphData[i][1]
        data = graphData[i]
        data2 = graphData[i+1]
        pygame.draw.line(screen, (0,255,0), (i*2,775-150*(data[1]-q)/(p-q)), (i*2+2,775-150*(data2[1]-q)/(p-q)))
        pygame.draw.line(screen, (255,0,0), (i*2,775-150*(data[0]-q)/(p-q)), (i*2+2,775-150*(data2[0]-q)/(p-q)))

#draw the cities and a line through it based on a DNA list.
#xmod is used to draw the best on the left and the mean on the right.
def drawTSP(tspdna,xmod):
    e = evaluate(tspdna)
    dnaFitness = font.render(str(e), False, (0,255,0), (0,0,0))
    t = tspdna + [tspdna[0]]
    for i in range(len(t)-1):
        x = 6*cities[t[i]][0]+xmod
        y = 600-6*cities[t[i]][1]
        xc = 6*cities[t[i+1]][0]+xmod
        yc = 600-6*cities[t[i+1]][1]
        pygame.draw.line(screen, (255,255,255), (x,y), (xc,yc), 5)
    for i in cities:
        x = 6*i[0]+xmod
        y = 600-6*i[1]
        pygame.draw.circle(screen, (255,0,0), (x,y), 10)
    screen.blit(dnaFitness, (300+xmod,600-14))
    if graph:
        addGraph(e, bool(xmod))

#text constants
font = pygame.font.SysFont(None,20)
best = font.render("best", False, (255,255,255), (0,0,0))
mean = font.render("mean", False, (255,255,255), (0,0,0))
graphKey = font.render("press 'G' to display graph", False, (255,255,255), (0,0,0))
mutVar = font.render("mut = "+str(mut), False, (255,255,255), (0,0,0))
popCount = font.render("pop size = "+str(popSize)+", "+str(int(100*selectionTop/popSize))+"%", False, (255,255,255), (0,0,0))
pauseHint = font.render("press 'P' to pause", False, (255,0,0), (0,0,0))

newTSP(loadFromFile)

pause = 0
paused = 0

#main loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == 32: #space triggers new generation
                print("new gen")
                newTSP(loadFromFile)
            if event.key == 114: #R resets generation
                generations = 0
                generation = [ list(range(50)) for i in range(popSize) ]
            if event.key == 103: #G to toggle graph
                dispGraph = not dispGraph
            if event.key == 112: #P to pause
                pause = not pause
                paused = 1
                pygame.draw.rect(screen, (0,0,0), (1200-wid,0,wid,pauseHint.get_height()))
                pygame.draw.rect(screen, (255,0,0), (1180,10,10,40))
                pygame.draw.rect(screen, (255,0,0), (1160,10,10,40))
                #^draws pause icon
                
    if not pause:
        screen.fill((0,0,0))
        generation = sorted([mutate(i,mut) for i in generation],key=evaluate)
        #mutate the entire generation,
        #then sort it based on total distance between cities
        #least distance is first
        drawTSP(generation[0],0) #draw best
        drawTSP(generation[int(popSize/2-1)],605) #draw mean
        genCount = font.render("generation "+str(generations), False, (255,255,255), (0,0,0))
        fpsCount = font.render(str(int(clock.get_fps()))+" fps", False, (255,255,255), (0,0,0))
        #draw the texts
        screen.blit(genCount, (0,0))
        screen.blit(mutVar, (0,14))
        screen.blit(popCount, (0,28))
        screen.blit(fpsCount, (1150,600-14))
        screen.blit(best, (0,600-14))
        screen.blit(mean, (605,600-14))
        pygame.draw.line(screen, (0,255,0), (600,0), (600,600))
        if graph:
            pygame.draw.line(screen, (0,255,0), (0,600), (1200,600))
        if dispGraph and graph:
            drawGraph(generations)
        elif graph:
            screen.blit(graphKey, (550,700-14))
        generation = generation[:selectionTop]*int((popSize/selectionTop))
        #let the first selectionTop DNA lists live, kill off the rest.
        #and duplicate until generation is full again.
        generations += 1

    if not paused:
        wid = pauseHint.get_width()
        screen.blit(pauseHint, (1200-wid,0))

    if generations == 2: #for particularly awesome mutations
        pygame.image.save(screen, "TSPgen1.bmp")
    if generations == 11:
        pygame.image.save(screen, "TSPgen10.bmp")
    if generations == 101:
        pygame.image.save(screen, "TSPgen100.bmp")
    if generations == 501:
        pygame.image.save(screen, "TSPgen500.bmp")
    if generations == 2001:
        pygame.image.save(screen, "TSPgen2000.bmp")
              
    pygame.display.flip()
    clock.tick()
