import pygame
import random
import time

pygame.init()
pygame.font.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
fieldsize = 10
z = 50
dish = 500
disw = 500
dis = pygame.display.set_mode((disw, dish))
winn = 'snek'
pygame.display.set_caption(winn)
clock = pygame.time.Clock()



def playgame():
    (snakecells,snakefood,direction,fps,foodcounter,prev) = init()
    while True:
        events = pygame.event.get()
        (snakecells,snakefood,direction,fps,foodcounter,prev) = gametick(snakecells,snakefood,direction,fps,foodcounter,prev,events)
        x=returnpath(prev,snakecells[0],snakefood)
        # print("food:", snakefood, "direction:", direction, "snake:", snakecells)
        drawgame(snakecells,snakefood,x)
        if isgameover(snakecells):
            break

        pygame.display.update()
        clock.tick(fps)



def init():
    snakecells = [(5,5), (5,6), (5,7)]
    snakefood = createfood(snakecells)
    direction = 'up'
    fps = 4
    foodcounter = 0
    prev={}
    return (snakecells,snakefood,direction,fps,foodcounter,prev)



def endgame():
    while True:
        events = pygame.event.get()
        drawgameover()
        for event in events:
            if event.key == pygame.K_RETURN:
                return
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(10)



def gametick(snakecells,oldsnakefood,direction,fps,oldfoodcounter,prev,_events):
    foodcounter = oldfoodcounter
    snakefood = oldsnakefood
    (direction, prev) = bfs(snakecells,snakefood)
    snakecells = movesnake(direction,snakecells)
    if snakecells[0] == (snakefood[0],snakefood[-1]):
        snakecells = eatfood(snakecells)
        snakefood = createfood(snakecells)
        foodcounter += 1
        if foodcounter == 10:
            fps += 1
            foodcounter = 0
            snakecells = [snakecells[0],snakecells[1],snakecells[2]]
    return (snakecells,snakefood,direction,fps,foodcounter,prev)



def createfood(snakecells):
    x = random.randint(0,9)
    y = random.randint(0,9)
    i = 0
    while i < len(snakecells):
        if (x,y) == snakecells[i]:
            x = random.randint(0,9)
            y = random.randint(0,9)
            i = 0
        else:
            i += 1
    return (x,y)



def movesnake(direction,snakecells):
    (x,y) = snakecells[0]
    if direction == 'up':
        tup = (x,(y-1) % fieldsize)
    if direction == 'down':
        tup = (x,(y+1) % fieldsize)
    if direction == 'left':
        tup = ((x-1) % fieldsize, y)
    if direction == 'right':
        tup = ((x+1) % fieldsize, y)
    snakecells.insert(0, tup)
    snakecells.pop()
    return snakecells



def get_neighbors(current,snake):
    (x,y)=current
    nu=(x,y-1)
    nd=(x,y+1)
    nl=(x-1,y)
    nr=(x+1,y)
    if x==9:
        nr=(0,y)
    if x==0:
        nl=(9,y)
    if y==9:
        nd=(x,0)
    if y==0:
        nu=(x,9)
    neighbors=[nu,nd,nl,nr]
    for cell in neighbors:
        if cell in snake:
            neighbors.remove(cell)

    return neighbors



def returnpath(prev,src,end):
    key=end
    path=[]
    while True:
        next=prev.get(key)
        path.append(next)
        if next==src:
            path.reverse()
            path.append(end)
            return path
        key=next



def bfs(snake,end):
    src=snake[0]
    (x,y)=src
    visited=[]
    queue=[]
    prev={}
    visited.append(end)
    queue.append(src)

    while queue:
        current=queue.pop(0)
        visited.append(current)

        for neighbor in get_neighbors(current,snake):
            if neighbor==end:
                prev[neighbor]=current
                x=returnpath(prev,src,end)
                if x[1][0]>x[0][0]:
                    if x[0][0]==0:
                        direction="left"
                    else:
                        direction="right"
                if x[1][0]<x[0][0]:
                    if x[0][0]==9:
                        direction="right"
                    else:
                        direction="left"
                if x[1][1]<x[0][1]:
                    if x[0][1]==9:
                        direction="down"
                    else:
                        direction="up"
                if x[1][1]>x[0][1]:
                    if x[0][1]==0:
                        direction="up"
                    else:
                        direction="down"
                print(x)
                return (direction,prev)
            if neighbor not in visited:
                queue.append(neighbor)
                prev[neighbor]=current



# def newdirect(path,direction):
#     if x[1][0]>x[0][0]:
#         if x[0][0]==0 and direction==:
#             direction="left"
#         else:
#             direction="right"
#     if x[1][0]<x[0][0]:
#         if x[0][0]==9:
#             direction="right"
#         else:
#             direction="left"
#     if x[1][1]<x[0][1]:
#         if x[0][1]==9:
#             direction="down"
#         else:
#             direction="up"
#     if x[1][1]>x[0][1]:
#         if x[0][1]==0:
#             direction="up"
#         else:
#             direction="down"
#     return direction


def isgameover(snakecells):
    i = 1
    while i < len(snakecells):
        if snakecells[0] == snakecells[i]:
            drawgameover()
            return True
        else:
            i += 1
    return False



def drawgameover():
    dis.fill(red)
    font = pygame.font.SysFont('Segoe UI', 35)
    font2 = pygame.font.SysFont('Segoe UI', 20)
    fontyesno = pygame.font.SysFont('Segoe UI', 5)
    fontdis = font.render('Game Over', True, (0,0,0))
    fontdis2 = font.render('Restart?', True, (0,0,0))
    fd3 = font.render('Yes (enter)', True, (255,255,255))
    fd4 = font.render('No, quit (esc)', True, (255,255,255))
    dis.blit(fontdis,(150,150))
    dis.blit(fontdis2, (180,185))
    dis.blit(fd3, (40,400))
    dis.blit(fd4, (250,400))



def eatfood(snakecells):
    snakecells.append(snakecells[-1])
    return (snakecells)



def drawgame(snakecells,snakefood,path):
    dis.fill(green)
    for item in path:
        pygame.draw.rect(dis, blue, (item[0]*z,item[1]*z,z,z))
    pygame.draw.rect(dis, white, (snakefood[0]*z,snakefood[1]*z,z,z))
    for cell in snakecells:
        pygame.draw.rect(dis, black, (cell[0]*z,cell[1]*z,z,z))



while True:
    playgame()
    endgame()
