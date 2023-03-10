import pygame, sys
import numpy as np
import random
import math
from pygame.locals import *
pygame.init()
pygame.mixer.init()

#Initiates the display and the FPS
DISPLAYSURF= pygame.display.set_mode((800,600))
pygame.display.set_caption("Comets")
fpsClock=pygame.time.Clock()
FPS=60
surface_size=DISPLAYSURF.get_size()

#Color palette
WHITE = (255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
BLACK = (0,0,0)

#Loads fonts
score_font=pygame.font.SysFont('Arial',25)
title_font=pygame.font.SysFont('Arial',150)
menu_font=pygame.font.SysFont('Arial',70)
over_font=pygame.font.SysFont('Arial',150)
lb_title_font=pygame.font.SysFont('Arial',50)
lb_board_font=pygame.font.SysFont('Arial',30)


#Loads images
player_image=pygame.image.load("player.png")
bullet_image=pygame.image.load("bullet.png")

#Loads sounds
pew_sound=pygame.mixer.Sound('./Audio/Sounds/pew.mp3')
death_sound=pygame.mixer.Sound('./Audio/Sounds/death.mp3')
boom_sound=pygame.mixer.Sound('./Audio/Sounds/boom.mp3')

#Assigns hitboxes for the player and the bullets
hitbox= pygame.Rect(0,0,player_image.get_width(),player_image.get_height())
bullet_hitbox= pygame.Rect(0,0,bullet_image.get_width(),bullet_image.get_height())

#Initiates the score and player position
playerPos=(400,300)
score=0


#Plays given music and stops the previous one
def play_music(music):
    pygame.mixer.music.stop()
    music_path='./Audio/Music/'+music+'.mp3'
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)


#Only returns True if the last bullet was shot at least 1 second ago.
def shootBullet(cooldown):
    currentTime=pygame.time.get_ticks()

    if cooldown+1000>currentTime:
        return False

    else:
        return True

def moveBullet(bulletPos,direction,rotation):

            #Moves the bullet towards it's direction
            bulletPos=np.add(bulletPos,direction)

            #Moves the bullet to the other side of the screen if it were to exit the borders
            bulletPos=wrap_around(bulletPos)

            #Assigns the bullet's hitbox
            bullet_hitbox.center=bulletPos
            rect = rotation.get_rect(center=bulletPos)
            
            #Draws the bullet
            pygame.draw.rect(DISPLAYSURF,GREEN,bullet_hitbox,-1)
            DISPLAYSURF.blit(rotation,rect)

            #Returns the new position
            return bulletPos


#Function for moving object positions to the opposite side of the screen once they reach the screen borders
def wrap_around(position):
    if position[0]>800:
        position=(position[0]-800,position[1])
    elif position[0]<0:
        position=(position[0]+800,position[1])
    if position[1]>600:
        position=(position[0],position[1]-600)
    elif position[1]<0:
        position=(position[0],position[1]+600)
    
    return position


#Dictionary to store comet dimensions
cometsize={
    "large":108,
    "medium":72,
    "small":36
    }

#Dictionary to store comet destruction score bonus
cometpoints={
    "large":200,
    "medium":100,
    "small":50
}
#Maximum and minimum amount of comets onscreen
cometmax=8
cometmin=3

#List storing all Comet objects
cometlist=[]

