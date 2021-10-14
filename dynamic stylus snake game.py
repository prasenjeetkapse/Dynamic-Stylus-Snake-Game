import cv2 as cv
import numpy as np
import pygame
import random

img_counter = 0
H = [0, 0, 0]
p = [0, 0, 0]
c = 0

# Creating a window to position and capture the Stylus
cam = cv.VideoCapture(0)
while True:
    ret, frame = cam.read()
    frame = cv.flip(frame, 1)
    frame = cv.putText(frame, 'Position the rectangle within the Stylus', (1, 110), cv.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    frame = cv.putText(frame, 'Press ESC', (240,380), cv.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv.LINE_AA)
    cv.rectangle(frame, (315,235), (325,245), (255,255,255), 2)
    cv.imshow("Capturing Stylus", frame)
    cv.moveWindow("Capturing Stylus", 100, 100)

    k = cv.waitKey(1)
    if k % 256 == 27:
        break

# Capturing the pixels in the Region of Interest
img = frame[235:245, 315:325]
img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
# Taking the average of HSV values of those pixels
for row in range(0, 10):
    for col in range(0, 10):
        if img[row, col][0] != 0:
            H = H + img[row, col]
            c = c + 1
p = H//c

cam.release()
cv.destroyAllWindows()

cap = cv.VideoCapture(0)
xc = 0
yc = 0

pygame.init()

dis_width = 600
dis_height = 400
blue=(0,0,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
yellow=(255, 255, 102)
white=(255,255,255)
hurdel_color =(0, 200, 213)


dis=pygame.display.set_mode((dis_width,dis_height))
pygame.display.set_caption('Snake game')
clock = pygame.time.Clock()


font_style = pygame.font.SysFont("bahnschrift", 30)
score_font = pygame.font.SysFont("comicsansms", 35)


   
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def message(msg,color):
        mesg = font_style.render(msg, True, color)
        dis.blit(mesg, [50, 150])


def our_snake(snake_block, snake_list):
    for i in snake_list:
        pygame.draw.rect(dis, black, [i[0], i[1], snake_block, snake_block])

def hurdel_1():
    pygame.draw.rect(dis, hurdel_color, [100, 100, 400, 50])
    #pygame.draw.rect(dis, hurdel_color, [150, 150, 50, 50])
    #pygame.draw.rect(dis, hurdel_color, [400, 250, 50, 50])

def hurdel_2():
    pygame.draw.rect(dis, hurdel_color, [300, 100, 100, 200])
    

def hurdel_3():
    pygame.draw.rect(dis, hurdel_color, [100, 200, 300, 50])

hurdel = [hurdel_1, hurdel_2, hurdel_3]

hur=hurdel[random.randint(0,2)]


snake_block = 10
snake_speed = 10

# Capturing the centroid of the Stylus using HSV Thresholding
def game_loop():
    game_over = False
    game_close = False
    x = 0  #initial position of snake
    y = 0

    x1_change = 0       
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    
    
    while not game_over:
        while game_close == True:
            dis.fill(white)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()
 
        ret, frame = cap.read()
        frame = cv.flip(frame, 1)

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Setting the upper and lower HSV limits
        lower = np.array([p[0] - 10, p[1] - 50, p[2] - 50])
        upper = np.array([p[0] + 10, p[1] + 50, p[2] + 50])

        mask = cv.inRange(hsv, lower, upper)

        # Reducing noise in the mask image
        kernel = np.ones((11,11), np.uint8)
        closing = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)
        opening = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)
        blur = cv.GaussianBlur(opening, (5, 5), 0)

        ret1, thresh = cv.threshold(blur, 127,255,0)

        rec=cv.rectangle(frame,(200,100), (400,300), (0,255,0), 3)

        # Finding the contours of the Stylus
        contours, hierarchy = cv.findContours(thresh, 1, 2)
        cv.drawContours(mask, contours, 0, (0,255,0), 3)

        cv.imshow('Frame', frame)

        k = cv.waitKey(20) & 0xFF
        if k == 27:
            break
        
        if contours and cv.contourArea(max(contours, key = cv.contourArea)) > 800:
                    
            c = max(contours, key = cv.contourArea) 
            M= cv.moments(c)   
            xc = int(M['m10']/M['m00'])
            yc = int(M['m01']/M['m00'])
          

            #finding direction of snake
                     
            if xc>400:
                print("right")                        #xc,yc are center of stylus
                x1_change = snake_block
                y1_change = 0
            if xc<200:
                print("left")
                x1_change = -snake_block
                y1_change = 0
            if yc<100:
                print("up")
                y1_change = -snake_block
                x1_change = 0
            if yc>300:
                print("down")
                y1_change = snake_block
                x1_change = 0
            
            if x >= dis_width or x < 0 or y >= dis_height or y < 0:
                game_close = True

        #if snake head collide with hurdels then game close
        if hur==hurdel_1:
            if ((100<=x<500) and (100<=y<150)) :
                game_close = True
      
        elif hur==hurdel_2:
            if ((300<=x<400) and (100<=y<300)):
                game_close = True
       
        else :
            if ((100<=x<400) and (200<=y<250)):
                game_close = True
 
        #if food is in hurdels then draw new food 
        if hur == hurdel_1:
            while ((100<=foodx<500) and (100<=foody<150)):
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        if hur == hurdel_2:
            while ((300<=foodx<400) and (100<=foody<300)):
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        if hur == hurdel_3:
            while ((100<=x<400) and (200<=y<250)):
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        
        x += x1_change
        y += y1_change
        dis.fill(blue)

        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
       
        

        snake_Head = []
        snake_Head.append(x)
        snake_Head.append(y)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for i in snake_List[:-1]:
            if i == snake_Head:
                game_close = True
        
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)



        if x == foodx and y == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        hur()
        pygame.display.update()
        pygame.display.flip()
        clock.tick(snake_speed)

    pygame.display.update()
    pygame.quit()
    quit()                        


game_loop()