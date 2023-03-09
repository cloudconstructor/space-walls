import pygame, sys, os
from pygame.locals import *
from time import sleep
import functions as fn


game_title = "SPACE WALLS"

#set dispay parameters
screen_settings = fn.loadScreenSettings()
full_screen = screen_settings["full_screen"]
screen_width = screen_settings["screen_width"]
screen_height = screen_settings["screen_height"]


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.display.set_caption(game_title)

size = screen_width, screen_height
if full_screen == 1:
    flags = flags = pygame.SCALED | pygame.RESIZABLE | pygame.FULLSCREEN
else:
    flags = pygame.SCALED | pygame.RESIZABLE 
screen = pygame.display.set_mode(size, flags)
clock = pygame.time.Clock()

#set local constants
black = 0, 0, 0
black = 0, 0, 0
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
blue2 = (0, 0, 82)
red = (255, 0, 0)
orange = (255, 128, 0)
yellow = (255, 255, 0)
gray = (125, 125, 125)
gameMapSize = 1000


#create game
space = fn.space(200, 1)
space.generateSpace()
st = fn.Stage(gameMapSize)
st.setBlockCoordinates()
herostart = st.getfirstAlt()
h = fn.Hero(herostart)
intm = 0

intro_music = pygame.mixer.Sound("sound/music/space_walls_soundtrack_intro.ogg")
game_music = pygame.mixer.Sound("sound/music/game_music.ogg")
pygame.mixer.Sound.set_volume(intro_music, 0.7)
pygame.mixer.Sound.set_volume(game_music, 0.7)

#auxiliary vars
intro_music_playing = 0
game_music_playing = 0
sound_on = 1
song_index = 0
soundset = 0
x = 0
state = 0
gameLevel = 1
counter = 0
gamePaused = 0
screenSet = 0
# full_screen = screen_mode

#value reseting
def resetGame():
    global x, state, st, space, h, song_index, gamePaused, counter, gameLevel
    del(st)
    del(space)
    space = fn.space(200, 1)
    space.generateSpace()
    st = fn.Stage(gameMapSize)
    st.setBlockCoordinates()
    herostart = st.getfirstAlt()
    h = fn.Hero(herostart)
    fn.resetGameVals()
    x=0
    state = 0
    gameLevel = 1
    counter = 0
    song_index = 0
    gamePaused = 0


if __name__ == "__main__":
    
    _quit = False
    while not _quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                _quit = True
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                    if event.key==K_ESCAPE:
                        if state == 1:
                            if gamePaused == 0:
                                gamePaused = 1
                                game_music.fadeout(300)
                            else:
                                gamePaused = 0
                                if sound_on == 1:
                                    game_music.play(-1)


        

        # state machine begins......................
        if state == 0: #menu screen
            soundset = 0
            screenSet = 0

            if intro_music_playing == 0:
                if sound_on == 1:
                    pygame.mixer.Sound.set_volume(intro_music, 0.7)
                    intro_music.play(-1)
                elif sound_on == 0:
                    intro_music.stop()
                intro_music_playing = 1
            
            space.roll_spaceFx()
            fn.menuScreen()
            ms = fn.getMenuSelection()
            if ms !=0:
                if ms == 1: #start game
                    intro_music_playing = 0
                    if sound_on == 1: 
                        intro_music.fadeout(700)
                state = ms
        
            fn.refreshStage()
            screen.fill(black)

        elif state == 1: #game rolling

            if gamePaused == 0:
                if game_music_playing == 0:
                    if sound_on == 1:
                        pygame.mixer.Sound.set_volume(game_music, 0.7)
                        game_music.play(-1)
                    game_music_playing = 1

                #check health
                hero_health = h.getHeroHealth()
                if hero_health == 0:
                    fn.saveHighScore()
                    state = 666
                    if sound_on == 1:
                        game_music.fadeout(700)
                    game_music_playing = 0

                space.roll_spaceFx()
                st.renderStage()
                h.drawHero()
                h.handle_keys()
                st.renderStats()
                if x == 0:
                    fn.gameStory()


                #check finish
                distance = st.returnDistance()
                if(distance <= 0):
                    fn.saveHighScore()
                    state = 667
                    if sound_on == 1:
                        game_music.fadeout(700)
                    game_music_playing = 0


                st.scrollStage() #comment this for degubing
                fn.gameDiff()
                fn.refreshStage()

                if x == 0:
                    sleep(6)
                    x = 1

                screen.fill(black)


            else : #pause screen
                exit = fn.showPauseMenu()
                if exit: 
                    resetGame()

        elif state == 2: # quit game       
            pygame.quit()
            sys.exit()
            
        elif state == 3: #show credits
            space.roll_spaceFx()
            fn.roll_Credits()
            fn.refreshStage()
            screen.fill(black)
            m = fn.escapeCreds()
            if m:
                state = 0

        elif state == 4: #sound settings
            space.roll_spaceFx()
            
            if soundset == 0:
                if sound_on == 1:
                    sound_on = 0
                elif sound_on == 0:
                    sound_on = 1
                intro_music_playing = 0
                soundset = 1
    
            fn.showSoundSettings(sound_on)
            fn.refreshStage()
            screen.fill(black)
            m = fn.escapeCreds()
            if m:
                state = 0

        elif state == 5:
            space.roll_spaceFx()
            
            if screenSet == 0:
                if full_screen == 0:
                    full_screen = 1
                elif full_screen == 1:
                    full_screen = 0
                screenSet = 1

            fn.showScreenSettings(full_screen)
            fn.refreshStage()
            screen.fill(black)
            m = fn.escapeCreds()
            if m:
                pygame.display.toggle_fullscreen()
                state = 0

        elif state == 666: # Failure Screen
            fn.looseGame()
            sleep(3)
            resetGame()   

        elif state == 667: # Failure Screen
            fn.endGame()
            sleep(5)
            resetGame()        


pygame.quit()

# it was fun...