#Class defining Comet attributes and comet-related functions
class Comet():
    #Attribute initialization
    direction=[1,1]
    speed=0
    size="large"
    hitbox=0
    points=0

    #Attribute assignment
    #   direction-initial movement direction vector (x,y)
    #   speed-initial movement speed
    #   size-comet size
    #   hitbox-stores the Rect object for the comet's hitbox
    #   points-comet destruction score bonus
    def __init__(self,center,direction,speed,size):
        self.direction=direction
        self.speed=speed
        self.size=size
        self.hitbox=pygame.Rect(center[0]-(cometsize[size]/2),center[1]-(cometsize[size]/2),cometsize[size],cometsize[size])
        self.points=cometpoints[size]
    
    #Gives the top left corner of a hitbox from its center point and comet size
    def corner(center,size):
        return [center[0]-(size/2),center[1]-(size/2)]

    #Adds a new Comet object to the cometlist list
    def spawn(center,direction,speed,size):
        cometlist.append(Comet(center,direction,speed,size))

    #Spawns the initial comets at game start
    def initial():
        for _ in range(2):
            #Checks if spawn position is far away enough from the player
            start_pos=(playerPos)
            while math.sqrt((start_pos[0]-playerPos[0])**2+(start_pos[1]-playerPos[1])**2)<200:
                start_pos=(random.randrange(surface_size[0]+1),random.randrange(surface_size[1]+1))

            start_angle=random.randrange(0,201)/100*np.pi
            direction=(np.cos(start_angle),np.sin(start_angle))
            speed=random.randrange(2,4)
            Comet.spawn(start_pos,direction,speed,"large")

    #Moves each Comet's hitbox in cometlist relative to its direction and speed        
    def move():
        for c in cometlist:
            size=cometsize[c.size]
            center=c.hitbox.center 
            
            new_center=(center[0]+(c.direction[0]*c.speed),center[1]+(c.direction[1]*c.speed))

            #Wraps back around if edge of the screen is reached 
            if new_center[0]<0:
                c.hitbox.move_ip(surface_size[0],0)
                
            elif new_center[0]>surface_size[0]:
                c.hitbox.move_ip(-1*surface_size[0],0)
                
            if new_center[1]<0:
                c.hitbox.move_ip(0,surface_size[1])
                
            elif new_center[1]>surface_size[1]:
                c.hitbox.move_ip(0,-1*surface_size[1])
                
            
            c.hitbox.move_ip((c.direction[0]*c.speed),(c.direction[1]*c.speed))

    #Draws each Comet  the game screen according to its hitbox's position
    def draw():
        for c in cometlist:
            pygame.draw.circle(DISPLAYSURF,WHITE,c.hitbox.center,cometsize[c.size]/2)


    #Deletes destroyed Comets and spawns smaller ones with random direction and same speed as the original
    def split(list_pos):
        #Deletes Comet from cometlist and keeps it stored in blown variable
        blown=cometlist.pop(list_pos)
        split_max=cometmax-len(cometlist)
        #Destroys large Comets and creates medium ones
        if blown.size=="large":
            start_pos=Comet.corner(blown.hitbox.center,cometsize[blown.size])
            speed=blown.speed
            
            #Creates a list of used angles
            angle_list=[]
            for _ in range (min(3,split_max)):
                start_angle=100
                #Creates non-repeated angles
                while start_angle in angle_list:
                    start_angle=random.randrange(0,9)/4*np.pi
                angle_list.append(start_angle)
                direction=(np.cos(start_angle),np.sin(start_angle))
                
                Comet.spawn(start_pos,direction,speed,"medium")
        #Destroys medium Comets and creates small ones
        elif blown.size=="medium":
            start_pos=Comet.corner(blown.hitbox.center,cometsize[blown.size])
            speed=blown.speed

            #Creates a list of used angles
            angle_list=[100]
            for _ in range (min(5,split_max)):
                start_angle=100
                #Creates non-repeated angles
                while start_angle in angle_list:
                    start_angle=random.randrange(0,9)/4*np.pi
                angle_list.append(start_angle) 
                direction=(np.cos(start_angle),np.sin(start_angle))
                
                Comet.spawn(start_pos,direction,speed,"small")

        #Spawns a large comet if the destroyed Comet brought the n?? of comets onscreen lower than cometmin
        elif len(cometlist)<cometmin:
            start_pos=(playerPos)
            while math.sqrt((start_pos[0]-playerPos[0])**2+(start_pos[1]-playerPos[1]))**2<200:
                start_pos=(random.randrange(surface_size[0]+1),random.randrange(surface_size[1]+1))

            start_angle=random.randrange(0,201)/100*np.pi
            direction=(np.cos(start_angle),np.sin(start_angle))
            speed=random.randrange(2,4)
            Comet.spawn(start_pos,direction,speed,"large") 



