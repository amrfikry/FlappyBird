from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import numpy as np
import pygame
from pygame import mixer
import time
import sys 
import os 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
FlabbyObjects = list()  #A List To Store Every Object of The Game At 

class GameObject:
    def __init__(self):
        self.IntPos = [0, 0, 0] #If No Position Is Given , Set To The Origin
        self.position = [0, 0, 0]  # GameObject's Position And Returning The Position
        self.scale = [0, 0, 0]  # GameObject's Scale
       
        global FlabbyObjects
        FlabbyObjects.append(self)  #Append The Given Object

    def setPos(self, PosList):  #To Set The Object To The Given Position in PosList
        self.position = PosList

    def getPos(self): #Return The Object's Position
        return self.position

    def setScale(self, ScaleList): #To Scale The Object in x ,y and z 
        self.scale = ScaleList
        glScale(self.scale[0], self.scale[1], self.scale[2])

    def getScale(self): #Return The Scale Used In DrawImage function in Image Renderer Class
        return self.scale

    def ApplyInitailPostion(self): #Translate The Object To A Specied Position
        glTranslate(self.IntPos[0], self.IntPos[1] * 2, self.IntPos[2])

    def StartingTransformation(self, PosList=[0, 0, 0], ScaleList=[1, 1, 1]): ### The Most Important Function For Set The Transformations on the Object

        self.scale = ScaleList
        glScale(ScaleList[0], ScaleList[1], ScaleList[2])
        self.setPos(PosList)
        self.IntPos = PosList
        

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class FlappyImages:
    def __init__(self, MyImages):
        self.AppliedImage = 0  #Select only one texture from the list
        self.imageCount = 0  
        self.imageCount=len(MyImages)  #the number of textures used in the game

        self.images = glGenTextures(self.imageCount) #To generate the textures
        i = 0
        for ID in MyImages:  #to Set and wrap every image in MyImages list 
            imgload = pygame.image.load(ID)
            img = pygame.image.tostring(imgload, "RGBA", 1)
            width = imgload.get_width()
            height = imgload.get_height()
            glBindTexture(GL_TEXTURE_2D, self.images[i])  # Set this image in images array
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
            i += 1
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.images[0])

    def ApplyImage(self, CurrentImage=1):  #to Select the applied image at a time
        self.AppliedImage = CurrentImage
        glBindTexture(GL_TEXTURE_2D, self.images[self.AppliedImage - 1])


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class ImageRenderer:
    def __init__(self, MyObject):
        self.gameObject = MyObject
        self.texCoordX1 = 0
        self.texCoordX2 = 0
        self.texCoordY1 = 0
        self.texCoordY2 = 0        
    # Draws Sprite every frame. Sprite is determined using 4 Coordinates from the main sprite sheet.
    def DrawImage(self, TextureCoordX1=0, TextureCoordX2=0, TextureCoordY1=0, TextureCoordY2=0):
        curGameObject = self.gameObject
        self.gameObject.ApplyInitailPostion()
        self.texCoordX1 = TextureCoordX1
        self.texCoordX2 = TextureCoordX2
        self.texCoordY1 = TextureCoordY1
        self.texCoordY2 = TextureCoordY2
        self.IntialScale = 0.05
        
        glBegin(GL_QUADS)
        glTexCoord(self.texCoordX1,self.texCoordY1)
        glVertex((-self.IntialScale * self.gameObject.getScale()[0]),
                 (-self.IntialScale) * self.gameObject.getScale()[1])

        glTexCoord(self.texCoordX2,self.texCoordY1)
        glVertex(((self.IntialScale) * self.gameObject.getScale()[0]),
                 (-self.IntialScale) * self.gameObject.getScale()[1])

        glTexCoord(self.texCoordX2,self.texCoordY2)
        glVertex(((self.IntialScale) * self.gameObject.getScale()[0]),
                 (self.IntialScale) * self.gameObject.getScale()[1])

        glTexCoord(self.texCoordX1,self.texCoordY2)
        glVertex(((-self.IntialScale) * self.gameObject.getScale()[0]),
                 (self.IntialScale) * self.gameObject.getScale()[1])

        glEnd()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
