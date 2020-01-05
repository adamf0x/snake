import pygame
import random
import json 
import os
pygame.init()

#segments of the snake have coordinates, a velocity (movement speed) and a direction of travel (0 = up, 1 = left, 2 = right, 3 = left)
class SnakePart():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.vel = 50
        self.traveldir = 0
    #move the head based on the direction it is moving in 
    def move(self):
        if self.traveldir == 0:
            self.y -= 50
            if self.y < 0:
                self.y = windowHeight
        if self.traveldir == 1:
            self.x -= 50
            if self.x < 0:
                self.x = windowWidth
        if self.traveldir == 2:
            self.y += 50
            if self.y > windowHeight:
                self.y = 0
        if self.traveldir == 3:
            self.x += 50
            if self.x > windowWidth:
                self.x = 0

    #draw the rectangle on the canvas 
    def drawSnake(self):
        colourA = random.randint(0,255)
        colourB = random.randint(0,255)
        colourC = random.randint(0,255)
        pygame.draw.rect(win,(colourA,colourB,colourC), (self.x,self.y,self.width,self.height))
    def __str__(self):
        return str(self.x) + " " + str(self.y) + " " + str(self.traveldir)
        
#apple that appear on the canvas
class Food():
    #apples are assigned random coordinates when they are instantiated 
    def __init__(self):
        self.x = random.randrange(0,windowWidth,50)
        self.y = random.randrange(0,windowHeight,50)
        self.width = 50
        self.height = 50
    def drawApple(self, snake):
        for i in snake:
            if self.x == i.x and self.y == i.y:
                self.x = random.randrange(0,windowWidth,50)
                self.y = random.randrange(0,windowHeight,50)
        pygame.draw.circle(win,(255,0,0), (self.x+25,self.y+25), 25)

    

windowWidth = 1000
windowHeight = 800
win = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption("Snake")

head = SnakePart(250, 250)
apple = Food()
score = 0
snake = [head]

def addPart():
    tail = snake[len(snake)-1]
    direction = tail.traveldir
    x = tail.x
    y = tail.y
    if direction == 0:
        y = y+50
    if direction == 1:
        x = x+50
    if direction == 2:
        y = y-50
    if direction == 3:
        x = x-50
    NewPart = SnakePart(x,y)
    snake.append(NewPart)
addPart()
run = True


while run:
    pygame.display.set_caption("Snake. Score = %s" %(score))
    pygame.time.delay(125)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    win.fill((0,0,0))

    #if the head of the snake is in the same cell as an apple increment the score, add a segment to the snake, and assign new coordinates to the apple
    if snake[0].x == apple.x and snake[0].y == apple.y:
            score = score + 10
            apple = Food()
            addPart()

    #control direction of snakes head using arrow keys
    if keys[pygame.K_UP] and snake[0].traveldir != 2:                   
        snake[0].traveldir = 0
    if keys[pygame.K_LEFT] and snake[0].traveldir != 3:
        snake[0].traveldir = 1
    if keys[pygame.K_DOWN] and snake[0].traveldir != 0:
        snake[0].traveldir = 2
    if keys[pygame.K_RIGHT] and snake[0].traveldir != 1:
        snake[0].traveldir = 3

    apple.drawApple(snake)
    #upadate the position of all the snake cells to be the position of the cell in front of it, moving the snake
    for i in range(len(snake)-1, 0, -1):
        snake[i].x = snake[i-1].x
        snake[i].y = snake[i-1].y
        snake[i].traveldir = snake[i-1].traveldir
        snake[i].drawSnake()

    #move the head segment of the snake in the travel direction and draw it 
    snake[0].move()
    snake[0].drawSnake()
    #check if the snake's head has colided with any of its segments 
    for i in range(1, len(snake)):
        if snake[0].x == snake[i].x and snake[0].y == snake[i].y:
            run = False
    pygame.display.update()
    
#write the score to a score file 
path = os.path.dirname(os.path.realpath(__file__))
with open(str(path) + "\scores.txt", "a", encoding= "utf-8") as f:
    f.writelines(str(score) + "\n")
    print("worte score to file")

path = os.path.dirname(os.path.realpath(__file__))
with open(str(path) + "\scores.txt", "r", encoding= "utf-8") as f:
    scorelist = f.readlines()
    for line in f:
        scorelist.append(line)

print("the high score is: " + str(max(scorelist)))
pygame.quit()