#Main game loop
def gameloop():

    #Calls the Comet variables and class
    global cometlist
    global cometmax
    global cometmin
    Comet.initial()

    #Calls the score and resets it
    global score
    score=0
    #Initiates a variable for survival score awards
    lastScore=0

    #Initiates a variable for increasing difficulty over time
    difficultyIncrease=0

    #Initiates the movement variables and the spawn point
    ang=0
    global playerPos
    playerPos=(400,300)
    accel=0
    propulsion=(0,0)

    #Initiates all variables for each of the bullets
    bulletCooldownMain=0
    bulletCooldown1=0
    bulletCooldown2=0
    bulletCooldown3=0
    bulletCooldown4=0

    shot1=False
    shot2=False
    shot3=False
    shot4=False

    spawnAssigned1=False
    spawnAssigned2=False
    spawnAssigned3=False
    spawnAssigned4=False

    #Displays the controls for a short while before starting the game
    DISPLAYSURF.fill(BLACK)

    tutorial_movement1=lb_board_font.render("UP to thrust forward",True,WHITE)

    DISPLAYSURF.blit(tutorial_movement1,(250,150))

    tutorial_movement2=lb_board_font.render("LEFT and RIGHT to turn",True,WHITE)
    DISPLAYSURF.blit(tutorial_movement2,(250,250))

    tutorial_shoot=lb_board_font.render("SPACEBAR to shoot",True,WHITE)
    DISPLAYSURF.blit(tutorial_shoot,(250,350))


    pygame.display.update()
    pygame.time.wait(2500)

    #Starts playing music
    play_music("game_music")

    game=True
    while game:

        #Adds the propulsion value to the current position of the player
        playerPos=np.add(propulsion,playerPos)

        #Moves the player to the opposite side of the screen if they were to exit the borders
        playerPos=wrap_around(playerPos)

        #Assigns the front of the spaceship (where the player is facing)
        front_x= playerPos[0]+ math.cos((ang-90)*(np.pi)/180)*(player_image.get_width()/2)
        front_y= playerPos[1]+ math.sin((ang-90)*(np.pi)/180)*(player_image.get_height()/2)
        frontPoint=(front_x,front_y)

        #Fills the screen black and draws the player according to their position and rotation.
        DISPLAYSURF.fill(BLACK)
        rotimage = pygame.transform.rotate(player_image,-ang)
        rect = rotimage.get_rect(center=playerPos)
        DISPLAYSURF.blit(rotimage,rect)


        #Assigns the hitbox to the player
        hitbox.center=playerPos
        pygame.draw.rect(DISPLAYSURF,GREEN,hitbox,-1)
        
        #Updates the Comet positions, then draws them
        Comet.move()
        Comet.draw()

        #Detects if the player presses the "X" button on the window, and closes the game if they do
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #Checks if the player is pressing any key
        keys = pygame.key.get_pressed()

        #Left and Right arrow keys rotate the player in the respective direction
        if keys[pygame.K_LEFT]:

            ang-=2
            
        if keys[pygame.K_RIGHT]:

            ang+=2

        #Up arrow key accelerates and creates propulsion for the ship, which is used to move the player
        if keys[pygame.K_UP]:

            #Consistently accelerates every loop up to 10 times
            accel+=0.01
            if accel>0.1:
                accel=0.1
            
            #Calculates where the player is facing and multiplies the acceleration by the unit vectors
            player_distance=np.subtract(frontPoint,playerPos)
            player_norm=math.sqrt(player_distance[0]**2 + player_distance[1]**2)
            player_direction=np.divide(player_distance,player_norm)*accel


            #Adds the calculated force of the direction to the propulsion every loop
            propulsion=np.add(player_direction,propulsion)

            #Caps the propulsion at 5 for each direction to prevent the player from getting too fast
            if propulsion[0]>5:
                propulsion[0]=5
            elif propulsion[0]<-5:
                propulsion[0]=-5
            
            if propulsion[1]>5:
                propulsion[1]=5
            elif propulsion[1]<-5:
                propulsion[1]=-5


        #Acceleration resets to 0 if the player stops pressing the key
        else:
            accel=0

        #Spacebar shoots one of the four bullets depending on which ones are still "alive" in the game
        if keys[pygame.K_SPACE]:


            #If the first bullet isn't "alive"
            if not shot1: 

                #Checks if the shooting cooldown has passed
                shot1=shootBullet(bulletCooldownMain)

                #Assigns an individual cooldown to the bullet, used for checking how long they have been "alive"
                bulletCooldown1=pygame.time.get_ticks()

                #If the bullet was shot, resets the shooting cooldown and plays a sound
                if shot1:
                    bulletCooldownMain=pygame.time.get_ticks()
                    pygame.mixer.Sound.play(pew_sound)


            #If the second bullet isn't "alive"
            elif not shot2:

                #Checks if the shooting cooldown has passed
                shot2=shootBullet(bulletCooldownMain)

                #Assigns an individual cooldown to the bullet, used for checking how long they have been "alive"
                bulletCooldown2=pygame.time.get_ticks()

                #If the bullet was shot, resets the shooting cooldown and plays a sound
                if shot2:
                    bulletCooldownMain=pygame.time.get_ticks()
                    pygame.mixer.Sound.play(pew_sound)


            #If the third bullet isn't "alive"
            elif not shot3:

                #Checks if the shooting cooldown has passed
                shot3=shootBullet(bulletCooldownMain)

                #Assigns an individual cooldown to the bullet, used for checking how long they have been "alive"
                bulletCooldown3=pygame.time.get_ticks()

                #If the bullet was shot, resets the shooting cooldown and plays a sound
                if shot3:
                    bulletCooldownMain=pygame.time.get_ticks()
                    pygame.mixer.Sound.play(pew_sound)


            #If the fourth bullet isn't "alive"
            elif not shot4:

                #Checks if the shooting cooldown has passed
                shot4=shootBullet(bulletCooldownMain)

                #Assigns an individual cooldown to the bullet, used for checking how long they have been "alive"
                bulletCooldown4=pygame.time.get_ticks()

                #If the bullet was shot, resets the shooting cooldown and plays a sound
                if shot4:
                    bulletCooldownMain=pygame.time.get_ticks()
                    pygame.mixer.Sound.play(pew_sound)


        #Escape key also closes the game
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        #Gives 10 points of score every 2 seconds the player is alive
        if lastScore+2000<=pygame.time.get_ticks():
            lastScore=pygame.time.get_ticks()
            score+=10


        #Increases the minimum and maximum amount of comets every 15 seconds
        if difficultyIncrease+15000<=pygame.time.get_ticks():
            difficultyIncrease=pygame.time.get_ticks()
            cometmax+=2
            cometmin+=2


        #Detects if the first bullet is "alive"
        if shot1:
            killBullet=False

            #Assigns position, direction and rotation values the first time the bullet is detected
            while not spawnAssigned1:

                bulletPos1=frontPoint

                distance1=np.subtract(bulletPos1,playerPos)
                norm1=math.sqrt(distance1[0]**2 + distance1[1]**2)
                direction1=np.divide(distance1,norm1)*8
                rotation1 = pygame.transform.rotate(bullet_image,-ang)

                #Completes the value assignment
                spawnAssigned1=True

            bulletPos1=moveBullet(bulletPos1,direction1,rotation1)

            #Checks all Comet hitboxes for collision
            for i in range(len(cometlist)):

                #If a collision is detected, "kills" the bullet, adds score, and splits the respective comet
                if bullet_hitbox.colliderect(cometlist[i].hitbox):
                    killBullet=True
                    score+=cometlist[i].points
                    pygame.mixer.Sound.play(boom_sound)
                    Comet.split(i)
                    break
                    
            #"Kills" the bullet if it has been shot over 4 seconds ago
            if bulletCooldown1+4000<=pygame.time.get_ticks():
                killBullet=True

            #If the bullet is "killed", marks the bullet as unassigned and not "alive" until it's shot again
            if killBullet:
                shot1=False
                spawnAssigned1=False

        #Detects if the second bullet is "alive"
        if shot2:
            killBullet=False

            #Assigns position, direction and rotation values the first time the bullet is detected
            while not spawnAssigned2:

                bulletPos2=frontPoint

                distance2=np.subtract(bulletPos2,playerPos)
                norm2=math.sqrt(distance2[0]**2 + distance2[1]**2)
                direction2=np.divide(distance2,norm2)*8
                rotation2 = pygame.transform.rotate(bullet_image,-ang)

                #Completes the value assignment
                spawnAssigned2=True

            bulletPos2=moveBullet(bulletPos2,direction2,rotation2)

            #Checks all Comet hitboxes for collision
            for i in range(len(cometlist)):

                #If a collision is detected, "kills" the bullet, adds score, and splits the respective comet
                if bullet_hitbox.colliderect(cometlist[i].hitbox):
                    killBullet=True
                    score+=cometlist[i].points
                    pygame.mixer.Sound.play(boom_sound)
                    Comet.split(i)
                    break
                    
            #"Kills" the bullet if it has been shot over 4 seconds ago       
            if bulletCooldown2+4000<=pygame.time.get_ticks():
                killBullet=True

            #If the bullet is "killed", marks the bullet as unassigned and not "alive" until it's shot again
            if killBullet:
                shot2=False
                spawnAssigned2=False

        #Detects if the third bullet is "alive"
        if shot3:
            killBullet=False

            #Assigns position, direction and rotation values the first time the bullet is detected
            while not spawnAssigned3:

                bulletPos3=frontPoint

                distance3=np.subtract(bulletPos3,playerPos)
                norm3=math.sqrt(distance3[0]**2 + distance3[1]**2)
                direction3=np.divide(distance3,norm3)*8
                rotation3 = pygame.transform.rotate(bullet_image,-ang)
                
                #Completes the value assignment
                spawnAssigned3=True

            bulletPos3=moveBullet(bulletPos3,direction3,rotation3)

            #Checks all Comet hitboxes for collision
            for i in range(len(cometlist)):

                #If a collision is detected, "kills" the bullet, adds score, and splits the respective comet
                if bullet_hitbox.colliderect(cometlist[i].hitbox):
                    killBullet=True
                    score+=cometlist[i].points
                    pygame.mixer.Sound.play(boom_sound)
                    Comet.split(i)
                    break

            #"Kills" the bullet if it has been shot over 4 seconds ago        
            if bulletCooldown3+4000<=pygame.time.get_ticks():
                killBullet=True

            #If the bullet is "killed", marks the bullet as unassigned and not "alive" until it's shot again
            if killBullet:
                shot3=False
                spawnAssigned3=False

        #Detects if the fourth bullet is "alive"
        if shot4:
            killBullet=False

            #Assigns position, direction and rotation values the first time the bullet is detected
            while not spawnAssigned4:

                bulletPos4=frontPoint

                distance4=np.subtract(bulletPos4,playerPos)
                norm4=math.sqrt(distance4[0]**2 + distance4[1]**2)
                direction4=np.divide(distance4,norm4)*8
                rotation4 = pygame.transform.rotate(bullet_image,-ang)
                
                #Completes the value assignment
                spawnAssigned4=True

            bulletPos4=moveBullet(bulletPos4,direction4,rotation4)

            #Checks all Comet hitboxes for collision
            for i in range(len(cometlist)):

                #If a collision is detected, "kills" the bullet, adds score, and splits the respective comet
                if bullet_hitbox.colliderect(cometlist[i].hitbox):
                    killBullet=True
                    score+=cometlist[i].points
                    pygame.mixer.Sound.play(boom_sound)
                    Comet.split(i)
                    break

            #"Kills" the bullet if it has been shot over 4 seconds ago
            if bulletCooldown4+4000<=pygame.time.get_ticks():
                killBullet=True

            #If the bullet is "killed", marks the bullet as unassigned and not "alive" until it's shot again
            if killBullet:
                shot4=False
                spawnAssigned4=False




        #Caps the score at 9999
        if score>9999:
            score=9999

        #Assigns an arcade-like display of the score
        if score<10:
            score_string="Score: "+"000"+str(score)
            score_display=score_font.render(score_string,True,WHITE)

        elif score<100:
            score_string="Score: "+"00"+str(score)
            score_display=score_font.render(score_string,True,WHITE)

        elif score <1000:
            score_string="Score: "+"0"+str(score)
            score_display=score_font.render(score_string,True,WHITE)

        elif score <9999:
            score_string="Score: "+str(score)
            score_display=score_font.render(score_string,True,WHITE)

        else:
            score_string="Score: "+str(score)
            score_display=score_font.render(score_string,True,RED)

        DISPLAYSURF.blit(score_display,(675,25))


        #Checks all Comet hitboxes for collision with the player
        for c in range(len(cometlist)):

            #If a collision is detected:
            if hitbox.colliderect(cometlist[c].hitbox):

                #Draws which hitboxes collided
                pygame.draw.rect(DISPLAYSURF,RED,hitbox,5)
                pygame.draw.rect(DISPLAYSURF,RED,cometlist[c].hitbox,5)
                pygame.display.update()

                #Plays a death sound and stops the music
                pygame.mixer.Sound.play(death_sound)
                pygame.mixer.music.stop()

                #Delays for one second so the player can see what happened
                pygame.time.wait(1000)

                #Changes the loop variable to False to end the loop
                game=False
                break
                


        pygame.display.update()
        fpsClock.tick(FPS)
    

    #Triggers the game over screen and leaderboard
    gameover()

