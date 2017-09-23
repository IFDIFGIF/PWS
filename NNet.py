import pygame, math, random
import Q
import numpy as np
pygame.init()

def getText(string,cap=None,size=40):
    font = pygame.font.SysFont(None,int(size*1.5))
    return font.render(string[:cap], False, (255,255,255))

screen = pygame.display.set_mode((567*2, 354*2))
done = False

clock = pygame.time.Clock()

nodes = (3, 4, 3)
layers = 3

inputLayer = np.matrix('1.0 1.0 1.0')
hiddenLayer = np.matrix('0.0 0.3245 0.0 0.0')
outputLayer = np.matrix('0.0 0.0 0.0')

layerValues = [inputLayer,hiddenLayer,outputLayer]

w1 = np.matrix('0.0 0.0 0.0 0.0; 0.0 0.0 0.0 0.0; 0.0 0.0 0.0 0.0')
w2 = np.matrix('1.0 0.0 0.0; 1.0 0.0 0.0; 1.0 0.0 0.0; 1.0 0.0 0.0')

for x in range(3):
    for y in range(4):
        w1.itemset(x,y,Q.Qran()*20-10)

for x in range(4):
    for y in range(3):
        w2.itemset(x,y,Q.Qran()*20-10)

weights = [w1,w2]

sectionx = int(600/(layers+1))

def getNodeYValues(n):
    tList = []
    sectiony = 600/(nodes[n]+1)
    for i in Q.Qr(nodes[n]):
        tList.append(sectiony*(i+1))
    return tList

def drawNodes():
    for i in Q.Qr(layers):
        sectiony = 600/(nodes[i]+1)
        size = 60/nodes[i]
        for n in Q.Qr(nodes[i]):
            p = (sectionx*(i+1),int(sectiony*(n+1)))
            pygame.draw.circle(screen, (255,0,0), p, int(size))
            t = getText(str(layerValues[i].A1[n]),5,size)
            screen.blit(t,(p[0]-t.get_width()/2,p[1]-t.get_height()/2))
            

def drawLines():
    for i in Q.Qr(layers-1):
        sectiony = 600/(nodes[i]+1)
        for n in Q.Qr(nodes[i]):
            y = getNodeYValues(i+1)
            for c in y:
                pygame.draw.line(screen, (255,255,255), (sectionx*(i+1),int(sectiony*(n+1))), (sectionx*(i+2),int(c)))

def sigma(n):
    return 1/(1+math.exp(-n))

def sigmoid(matr):
    matr = matr[:]
    for x in Q.Qr(matr.shape[0]):
        for y in Q.Qr(matr.shape[1]):
            matr.itemset(x,y,sigma(matr.item(x,y)))
    return matr

def compute():
    layerValues[1] = sigmoid(layerValues[0] * weights[0])
    layerValues[2] = sigmoid(layerValues[1] * weights[1])

scale = 1
dimx = int(567/scale)
dimy = int(354/scale)

img = pygame.transform.scale(pygame.image.load("gogh.jpg"),(dimx,dimy))

m = pygame.Surface((dimx,dimy))
for x in range(dimx):
    #print("{}% done".format(int(x*10/6)))
    for y in range(dimy):
        #layerValues[0] = np.matrix([[x*10/300-1,abs(x*10-y*10)/300-1,y*10/300-1]])
        c = img.get_at((x,y))
        layerValues[0] = np.matrix([[c[0]/255-0.5,c[1]/255-0.5,c[2]/255-0.5]])
        compute()
        m.set_at((x,y),(int(layerValues[2].A1[0]*255),int(layerValues[2].A1[1]*255),int(layerValues[2].A1[2]*255)))

m = pygame.transform.scale(m, (dimx*2,dimy*2))
img = pygame.transform.scale(img, (dimx*2,dimy*2))

s = True
#counter = 0
while not done:
    #counter = Q.Qran()
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == 114:
                s = not s

    #drawLines()
    #drawNodes()
    #compute()
    if s:
        screen.blit(m,(0,0))
    else:
        screen.blit(img,(0,0))

    #weights[0].itemset(2,0,counter)
   
    pygame.display.flip()
    clock.tick(60)

pygame.display.quit()