WINDOW_HEIGHT = 800
WINDOW_WIDTH = 600
gameImages = None
numberImages = None
global anim , v_velocity , dtime , y
anim = 0                                            #if anim = 0 wether the user lost or has't started game yet
y = 0
sound_button = None
sound_die = None
sound_hit = None
sound_point = None
sound_swag=None
sound_mario=None
sound_credits = None
sound_suck = None
sound_win = None
sound_damn =None
sound_sweetie = None
CountScore=0  #The Score Counter
SoundPlayed = False #To Play The Lose Tone Only Once
Tapped = False #Flag used to hide the Tap Texture After The Key Is Pressed
speedX=0 #Intialing The Pipes Speed
PipesRandom = True #A Flag Used To Stop The Random Generation Of The Pipes Everytime The Main Is Called
pipes=list()  #Used To Store The yTranslate Of Each Pipe
randomBackground=None #A Flag Used To Stop The Random Generation Of The BackGround
randomBird = None      #Same For The Bird
randomGround = None     #Same For The Ground 
time =1000
FPS = 60
Easy = False
Hard = False
xMouse = 0
yMouse = 0
pointer =0     #Points at The y's Of The Pipes in pipes List
selectedpipe=19 #To Get The Real X's for Each Pipe
increase =False #A Flag Used To Increase The Counter Only Once
PointerInc=False #A Flag To Increase The Pointer And Decrease The Selected Pipe
dtime = .0005
v_velocity = .005
SwagCheck = False  #To Check If you deserve the SWAGGGGGG
BG=False #A Flag to generate the Backgrounds, birds and grounds only once
Stop = False
Clicked = False
SwagSong=False
MarioSong = False
CreditsSong = False
YouSuck = False
SoundDamn = False
SoundSweetie = False 
FireballSound = 0
CreditsSpeed = -1.25
speedY=0
Realx = 0.0
Realy = 0.0
CreditsEnable = False
Exit = False
ballY=[.65,-.65,.5,-.5,.35,-.35,.2,-.2]
ballmovements = [0,0,0,0,0,0,0,0]
balls=[]
PosY=[]
PassedMario = False
#---------------------------------------------------------Making Everything Game Object--------------------------------------------------------------------------------------#
background = GameObject()
backgroundRenderer = ImageRenderer(background)

bird = GameObject()
birdRenderer = ImageRenderer(bird)

ground = GameObject()
groundSprite = ImageRenderer(ground)

LowerPipe = GameObject()
LowerPipeRenderer = ImageRenderer(LowerPipe)

UpperPipe = GameObject()
UpperPipeRenderer = ImageRenderer(UpperPipe)

flappy = GameObject()
flappyRenderer = ImageRenderer(flappy)

ShowScoreBoard = GameObject()
ScoreBoardRenderer = ImageRenderer(ShowScoreBoard)

GameOver = GameObject()
GameOverRenderer = ImageRenderer(GameOver)

TapToPlay = GameObject()
TapRenderer = ImageRenderer(TapToPlay)

Medals = GameObject()
MedalsRenderer = ImageRenderer(Medals)

PrintScore = GameObject()
ShowScoreRenderer = ImageRenderer(PrintScore)

Modes = GameObject()
ModesRenderer = ImageRenderer(Modes)

ball = GameObject()
showBall = ImageRenderer(ball)

SuperMario = GameObject()
SuperMarioRender = ImageRenderer(SuperMario)


