import pygame, random, sys

game_title = "SPACE WALLS"



pygame.init()
pygame.display.set_caption(game_title)
clock = pygame.time.Clock()

size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(size)
framerate = 50

wall_crush = pygame.mixer.Sound("sound/sfx/wallcrash.ogg")
wall_pass = pygame.mixer.Sound("sound/sfx/wallpass.ogg")
pygame.mixer.Sound.set_volume(wall_crush, 0.7)
pygame.mixer.Sound.set_volume(wall_pass, 0.4)

logo_height = screen_height // 2
lf = 0
menu_selection = 1
menu_final_selection = 0
debounce = 0

black = 0, 0, 0
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
blue2 = (0, 0, 82)
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
gray = (125, 125, 125)

barWidth = 10
barDistance = 200
scroll_speed = 2
levelUpwalls = 20 #every x walls the speed will accelerate
gameLevel = 1
gapsize = 100
heroPosition = 0, 0 ,0
hits = 0
hopsPassed = 0
oldHopsPassed = 0
star_speed = 1
star_density = 200
hero_health = 100
c = 0

class Stage:
    def __init__(self,mapSize):
        self.blockMapSize = mapSize
        self.blockCoords = [0] * self.blockMapSize #syntetagmenes gia ka8e block
        self.blockGapHeight = [0] * self.blockMapSize #pou 8a einai to keno
        self.scrollSpeed = scroll_speed #poso grhgora 8a scrollarei
        self.distance = 0
        self.blockXpos = 50

    def resetStage(self):
        global scroll_speed
        self.blockCoords = [0] * self.blockMapSize
        self.blockGapHeight = [0] * self.blockMapSize
        self.scrollSpeed = scroll_speed
        self.distance = 0
        self.blockXpos = 50

    def setBlockCoordinates(self): #generate random obsticles
        for x in range(self.blockMapSize):            
            self.blockXpos +=barDistance
            self.blockCoords[x] = self.blockXpos #wall coords
            rndbit = random.randint(50,500)
            self.blockGapHeight[x] = rndbit #gaps

    def getfirstAlt(self): # let our hero start near the first gap
        return self.blockGapHeight[0]
                
    def scrollStage(self): #reduce x corrds by speed on each refresh
        global hopsPassed, wall_pass
        for x in range(self.blockMapSize):
            self.blockXpos = self.blockCoords[x] - self.scrollSpeed
            self.blockCoords[x] = self.blockXpos  
            if self.blockXpos == 30:
                hopsPassed += 1
                # wall_pass.play(0)
                gapHeight = self.blockGapHeight[x]
                self.detectCollition(gapHeight)
                    
    def renderStage(self): #render blocks at the arrays corrds
        for x in range(self.blockMapSize):
            whiteCoords = self.blockCoords[x]
            w = Bar(gapsize, self.blockGapHeight[x], whiteCoords, blue, blue2)
            w.createBars()
            self.distance = self.blockCoords[x]
            
    def detectCollition(self, gapHeight): #detect hero collition with walls
        global hits, hero_health, wall_crush

        heroTop = heroPosition[0]
        heroBase = heroPosition[1]
        obsOpenTop = gapHeight
        obsOpenBot = gapHeight + gapsize

        if heroTop <= obsOpenTop:
            hits +=1
            screen.fill(white)
            hero_health -=10
            wall_crush.play(0)
        elif heroBase >= obsOpenBot:
            hits +=1
            screen.fill(white)
            hero_health -=10
            wall_crush.play(0)
        else:
            wall_pass.play(0)

    
    def renderStats(self): #output text
        global hopsPassed , hits, hero_health, gameLevel

        #distance    
        font1 = pygame.font.SysFont('impact', 24)
        text1 = font1.render('Distance remaining: '+str(self.distance)+ 'miles', True, green)
        textRect1 = text1.get_rect()
        textRect1.center = (screen_width // 2, screen_height -20)
        screen.blit(text1, textRect1)
        
        #health    
        font2 = pygame.font.SysFont('impact', 36)
        text2 = font2.render("\U00002665"+str(hero_health)+ '%', True, red)
        textRect2 = text2.get_rect()
        textRect2.center = (screen_width - 250, 20)
        screen.blit(text2, textRect2)

        #hops
        font3 = pygame.font.SysFont('impact', 36)
        text3 = font3.render("W "+str(hopsPassed), True, yellow)
        textRect3 = text3.get_rect()
        textRect3.center = (screen_width - 140, 20)
        screen.blit(text3, textRect3)

        #level
        font3 = pygame.font.SysFont('impact', 36)
        text3 = font3.render("LvL "+str(gameLevel), True, green)
        textRect3 = text3.get_rect()
        textRect3.center = (screen_width - 50, 20)
        screen.blit(text3, textRect3)

    
class Bar:
    def __init__(self, opensize, openheight, empodioPosition, color1, color2):
        self.openSize = opensize
        self.openHeight = openheight
        self.barColor1 = color1
        self.barColor2 = color2
        self.empodioPosition = empodioPosition

    def createBars(self): #design the obsticle bars
        topBar = pygame.Rect(self.empodioPosition, 0, barWidth, self.openHeight)
        topBar2 = pygame.Rect(self.empodioPosition+10, 0, barWidth, self.openHeight)
        pygame.draw.rect(screen, self.barColor1, topBar, 100)
        pygame.draw.rect(screen, self.barColor2, topBar2, 100)

        btb_start = self.openHeight + self.openSize
        btb_height = screen_height - btb_start

        bottomBar = pygame.Rect(self.empodioPosition, btb_start, barWidth, btb_height)
        bottomBar2 = pygame.Rect(self.empodioPosition+10, btb_start, barWidth, btb_height)
        pygame.draw.rect(screen, self.barColor1, bottomBar, 100)
        pygame.draw.rect(screen, self.barColor2, bottomBar2, 100)

class Hero:
    def __init__(self, herostart):
        self.heroAlt  = herostart + 35
        
    def drawHero(self):
        global c, hero_health
        c1 = 10, self.heroAlt
        c2 = 10, self.heroAlt+20
        c3 = 30, self.heroAlt+10
        inc1 = 10, self.heroAlt+5
        inc2 = 10, self.heroAlt+15
        inc3 = 25, self.heroAlt+10
        lineu = 8, self.heroAlt
        lined = 8, self.heroAlt+20
        lineu2 = 6, self.heroAlt+7
        lined2 = 6, self.heroAlt+13

        if hero_health <= 50 and hero_health > 20:
            herocolor = orange
        elif hero_health <= 20 and hero_health > 10:
            herocolor = red
        elif hero_health <= 10:
            if c == 5:
                herocolor = yellow
            else:
                herocolor = red
        else:
            herocolor = gray

        if c == 5:
            herocolor1 = white
            herocolor2 = white
            c = 0
        else:
            herocolor1 = red
            herocolor2 = orange
            c +=1

        pygame.draw.polygon(screen, herocolor, (c1, c2, c3), 3)
        pygame.draw.polygon(screen, herocolor, (inc1, inc2, inc3), 8)
        pygame.draw.line(screen, herocolor1, lineu, lined, 3)
        pygame.draw.line(screen, herocolor2, lineu2, lined2, 3)


    def handle_keys(self):
        global heroPosition

        key = pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_w]:
            if(self.heroAlt > 10):
                self.heroAlt -=5
        if key[pygame.K_DOWN] or key[pygame.K_s]:
            if(self.heroAlt < screen_height-30):
                self.heroAlt +=5
        heroPosition = self.heroAlt, (self.heroAlt+30), 30

    def getHeroHealth(self):
        global hero_health
        return hero_health

    
