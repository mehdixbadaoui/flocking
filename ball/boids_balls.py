#!/usr/bin/env python
# Boid implementation in Python using PyGame
# Ben Dowling - www.coderholic.com

import sys, pygame, random, math

pygame.init()

size = width, height = 800, 600
black = 0, 0, 0

finishX = 700
finishY = 500

maxVelocity = 3
numBoids = 20
numObs = 2
boids = []

class Boid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0
        self.isMouse = False
        self.captured = False

    "Return the distance from another boid"
    def distance(self, boid):
        distX = self.x - boid.x
        distY = self.y - boid.y        
        return math.sqrt(distX * distX + distY * distY)

    "Move closer to a set of boids"
    def moveCloser(self, boids):
        if len(boids) < 1: return
            
        # calculate the average distances from the other boids
        avgX = 0
        avgY = 0
        for boid in boids:
            if boid.x == self.x and boid.y == self.y:
                continue
            if boid.isMouse:
                boid.velocityX += numBoids / 2
                boid.velocityY += numBoids / 2


            avgX += (self.x - boid.x)
            avgY += (self.y - boid.y)

        avgX /= len(boids)
        avgY /= len(boids)

        # set our velocity towards the others
       
        self.velocityX -= (avgX / 100)
        self.velocityY -= (avgY / 100)
        
    "Move with a set of boids"
    def moveWith(self, boids):
        if len(boids) < 1: return
        # calculate the average velocities of the other boids
        avgX = 0
        avgY = 0
                
        for boid in boids:
            if boid.isMouse:
                boid.velocityX += numBoids
                boid.velocityY += numBoids

            avgX += boid.velocityX
            avgY += boid.velocityY

        avgX /= len(boids)
        avgY /= len(boids)

        if not self.isMouse:
            # set our velocity towards the others
            self.velocityX += (avgX / 40)
            self.velocityY += (avgY / 40)

    
    "Move away from a set of boids. This avoids crowding"
    def moveAway(self, boids, minDistance):
        if len(boids) < 1: return
        
        distanceX = 0
        distanceY = 0
        numClose = 0

        for boid in boids:
            distance = self.distance(boid)
            if  distance < minDistance:
                numClose += 1
                xdiff = (self.x - boid.x) 
                ydiff = (self.y - boid.y) 
                
                if xdiff >= 0: xdiff = math.sqrt(minDistance) - xdiff
                elif xdiff < 0: xdiff = -math.sqrt(minDistance) - xdiff
                
                if ydiff >= 0: ydiff = math.sqrt(minDistance) - ydiff
                elif ydiff < 0: ydiff = -math.sqrt(minDistance) - ydiff

                distanceX += xdiff 
                distanceY += ydiff 
        
        if numClose == 0:
            return
            
        self.velocityX -= distanceX / 10
        self.velocityY -= distanceY / 10
        
    "Perform actual movement based on our velocity"
    def move(self):
        if abs(self.velocityX) > maxVelocity or abs(self.velocityY) > maxVelocity:
            scaleFactor = maxVelocity / max(abs(self.velocityX), abs(self.velocityY))
            self.velocityX *= scaleFactor
            self.velocityY *= scaleFactor
        
        self.x += self.velocityX
        self.y += self.velocityY

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

obstacles = [Obstacle(200,200), Obstacle(400,400), Obstacle(600,600)]

screen = pygame.display.set_mode(size)
background_image = pygame.image.load("D:/Documents/UNI/IA/boids/ball/grass.jpg")

sheep = pygame.image.load("sheep.png")
tree = pygame.image.load("tree.png")
dog = pygame.image.load("dog.png")
fence = pygame.image.load("fence.png")

sheeprect = sheep.get_rect()
treerect = tree.get_rect()
dogrect = dog.get_rect()
fencerect = fence.get_rect()

font = pygame.font.Font('freesansbold.ttf', 50)
text = font.render('LEVEL COMPLETE!', True, (255, 255, 255))
textRect = text.get_rect()
textRect.center = (400, 300)