Credits = GameObject()
CreditsRendderer = ImageRenderer(Credits)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def init():

    glClearColor(1,1,1,1)

    global gameImages, numberImages
    global sound_button
    global sound_die
    global sound_hit
    global sound_point
    global sound_swag
    global sound_mario
    global sound_credits
    global sound_suck
    global sound_win
    global sound_sweetie
    global sound_damn


    pygame.init() #Applying the Sounds imported in the folder 
    sound_button=pygame.mixer.Sound("sounds//wing.wav")
    sound_point=pygame.mixer.Sound("sounds//point.wav")
    sound_hit=pygame.mixer.Sound("sounds//hit.wav")
    sound_die=pygame.mixer.Sound("sounds//die.wav")
    sound_swag=pygame.mixer.Sound("sounds//Swag.wav")
    sound_mario=pygame.mixer.Sound("sounds//mario.wav")
    sound_credits=pygame.mixer.Sound("sounds//credits.wav")
    sound_suck=pygame.mixer.Sound("sounds//youSuck.wav")
    sound_win = pygame.mixer.Sound("sounds//champions.wav")
    sound_sweetie = pygame.mixer.Sound("sounds//sweetie.wav")
    sound_damn = pygame.mixer.Sound("sounds//Damn.wav")


    glMatrixMode(GL_MODELVIEW)
    #Applying Nedded Images For The Game 
    gameImages = FlappyImages(["assests//background.png","assests//Nums n Medals.png"
                            ,"assests//birds.png","assests//credits.png"
                            ,"assests//ground.png","assests//pipes.png"
                            ,"assests//flappy.png","assests//youend.png"
                            ,"assests//modes.png","assests//ball and check.png","assests//Mario.png"])
#####-----------------------------------------------------------Setting The Intail Transformation For Each Object"-----------------------------------------------------------#######

    background.StartingTransformation([0,0,0],[20,20,1])
    glLoadIdentity()


    ground.StartingTransformation([0,-0.48,0],[20,5,1])
    glLoadIdentity()

    TapToPlay.StartingTransformation([0,0,0],[9,6.5,1])
    glLoadIdentity()

    

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def showScore():
    global CountScore, numberImages,anim,SoundDamn,SoundSweetie,MarioSong,SwagCheck,SwagSong
    
    if anim == 1: #Shows The Score After The Key Is Pressed And The Game Moves
        PrintScore.StartingTransformation([0,0.4,0],[2,1.5,1])
        glLoadIdentity()

###--------------------------------------------------------------------Score Conditions To Select Which Texture To Show---------------------------------------------------------------------------------------###

    gameImages.ApplyImage(2)
    if CountScore == 0:
        ShowScoreRenderer.DrawImage(0, 0.2, 0.8, 1)  # Print The Current Score
    elif CountScore == 1:
        ShowScoreRenderer.DrawImage(0.2, 0.4, 0.8, 1)
    elif CountScore == 2:
        ShowScoreRenderer.DrawImage(0.4, 0.6, 0.8, 1)
    elif CountScore == 3:
        ShowScoreRenderer.DrawImage(0.6, 0.8, 0.8, 1)
    elif CountScore == 4:
        ShowScoreRenderer.DrawImage(0.8, 1, 0.8, 1)
    elif CountScore == 5:
        ShowScoreRenderer.DrawImage(0, 0.2, 0.6, 0.8)
        if not SoundDamn:
            pygame.mixer.Sound.play(sound_damn)
            SoundDamn = True 
        
    elif CountScore == 6:
        ShowScoreRenderer.DrawImage(0.2, 0.4, 0.6, 0.8)
    elif CountScore == 7:
        ShowScoreRenderer.DrawImage(0.4, 0.6, 0.6, 0.8)
    elif CountScore == 8:
        ShowScoreRenderer.DrawImage(0.6, 0.8, 0.6, 0.8)
    elif CountScore == 9:
        ShowScoreRenderer.DrawImage(0.8, 1, 0.6, 0.8)
    elif CountScore == 10:
        ShowScoreRenderer.DrawImage(0, 0.2, 0.4, 0.6)
        if not SoundSweetie:
            pygame.mixer.Sound.play(sound_sweetie)
            SoundSweetie = True
    elif CountScore == 11:
        ShowScoreRenderer.DrawImage(0.2, 0.4, 0.4, 0.6)
    elif CountScore == 12:
        ShowScoreRenderer.DrawImage(0.4, 0.6, 0.4, 0.6)
    elif CountScore == 13:
        ShowScoreRenderer.DrawImage(0.6, 0.8, 0.4, 0.6)
    elif CountScore == 14:
        ShowScoreRenderer.DrawImage(0.8, 1, 0.4, 0.6)
    elif CountScore == 15:
        ShowScoreRenderer.DrawImage(0, 0.2, 0.2, 0.4)
        SwagCheck=True
        if not SwagSong:
            pygame.mixer.Sound.play(sound_swag)
            SwagSong=True 
    elif CountScore == 16:
        ShowScoreRenderer.DrawImage(0.2, 0.4, 0.2, 0.4)
    elif CountScore == 17:
        ShowScoreRenderer.DrawImage(0.4, 0.6, 0.2, 0.4)
    elif CountScore == 18:
        ShowScoreRenderer.DrawImage(0.6, 0.8, 0.2, 0.4)
    elif CountScore == 19:
        ShowScoreRenderer.DrawImage(0.8, 1, 0.2, 0.4)
        if not MarioSong :
             pygame.mixer.Sound.play(sound_mario)
             MarioSong = True
    elif CountScore == 20:
        ShowScoreRenderer.DrawImage(0, 0.2, 0, 0.2)