#Start screen loop
def title():
    #Defines the text to be displayed onscreen
    text_title=title_font.render("COMETS",True,WHITE)
    rect_title=text_title.get_rect()
    rect_title.center=(surface_size[0]/2,surface_size[1]/5)

    text_start=menu_font.render("START",True,WHITE)
    rect_start=text_start.get_rect()
    rect_start.center=(surface_size[0]/2,surface_size[1]/2)

    text_quit=menu_font.render("QUIT",True,WHITE)
    rect_quit=text_quit.get_rect()
    rect_quit.center=(surface_size[0]/2,surface_size[1]/1.5)

    #Menu cursor attributes initialization
    cursor=1
    img_cursor=pygame.transform.rotate(player_image,-90)
    rect_cursor=img_cursor.get_rect()
    pos_cursor=[surface_size[0]/3,rect_start.center[1]] 

    #Plays the menu music
    play_music("menu_music")

    #Title screen loop
    title=True
    while title:
        #Draws text onscreen
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(text_title,rect_title)
        DISPLAYSURF.blit(text_start,rect_start)
        DISPLAYSURF.blit(text_quit,rect_quit)


        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            #Keyboard input handler
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    cursor=1
                    pos_cursor[1]=rect_start.center[1]
                if event.key==pygame.K_DOWN:
                    cursor=2
                    pos_cursor[1]=rect_quit.center[1]
                if event.key==pygame.K_SPACE:
                    if cursor==1:
                        #Starts main game loop                       
                        gameloop()
                    else:
                        #Quits game
                        pygame.quit()
                        sys.exit()

        #Moves cursor position
        rect_cursor.center=(pos_cursor)
        #Draws cursor onscreen
        DISPLAYSURF.blit(img_cursor,rect_cursor)

        pygame.display.update() 
        fpsClock.tick(FPS)