class space:
    def __init__(self, star_density, star_speed):
        self.density = int(star_density)
        self.speed = int(star_speed)
        
    def generateSpace(self):
        self.stars = [
            [random.randint(0, screen_width),random.randint(0, screen_height)]
            for x in range(self.density)
        ]

    def roll_spaceFx(self):
        for star in self.stars:
            pygame.draw.line(screen,
                (255, 255, 255), (star[0], star[1]), (star[0], star[1]))
            star[0] = star[0] - 1
            if star[0] < 0:
                star[0] = screen_width
                star[1] = random.randint(0, screen_height)
        screen.blit(screen, (0,0))


def resetGameVals():
    global hero_health, barDistance, scroll_speed, gapsize, heroPosition, hits, hopsPassed, star_speed, c, lf, menu_selection, menu_final_selection, debounce,framerate
    
    barDistance = 200
    scroll_speed = 2
    gapsize = 100
    heroPosition = 0, 0 ,0
    hits = 0
    hopsPassed = 0
    # oldHopsPassed = 0
    star_speed = 1
    hero_health = 100
    c = 0
    lf = 0
    menu_selection = 1
    menu_final_selection = 0
    debounce = 0
    framerate = 50

def renderMessage(message):
    font = pygame.font.SysFont('impact', 42)
    text = font.render(message  , True, red)
    textRect = text.get_rect()
    textRect.center = (screen_width // 2, screen_height // 2)
    screen.blit(text, textRect)

def showCredLine():
    font = pygame.font.SysFont('impact', 18)
    text = font.render("2023 by Buggy Games v0.7"  , True, red)
    textRect = text.get_rect()
    textRect.center = (screen_width // 2, screen_height -20)
    screen.blit(text, textRect)

def renderMessage2(message, fontsize, color, x, y):
    font = pygame.font.SysFont('impact', fontsize)
    text = font.render(message  , True, color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    screen.blit(text, textRect)

def refreshStage():
    pygame.display.flip()
    clock.tick(framerate) #fps
    pygame.display.update()

      
def gameDiff():
        global hopsPassed, oldHopsPassed,  gameLevel, framerate, levelUpwalls
        deltaHops = hopsPassed - oldHopsPassed  
        if deltaHops == levelUpwalls:
            oldHopsPassed = hopsPassed
            framerate +=10
            gameLevel +=1

def mainLogo(height):
    global game_title
    font = pygame.font.SysFont('impact', 82, True, True)
    text = font.render(game_title  , True, blue2)
    textRect = text.get_rect()
    textRect.center = (screen_width // 2, height)
    screen.blit(text, textRect)

    font2 = pygame.font.SysFont('impact', 79, False, True)
    text2 = font2.render(game_title  , True, blue)
    textRect2 = text2.get_rect()
    textRect2.center = (screen_width // 2, height)
    screen.blit(text2, textRect2)

def mainMenu(height, selc):
    sc = red
    uc = green
    if selc == 1:
        c1 = sc
        c2 = uc
        c3 = uc
        c4 = uc
    elif selc == 2: #quit
        c2 = sc
        c1 = uc
        c3 = uc
        c4 = uc
    elif selc == 3: #creds
        c1 = uc
        c2 = uc
        c3 = sc
        c4 = uc
    elif selc == 4: #sound
        c1 = uc
        c2 = uc
        c3 = uc
        c4 = sc

    font = pygame.font.SysFont('impact', 36)
    text = font.render("START" , True, c1, black)
    text2 = font.render("QUIT"  , True, c2, black)
    text3 = font.render("CREDS"  , True, c3, black)
    text4 = font.render("SOUND"  , True, c4, black)

    height2 = height + 40
    height3 = height2 + 40
    height4 = height3 + 40
    textRect = text.get_rect()
    textRect2 = text2.get_rect()
    textRect3 = text3.get_rect()
    textRect4 = text4.get_rect()
    textRect.center = (screen_width // 2, height)
    textRect2.center = (screen_width // 2, height2)
    textRect3.center = (screen_width // 2, height3)
    textRect4.center = (screen_width // 2, height4)
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text4, textRect4)

def menuKeys():
    global menu_selection, debounce, menu_final_selection

    key = pygame.key.get_pressed()
    if key[pygame.K_UP] or key[pygame.K_w]:
        if debounce == 8:
            menu_final_selection = 0
            if menu_selection > 1:
                menu_selection -=1
            debounce = 0
        else:
            debounce += 1
        
    if key[pygame.K_DOWN] or key[pygame.K_s]:
        if debounce == 8:
            menu_final_selection = 0
            if menu_selection < 4:
                menu_selection +=1
            debounce = 0
        else:
            debounce += 1

    if key[pygame.K_RETURN]:
        if debounce == 8:
            menu_final_selection = menu_selection
            debounce = 0
        else:
            debounce += 1
        
def getMenuSelection():
    global menu_final_selection
    return menu_final_selection

def menuScreen():
    global logo_height, lf, menu_selection
    sp = space(200, 1)
    sp.generateSpace()

    if lf == 60:
        if(logo_height > 100):
            logo_height -= 5
    else:
        lf +=1
    mainLogo(logo_height)
    if(logo_height == 100):
        mainMenu(300, menu_selection)
        menuKeys()
        showCredLine()

def roll_Credits():
    global menu_final_selection, menu_selection
    menu_final_selection = 0
    
    text = (
            "Coded in Python 3.9 and pygame 2.1.3 by George Droulias",
            "Music Composed and played by George Droulias",
            "",
            "TODO list:",
            "1.Make a better collition and keyb debounce algorithm",
            "2.get the game stats to the death screen",
            "3.Make an endgame screen",
            "4.Optimize and reduce code",
            "5.turn this to exe file",
            )
    
    h = 100
    for t in text:
        renderMessage2(t, 24, red, screen_width //2, h)
        h +=30  


def showSettings(sound_on):
    global menu_final_selection, menu_selection
    menu_final_selection = 0
    #array contents
    text = (
            "SOUND OFF",
            "SOUND ON",
            )
    renderMessage2(text[sound_on], 24, red, screen_width //2, screen_height // 2)
     
def escapeCreds():
    renderMessage2("Press [ESC] for Menu", 18, yellow, screen_width //2, screen_height - 20)
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        return True
    