def ShowCredits():
    global CreditsSpeed,CreditsEnable,Exit,sound_credits,CreditsSong   
    if not CreditsSong:
        pygame.mixer.Sound.play(sound_credits)
        CreditsSong=True
    

    if CreditsEnable  :
        
        background.StartingTransformation([0,0,0],[20,20,0])
        glLoadIdentity()
        gameImages.ApplyImage(1)

        if randomBackground==1:
            gameImages.ApplyImage(1) #Draw The Selected Background
            backgroundRenderer.DrawImage(0,.5,0,1)
            glLoadIdentity()
        elif randomBackground==2:
            gameImages.ApplyImage(1) #Draw The Selected Background
            backgroundRenderer.DrawImage(.5,1,0,1)
            glLoadIdentity()

        Credits.StartingTransformation([0,CreditsSpeed,0],[18,25,1])
        glLoadIdentity()

        gameImages.ApplyImage(4)
        CreditsRendderer.DrawImage(0,1,0,1)

        if CreditsSpeed > 1.25:
            sys.exit()

def ScoreEffects():
    global Tapped , CountScore,YouSuck, Clicked,Exit,sound_suck,SoundDamn,SoundSweetie

    Tapped = True #Used For Not Showing The Tap Texture After Losing 

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    ShowScoreBoard.StartingTransformation([0,0,0],[18,20,1]) #If Lost Then Show The ScoreBoard 
    glLoadIdentity()

    gameImages.ApplyImage(8)
    if CountScore == 20:
        ScoreBoardRenderer.DrawImage(0.5,1,0,1) #Draw The ScoreBoard
    else:
        ScoreBoardRenderer.DrawImage(0,0.5,0,1)
    glLoadIdentity()

    if CountScore == 0 :
        if not YouSuck:
            pygame.mixer.Sound.play(sound_suck) 
            YouSuck = True

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    Medals.StartingTransformation([-0.37,0,0],[4,3.5,1])
    glLoadIdentity()
    #To Select Which Medal The Play Occupy Depending on The Current Score 
    gameImages.ApplyImage(2)
    if CountScore > 0 and CountScore <= 5:
        MedalsRenderer.DrawImage(0.2,0.4,0,0.2)
    if CountScore > 5 and CountScore <= 10:
        MedalsRenderer.DrawImage(0.8,1,0,0.2)
    if CountScore > 10 and CountScore <= 15:
        MedalsRenderer.DrawImage(0.6,0.8,0,0.2)
    if CountScore > 15 and CountScore <= 20:
        MedalsRenderer.DrawImage(0.4,0.6,0,0.2)
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
    PrintScore.StartingTransformation([0.41,0.01,0],[2,1.5,1]) #To Print The Score At The ScoreBoard
    glLoadIdentity()

    
    showScore() #Function Used to Show The Score 
    
    if Exit :
        sys.exit()