restart_button = button((255, 255, 255), 300, 450, 200, 100, 'RESTART')

def restart():

    boids = []
    obstacles = [Obstacle(200,200), Obstacle(400,400), Obstacle(600,600)]
    for i in range(numBoids):
        boids.append(Boid(random.randint(0, width * 0.9), random.randint(0, height * 0.9)))

    for i in range(numObs):
        obstacles.append(Obstacle(random.randint(0, width), random.randint(0, height)))

    print("restarting")
# create boids at random positions
for i in range(numBoids):
    boids.append(Boid(random.randint(0, width*0.9), random.randint(0, height*0.9)))

for i in range(numObs):
    obstacles.append(Obstacle(random.randint(0, width), random.randint(0, height)))

mouse_visible = False

while 1:
    pygame.mouse.set_visible(mouse_visible)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for boid in boids:
        closeBoids = []
        closeObs = []

        for otherBoid in boids:
            if otherBoid == boid: continue
            distance = boid.distance(otherBoid)
            if distance < 200:
                closeBoids.append(otherBoid)

        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        mouse = Boid(Mouse_x, Mouse_y)
        mouse.isMouse = True
        closeBoids.append(mouse)

        for obs in obstacles:
            distance = boid.distance(obs)
            if distance < 200:
                closeObs.append(obs)

        boid.moveCloser(closeBoids)
        boid.moveWith(closeBoids)
        boid.moveAway(closeBoids, 20)
        boid.moveAway(closeObs, 35)


        #print(avgX, ",",avgY, " - ", pygame.mouse.get_pos())

        # ensure they stay within the screen space
        # if we roubound we can lose some of our velocity
        borderX = 25
        borderY = 25
        if boid.x > finishX and boid.y > finishY:
            boid.captured = True
            borderX = width * 0.9
            borderY = height * 0.9

        if boid.x < borderX and boid.velocityX < 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.x > width - 25 and boid.velocityX > 0:
            boid.velocityX = -boid.velocityX * random.random()
        if boid.y < borderY and boid.velocityY < 0:
            boid.velocityY = -boid.velocityY * random.random()
        if boid.y > height - 25 and boid.velocityY > 0:
            boid.velocityY = -boid.velocityY * random.random()

        boid.move()
        allCaptured = True
        for b in boids:
            if boid.isMouse: continue
            if not b.captured: allCaptured = False



    # screen.fill()
    screen.blit(background_image, [0, 0])
    for boid in boids:
        boidRect = pygame.Rect(sheeprect)
        boidRect.x = boid.x
        boidRect.y = boid.y
        screen.blit(sheep, boidRect)

    for obs in obstacles:
        treeRect = pygame.Rect(treerect)
        treeRect.x = obs.x
        treeRect.y = obs.y
        screen.blit(tree, treeRect)

    dogRect = pygame.Rect(dogrect)
    dogRect.x = Mouse_x
    dogRect.y = Mouse_y
    screen.blit(dog, dogRect)

    fenceRect = pygame.Rect(fencerect)
    fenceRect.x = 720
    fenceRect.y = 540
    screen.blit(fence, fenceRect)

    # print(pygame.mouse.get_pressed() == (1, 0, 0))

    if allCaptured:
        screen.blit(text, textRect)
        boids = []
        obstacles = [Obstacle(200,200), Obstacle(400,400), Obstacle(600,600)]
        restart_button.draw(screen)
        mouse_visible = True

        if (pygame.mouse.get_pressed() == (1, 0, 0)):
            if(restart_button.isOver(pygame.mouse.get_pos())):
                for i in range(numBoids):
                    boids.append(Boid(random.randint(0, width * 0.9), random.randint(0, height * 0.9)))

                for i in range(numObs):
                    obstacles.append(Obstacle(random.randint(0, width), random.randint(0, height)))

                mouse_visible = False
                restart()

    pygame.display.flip()
    pygame.time.delay(10)