#Game Over and Leaderboard loops
def gameover():
    global cometlist
    cometlist=[]

    #Gets time at beginning of Game Over screen
    screen_start=pygame.time.get_ticks()
    screen_time=0
    #Plays Game Over screen for 2 seconds
    while screen_time<2000:
        #Draws Game Over text onscreen
        text_over=over_font.render("GAME OVER",True,WHITE)
        rect_over=text_over.get_rect()
        rect_over.center=(surface_size[0]/2,surface_size[1]/2)
        DISPLAYSURF.fill(BLACK)
        DISPLAYSURF.blit(text_over,rect_over)
        
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)
        #Tracks time elapsed since beginning of Game Over screen
        screen_time=pygame.time.get_ticks()-screen_start
   
    #Leaderboard section

    
    #Opens txt file to read saved highscores
    leaderboard=open("leaderboard.txt","r")
    lb_list=[]
    
    #Creates list of saved highscores
    for line in leaderboard:
        lb_list.append(line.strip())

    #Closes opened txt file
    leaderboard.close()

    #Defines Leaderboard title text to be displayed
    text_lb_title=lb_title_font.render("Leaderboard",True,WHITE)
    rect_lb_title=text_lb_title.get_rect()
    rect_lb_title.center=(surface_size[0]/2,surface_size[1]/12)

    #Checks if player achieved a highscore; If so, inserts it into lb_list in the correct position
    inp=20
    for l in range(len(lb_list)):
        if score>=int(lb_list[l][4:8]):
            score_str="0"*(4-len(str(score)))+str(score)
            lb_list.insert(l,"___-"+score_str)
            del lb_list[-1]
            inp=l
            
            break
    
    #Defines Leaderboard score text to be displayed
    text_lb_board=[]
    rect_lb_board=[]
    offset=2        
    for l in range(len(lb_list)):
        text_lb_board.append(lb_board_font.render(lb_list[l],True,WHITE))
        rect_lb_board.append(text_lb_board[l].get_rect())
        rect_lb_board[l].center=(surface_size[0]/2,surface_size[1]/12*(l+2))
        offset=offset+1

    #plays Leaderboard screen music
    play_music("leaderboard_music")

    
    if inp==20:
        screen_start=pygame.time.get_ticks()
        screen_time=0

        #No Highscore achived loop (hangs for 6 seconds)
        while screen_time<6000:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()

            #Draws Leaderboard score text onscreen    
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(text_lb_title,rect_lb_title)
            for l in range(len(rect_lb_board)):
                DISPLAYSURF.blit(text_lb_board[l],rect_lb_board[l])
            
            pygame.display.update()
            fpsClock.tick(FPS)
            screen_time=pygame.time.get_ticks()-screen_start

    else:
        inp_count=0
        name=""

        #Highscore achived loop (hangs for 1 second after name entry)

        #Only accepts input of 3 characters
        while inp_count<3:
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                #Text input handler
                if event.type==pygame.KEYDOWN:
                    #Only accepts characters
                    if event.unicode!="":
                        #Adds inputted character to name
                        name=name+event.unicode

                        #Defines player name and score to be displayed, even mid-input
                        text=name+"-"+("0"*(4-len(str(score))))+str(score)

                        #Defines text to be displayed onscreen
                        text_lb_board[inp]=lb_board_font.render(text,True,WHITE)
                        rect_lb_board[inp]=text_lb_board[inp].get_rect()
                        rect_lb_board[inp].center=(surface_size[0]/2,surface_size[1]/12*(inp+2))

                        inp_count=inp_count+1

            #Draws Leaderboard score text onscreen
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF.blit(text_lb_title,rect_lb_title)
            for l in range(len(rect_lb_board)):
               DISPLAYSURF.blit(text_lb_board[l],rect_lb_board[l])
                
                    
            pygame.display.update()
            fpsClock.tick(FPS)
        
        #Updates score list with player name
        lb_list[inp]=text

        #Reopens txt file to record new highscores
        leaderboard=open("leaderboard.txt","w")

        #Writes scores into txt file
        for line in lb_list:
            line=line+"\n"
            leaderboard.write(line)

        #Hangs for 1 second
        pygame.time.wait(1000)

#Game start
title()