#------------------------------------------------------A Function Used To Draw And Move The Pipes With A Specified Speed---------------------------------------------------------#
def drawPipes(xTranslate = 0, yTranslate = 0):
    #yTranslate is Used For Setting The Height OF The Pipes Randomly 
    global speedX , anim
    if anim == 0 : #While Key Is Not Pressed , No Animation And Set The Speed To Zero 
        speedX = 0
        LowerPipe.StartingTransformation([1.2, -.4, 0], [7, 14, 1])
        glLoadIdentity()
        UpperPipe.StartingTransformation([1.2 , .5, 0], [7, 14, 1])
        glLoadIdentity()
    if anim == 1 :#If Key Is Pressed ,Start Applying The Speed To The X's Of The Pipes 
        LowerPipe.StartingTransformation([(1.2+ xTranslate) -speedX, -0.4 + yTranslate, 0],[7,14,1])
        glLoadIdentity()

        UpperPipe.StartingTransformation([(1.2+ xTranslate) -speedX, 0.5 + yTranslate, 0],[7,14,1])
        glLoadIdentity()
#Drawing The Lower Pipes
    glPushMatrix()
    gameImages.ApplyImage(6)
    LowerPipeRenderer.DrawImage(0,.5,0,1)
    glPopMatrix()
#Drawing The Upper Pipes
    glPushMatrix()
    gameImages.ApplyImage(6)
    UpperPipeRenderer.DrawImage(.5,1,0,1)
    glPopMatrix()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def PipesRender():
    global PipesRandom
    global pipes
    global randomBackground
    global Easy
    if randomBackground==1:
        gameImages.ApplyImage(1) #Draw The Selected Background
        backgroundRenderer.DrawImage(0,.5,0,1)
        glLoadIdentity()
    elif randomBackground==2:
        gameImages.ApplyImage(1) #Draw The Selected Background
        backgroundRenderer.DrawImage(.5,1,0,1)
        glLoadIdentity()

    DrawName() #Draw The FlappyBird Logo
    glLoadIdentity()

    supermario()
    glLoadIdentity() 

    fireBalls()
    glLoadIdentity()

    for i in range(0,20,1): #A For Loop To Draw Twenty Pipes
        glLoadIdentity()
        if Easy:
            drawPipes(i,pipes[i]) #To Draw The Pipes With A Specific xTranslation Between Each Two Pipes "1 Unit" And a Random yTranslation From The "pipes" List 
        if not Easy:
            drawPipes(i*.8,pipes[i])
    if randomGround==4:
        gameImages.ApplyImage(5) #Draw The Random Ground
        groundSprite.DrawImage(0,.5,0,1)
        glLoadIdentity()
    elif randomGround==5:
        gameImages.ApplyImage(5) #Draw The Random Ground
        groundSprite.DrawImage(.5,1,0,1)
        glLoadIdentity() 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def DrawName(): #Draw "FLAPPY BIRD" 
    global speedX,Stop
    if not Stop: #Do not Drawing the "FLAPPY BIRD" logo again after losing
        flappy.StartingTransformation([0 - speedX,0.3,0],[16,10,1])
        glLoadIdentity()

        gameImages.ApplyImage(7)
        flappyRenderer.DrawImage(0.5,1,0,1)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def makeRandom(): 
    global randomBackground
    global randomBird
    global randomGround
    global BG
    global PipesRandom
    if PipesRandom: #To Generate The Height Only Once
        for i in range (0,20,1): #to Only Generate The RAndom yTranslate
            x = [-0.18,-0.16,-0.14,-0.12,-0.1,-0.08,-0.06,-0.04,-0.02,0,0.02,0.04,0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2] #A List To Choose The yTranslate From
            randomY = random.choice(x) #Get A Random Number From The List
            pipes.append(randomY)  #Appending The Random Height
        PipesRandom=False #Stop The Random Generation
    if not BG:
        randomBackground=random.randrange(1,3,1)
        randomBird = random.randrange(3,6,1)
        randomGround = random.randrange(4,6,1)
        BG=True 


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def birdMovement():
    global dtime , v_velocity ,anim, y , Stop , CountScore, SwagCheck , SoundPlayed,SwagSong
    if anim == 0 :
        y = y
        bird.StartingTransformation([-0.5, y, 0], [2.5, 1.75, 1])
        glLoadIdentity()
        

    if anim == 1 :

        bird.StartingTransformation([-0.5,y,0],[2.5,1.75,1])
        v_velocity = v_velocity -dtime
        y = y + v_velocity
    if y <=-.35 :
        Stop = True
        anim = 0
        if not SoundPlayed :  # Play The Lose Tone Once
            pygame.mixer.Sound.play(sound_hit)
            pygame.mixer.Sound.play(sound_die)
            SoundPlayed = True
        ScoreEffects()
    if y >= .5 :
        v_velocity = 0
        y = .5
        v_velocity = v_velocity -dtime

    glLoadIdentity()
    if not Stop and SwagCheck:



        gameImages.ApplyImage(3)
        birdRenderer.DrawImage(.75,1,0,1)
        glLoadIdentity()
    elif not Stop and not SwagCheck:
        gameImages.ApplyImage(3)
        if randomBird==3:
            birdRenderer.DrawImage(0,.24,0,1)
            glLoadIdentity()
        elif randomBird==4:
            birdRenderer.DrawImage(.25,.49,0,1)
            glLoadIdentity()
        elif randomBird==5:
            birdRenderer.DrawImage(.5,.74,0,1)
            glLoadIdentity()



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def keyboard(key,x,y): 
    global v_velocity , anim, Easy, Hard
    if Easy or Hard:
        if key == GLUT_KEY_UP:
            if not Stop :
                anim = 1
                v_velocity = .0092
                pygame.mixer.Sound.play(sound_button)  #Play The "wing" tone after each press


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


