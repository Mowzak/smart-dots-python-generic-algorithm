import math
import pygame, sys
from pygame.locals import *
import random
from time import sleep, time
# Setting up color objects
BLUE  = (255, 255, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
gen = 0
rad = 5
number_of_pop = 500
movement = 10
counter = 0
first_gen = True
##################################################################################################################
#setting the window
DISPLAYSURF = pygame.display.set_mode((1000,800)) 
DISPLAYSURF.fill(WHITE)
FPS = 30

pygame.init()
##################################################################################################################
#this our dots
class dot:
    def __init__(self) -> None:
        self.x = 500
        self.y = 780
        self.dead = False
        self.win = False
        self.step = ""
        self.score = 0
        self.color = GREEN
    ##################################################################################################################
    def move(self):
        self.step+=""
        a = random.choice([1,2,3,4,5,6,7,8])
        match a:
            case 1:
                self.y -= movement
                self.step += "1"
                pass
            case 2:
                self.y -=movement
                self.x +=movement
                self.step +="2"
                pass
            case 3:
                self.x +=movement
                self.step +="3"
            case 4:
                self.y +=movement
                self.x +=movement
                self.step +="4"
            case 5:
                self.y += movement
                self.step +="5"
            case 6:
                self.y +=movement
                self.x -=movement
                self.step +="6"
            case 7:
                self.x -= movement
                self.step += "7"
            case 8:
                self.y -=movement
                self.x -=movement
                self.step +="8"
    ##################################################################################################################
    def is_dead(self):
        blocks = (
                pygame.Rect(0,0,10, 1000),#main blocks
                pygame.Rect(990,0,30, 1000),#main blocks
                pygame.Rect(0,0,1000, 10),#main blocks
                pygame.Rect(0,790,1000, 10),#main blocks

                # pygame.Rect(700,300,10, 700),
                pygame.Rect(300,400,500, 10),
                # pygame.Rect(300,600,700, 10),
                )

        per_rect = Rect(per.x,per.y, 10,10)
        for block in blocks:
            pygame.draw.rect(DISPLAYSURF, BLUE, block)
            if pygame.Rect.colliderect(block,per_rect):
                                    self.dead = True
                                    continue
    ##################################################################################################################
    def move_two(self,step): #this func work for after first genrate
        if len(self.step)<=step:
            return  

        match self.step[step]:
            case "1":
                self.y -= movement
            case "2":
                self.y -=movement
                self.x +=movement
            case "3":
                self.x +=movement
            case "4":
                self.y +=movement
                self.x +=movement
            case "5":
                self.y += movement
            case "6":
                self.y +=movement
                self.x -=movement
            case "7":
                self.x -= movement
            
            case "8":
                self.y -=movement
                self.x -=movement
##################################################################################################################

def highest(pop):#this func check the highest step's len becuse we want to kill all dots after they all stop moving
    a = []
    for i in pop:
        a.append(len(i.step))
        
    a.sort(reverse=True)

    return a[0]
##################################################################################################################
def fitness(pop):
    lst = [[1000000000,1]]
    for i in pop:
        if i.win:#the winner dot have most score we sort them by they steps to pick fastet dot
            
            lst.append([len(i.step),2+(1/len(i.step))])
            i.score = 2+(1/len(i.step))
            continue

        s = math.dist([i.x,i.y],[250,50])
        try:

            i.score = 1/(s*s)
        except ZeroDivisionError:
            print("eror")
            i.score = 2

    pop.sort(reverse=True,key=lambda x:x.score)
    # print(max(pop,key=lambda x:x.score).score,pop[0].score)
    # print(min(lst,key=lambda x:x[0]))
    # print("*"*100)
    return pop
##################################################################################################################
def crossover(pop):
    new_pop = []
    scors = fitness(pop)
    best = dot() #best dot
    best.step = scors[0].step
    best.color = BLACK
    new_pop.append(best)
    for i in range(number_of_pop//2):

        a,b = scors[random.randint(0,5)],scors[random.randint(0,5)]
        new_a,new_b = dot(),dot()
        min([len(a.step),len(b.step)])
        cut_number = random.randint(0,min([len(a.step),len(b.step)]))

        new_a.step = a.step[:cut_number]+b.step[cut_number:]
        new_b.step = a.step[cut_number:]+b.step[:cut_number]

        new_pop.append(new_a)
        new_pop.append(new_b)
    return new_pop

##################################################################################################################
# def mut(pop):
#     scors = fitness(pop)

#     new_pop = []
#     a = dot()
#     a.step = scors[0].step
#     a.color = BLACK
#     new_pop.append(a)

#     for i in [int(i) for i in "0"*(number_of_pop*40//100)+"1"*(number_of_pop*8//100)+"2"*(number_of_pop*2//100)]:
#         demo_step = [w for w in scors[i].step]

#         for u in range(0,len(scors[i].step)//100):
#             demo_step[random.randint(0,len(demo_step)-1)] = random.choice([str(i) for i in range(1,9)])
#             demo_step.insert(random.randint(0,len(demo_step)-1),random.choice([str(i) for i in range(1,9)]))

#         # for u in range(2):
#         #     demo_step.insert(random.randint(0,len(demo_step)-1),random.choice([str(i) for i in range(1,9)]))

#         do = dot()
#         do.step = "".join(demo_step)
#         new_pop.append(do)

#     return new_pop

def mut(pop):
    mut_number = 100
    add_number = 50
    new_pop = []
    for i in pop:
        demo_step = [w for w in i.step]

        for u in range(0,len(i.step)//mut_number):
            demo_step[random.randint(0,len(demo_step))-1] = random.choice([str(i) for i in range(1,9)])
        for u in range(len(i.step)//add_number):
            demo_step.insert(random.randint(0,len(demo_step)-1),random.choice([str(i) for i in range(1,9)]))
        do = dot()
        do.step = "".join(demo_step)
        new_pop.append(do)

    return new_pop
##################################################################################################################
def generic(pop):
    a = crossover(pop)
    champ = a[0]

    p = mut(a)
    p.append(champ)
    return p

##################################################################################################################


pop = [dot() for i in range(number_of_pop)]
while True:
    # sleep(.01)
    
    goal = Rect(250, 50, 45,30)
    pygame.draw.rect(DISPLAYSURF, RED, goal)

    ##################################################################################################################
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(f"""GEN:{str(gen)}   number of pop:{str(len(pop))}""", True, BLACK,)
    textRect = text.get_rect()
    textRect.center = (500,650)
    DISPLAYSURF.blit(text, textRect)

    ##################################################################################################################
    if first_gen:

        for per in pop:
            per_rect = Rect(per.x,per.y, 10,10)
            collide = pygame.Rect.colliderect(goal,
                                        per_rect)
            if collide or per.dead:
                per.win = collide
                per.dead = True
            else:
                per.move()
                per.is_dead()
            pygame.draw.circle(DISPLAYSURF,per.color,(per.x,per.y),rad)
            # pygame.draw.rect(DISPLAYSURF, per.color, per_rect)

    ##################################################################################################################
    else:
        if counter >= highest_step:
            for i in pop:
                i.dead = True
        for per in pop:
            per_rect = Rect(per.x,per.y, 10,10)
            collide = pygame.Rect.colliderect(goal,
                                        per_rect)
            if collide or per.dead:
                per.step = per.step[:counter]
                per.win = collide
                per.dead = True

            else:


                per.move_two(counter)
                per.is_dead()
            
            # if per.color == BLACK:

            pygame.draw.circle(DISPLAYSURF,per.color,(per.x,per.y),rad)
            
        
    ##################################################################################################################
    counter+=1
    if not False in [i.dead for i in pop]:

        pop = generic(pop)
        highest_step = highest(pop)
        # print(pop)
        counter = 0
        gen+=1
        first_gen = False
        
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.fill(WHITE)
   