def TestCollision(alist):
    global pointer
    global CountScore
    global selectedpipe
    global increase
    global Stop
    global SwagCheck, MarioSong, PassedMario
    global SoundPlayed
    global PointerInc
    global Easy
    global ballmovements
    global ballY ,speedX

    PosX = []
    balls = []

    for i in range (0,8,1):
        balls.append(pipes[19]-.03 + ((ballmovements[i]*ballY[i])))
        PosX.append(((20.09 if Easy else 16.3) - speedX)-ballmovements[i])

#--------------------------------------------------------------------------Collision Algorithm-----------------------------------------------------------------------------------------#
    #LowerPipe.getPos() Method Gives Us Only The Last Position Of The Last Pipe 
    #But We Have The yTranslate Saved Into "pipes" List
    #So To Get The x Position Of The "i"th Pipe We Subtract The x of The LowerPipe.getPos() from "selectedpipe"
    #And To Get The y Position Of The "i"th Pipe We Load It From "pipe" List with A Pointer "pointer" Moves Through That List
    #Now We Have x and y Of Every Pipe 

    pipePos = [] #Clearing The Pipes and Bird Positions Everytime they Change
    if pointer != 20: #To Check If The Player Passed All The Pipes
        pipePos.extend([LowerPipe.getPos()[0] - selectedpipe,pipes[pointer]]) 

        if (pipePos[0]-.2 < bird.getPos()[0] < pipePos[0]+.2): #The Collision will occur Only If The x Of The Bird Is Between The Collision Surface "The Width Of The Pipe is 0.4"
            if (bird.getPos()[1] < pipePos[1] - .02  or bird.getPos()[1] > pipePos[1] + .13): #The Collision will Occur If The Y of The Bird is Less or Greater Than The Lower or The Upeer Pipe's Y Respectively 
                Stop = True     #Stop The Game And Show The ScoreBoard
                if not SoundPlayed :  # Play The Lose Tone Once
                    pygame.mixer.Sound.play(sound_hit)
                    pygame.mixer.Sound.play(sound_die)
                    SoundPlayed = True
        if CountScore <= pointer: #If Condition To Increase The Counter Only Once Not Everytime The Bird Point is between The Collison Surface But Not Crashed
            if (pipePos[0] < bird.getPos()[0] < pipePos[0] + .2) and ((pipePos[1] - .025 < bird.getPos()[1] < pipePos[1] + .125)): #The Score Is Increased If the Bird Position is Greater Than The Half Of Pipes
                increase = True #Increase The Score 
            
        if pipePos[0]+.25<bird.getPos()[0] <pipePos[0]+.3: #To Increase The Pointer After Leaving The Pipe to Select The Next Pipe 
            PointerInc=True #Increase pointer and Decrease selectedpipe

    if pointer == 19 :  
        for i in range(len(balls)):
            if (bird.getPos()[0]-.1<PosX[i]<bird.getPos()[0]+.1):
                if bird.getPos()[1]-.03<balls[i]<bird.getPos()[1]+.03:
                    #print("LOL")
                    Stop=True 
                    PassedMario=False
                    
        if PosX[len(PosX)-1]<(-1.5 if Easy else -1.5*.8):
            
            PassedMario = True
    
    if increase:
        CountScore += 1 #Increase The Score Only Once
        pygame.mixer.Sound.play(sound_point) #The "Point" Tone      
        increase = False 

    if speedX >= 21.5:
        Stop = True
        if not SoundPlayed:
            pygame.mixer.Sound.play(sound_win)
            SoundPlayed = True

    if PointerInc : #Increasing The pointer To point to the Next yTranslate at "pipes" and Decresing selectedpipe to get the Next pipe x Position
        pointer+=1
        if Easy:
            selectedpipe-=1
        else :
            selectedpipe-=.8
        PointerInc =False #ONLY ONCEEEE
def supermario():
    global speedX
    global pipes, PassedMario,speedY
    SuperMario.StartingTransformation([(20.2 if Easy else 16.4)- speedX, pipes[19]-(speedY if PassedMario else 0), 0], [2.5, 2.7,1])
    glLoadIdentity()
    gameImages.ApplyImage(11)
    SuperMarioRender.DrawImage(0,1,0,1)

def fireBalls():
    global speedX
    global pipes
    global ballmovements
    global ballY, anim, PassedMario,Easy
    if anim == 1 and PassedMario == False:
        gameImages.ApplyImage(10)

        for i in range (0,8,1):
            ball.StartingTransformation([(((20.09 if Easy else 16.3) - speedX)-ballmovements[i]), pipes[19]-.03 + ((ballmovements[i]*ballY[i])), 0], [1.5,1.5,1])
            glLoadIdentity()
            showBall.DrawImage(0,.5,0,1) 






def main():
#---------------------------------------------------##### The Objects' Order #####---------------------------------------------------------------------------------------------#
                            #1- Background 
                            #2- Flappy Bird Logo
                            #3- Pipes
                            #4- Ground
                            #5- Bird
                            #6- Tap To Start  
                            #7- Score And ScoreBoard    
    global gameImages
    global randomBackground
    global randomGround
    global pipes , balls, PosY
    global Tapped, Easy ,Hard, Clicked ,selectedpipe,CreditsEnable,PassedMario,pointer
    global xMouse,yMouse,Realx,Realy
    glClearColor(1, 1, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT) #Clearing The Color Buffer Bit

    makeRandom() #To Random The Objects
    glLoadIdentity()


    PipesRender() #Draw The Pipes
    glLoadIdentity()
 

    birdMovement() #Drawing And Moving The Bird

    Realy = (((glutGet(GLUT_WINDOW_HEIGHT) / 2) - yMouse) *2/ (glutGet(GLUT_WINDOW_HEIGHT) / 2)) / 2
    Realx = ((xMouse - (glutGet(GLUT_WINDOW_WIDTH) / 2 )) * 2 / (glutGet(GLUT_WINDOW_WIDTH) / 2)) / 2


    if anim == 0: #If No Key is Pressed Then Show Tap To Start Texture
        if not Tapped:
            gameImages.ApplyImage(7)
            TapRenderer.DrawImage(0,0.5,0,1)
            glLoadIdentity()

    
            Modes.StartingTransformation([-0.25,-0.1,0],[2.25,1.7,1])
            glLoadIdentity

            gameImages.ApplyImage(9)
            ModesRenderer.DrawImage(0,0.5,0,1)
            glLoadIdentity()
                
            Modes.StartingTransformation([0.25,-0.1,0],[2.25,1.7,1])
            glLoadIdentity

            gameImages.ApplyImage(9)
            ModesRenderer.DrawImage(0.5,1,0,1)
            glLoadIdentity()


            if Clicked  and -0.75 <= Realx <= -0.37  and -0.54 <=Realy <= -0.25:
                Medals.StartingTransformation([-0.55,-0.25,0],[2.25,1.75,1])
                glLoadIdentity()
                Easy = True
                selectedpipe=19
                    
            elif Clicked and 0.37 <= Realx <= 0.75  and -0.54 <=Realy <= -0.25:
                Medals.StartingTransformation([0.55,-0.25,0],[2.25,1.75,1])
                glLoadIdentity()
                Hard = True
                selectedpipe=19*.8
            Clicked = False
            gameImages.ApplyImage(10)
            MedalsRenderer.DrawImage(.5,1,0,1)
            glLoadIdentity()


    showScore() #Show The Score Of The Player On The Top Of The Screen
    glLoadIdentity() 

    if CreditsEnable:
        ShowCredits()
        glLoadIdentity()
    TestCollision(pipes) #Test The Collision At Each Frame 
    glutSwapBuffers()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def MouseMotion(button,state,x,y):
    global Clicked,Stop,Realx,Realy,xMouse,yMouse,CreditsEnable,Exit,xMouse,yMouse
    
    xMouse=x
    yMouse=y

    CursorInCreditsRange = (-0.67 <= Realx <= -0.11 and -0.56 <= Realy <= -0.32)
    CursorInExitRange = (0.11 <= Realx <= 0.67 and -0.56 <= Realy <= -0.32)

    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        Clicked = True
    
        if Stop: 
            if CursorInCreditsRange:
                CreditsEnable = True
            if CursorInExitRange:
                Exit = True
    
        
def MouseLocation (x,y):
    global xMouse,yMouse

    xMouse=x
    yMouse=y

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def Timer(v):
    global speedX,speedY,Stop ,ballmovements,pointer,CreditsSpeed,Clicked,PassedMario,sound_suck,FireballSound
    if not Stop:
        if pointer ==19 and not PassedMario:
            ballmovements[0] += .01
            for i in range (0,7,1):
                
                if ballmovements[i] > .4 :
                    ballmovements[i+1] +=.01

            
        elif PassedMario and speedY <.15:          
            speedY+=.001
        elif Easy :
            speedX +=.0085 #Set The Speed Of The Pipes
        elif Hard :
            speedX += 0.01

    if Stop and CreditsEnable and Clicked:
        if CreditsSpeed <= 1.25:
            CreditsSpeed += 0.001


    main()
    glutTimerFunc(time//FPS,Timer,1) #time//FPS to limit the Frames on specific no. of Frames
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def Display():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE| GLUT_RGBA)
    glutInitWindowPosition(800,50)
    glutInitWindowSize(WINDOW_WIDTH,WINDOW_HEIGHT)
    glutCreateWindow(b'Flappy Bird')
    glutDisplayFunc(main)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glutTimerFunc(time,Timer,1)
    glutSpecialFunc(keyboard)
    glutPassiveMotionFunc(MouseLocation)
    glutMouseFunc(MouseMotion)
    init()
    glutMainLoop()

Display()              