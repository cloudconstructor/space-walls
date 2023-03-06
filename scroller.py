import pygame, sys
import functions as fn


pygame.init()

#set local constants
size = screen_width, screen_height = 800, 600
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
gameMapSize = 5

#create game
screen = pygame.display.set_mode(size)
space = fn.space(200, 1)
space.generateSpace()
st = fn.Stage(gameMapSize)
st.setBlockCoordinates()
herostart = st.getfirstAlt()
h = fn.Hero(herostart)
intm = 0

intro_music = pygame.mixer.Sound("sound/music/space_walls_soundtrack_intro.ogg")
game_music = pygame.mixer.Sound("sound/music/game_music.ogg")
explosion = pygame.mixer.Sound("sound/sfx/explosion.ogg")
pygame.mixer.Sound.set_volume(intro_music, 0.7)
pygame.mixer.Sound.set_volume(game_music, 0.7)
pygame.mixer.Sound.set_volume(explosion, 0.6)

#auxiliary vars
intro_music_playing = 0
game_music_playing = 0
sound_on = 1
game_paused = 0
song_index = 0
soundset = 0
x = 0
state = 0
gameLevel = 1
counter = 0

#death message and some value reseting
def resetGame():
    global x, state, st, space, h, explosion, song_index

    fn.renderMessage2("YOU ARE FUCKIN DEAD!",42, red, screen_width //2, 200)
    fn.renderMessage2("BETTER LUCK NEXT TIME..",24, red, screen_width //2, 250)
    explosion.play(0)
    fn.refreshStage()
    pygame.time.wait(3000)

    del(st)
    del(space)
    space = fn.space(200, 1)
    space.generateSpace()
    st = fn.Stage(500)
    st.setBlockCoordinates()
    herostart = st.getfirstAlt()

    h = fn.Hero(herostart)
    fn.resetGameVals()
    x=0
    state = 0
    song_index = 0

def endGame():
    global x, state, st, space, h, explosion, song_index

    fn.mainLogo(150)
    fn.renderMessage2("YOU'VE MADE IT!",32, yellow, screen_width //2, 250)
    fn.renderMessage2("YOU HAVE ESCAPED TO HYPERSPACE AND TO FREEDOM!",24, red, screen_width //2, 280)
    fn.renderMessage2("HOPE YOU HAD AS GREAT TIME PLAYING THE GAME AS I HAD MAKING IT! ",24, red, screen_width //2, 310)
    fn.renderMessage2("SEE YOU AGAIN IN SOME OTHER ADVENTURE...",24, red, screen_width //2, 340)

    fn.refreshStage()
    pygame.time.wait(5000)

    del(st)
    del(space)
    space = fn.space(200, 1)
    space.generateSpace()
    st = fn.Stage(500)
    st.setBlockCoordinates()
    herostart = st.getfirstAlt()

    h = fn.Hero(herostart)
    fn.resetGameVals()
    x=0
    state = 0
    song_index = 0


if __name__ == "__main__":
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        

        # state machine begins......................
        if state == 0: #menu screen
            soundset = 0
            if intro_music_playing == 0:
                if sound_on == 1:
                    intro_music.play(-1)
                elif sound_on == 0:
                    intro_music.stop()
                intro_music_playing = 1
            
            space.roll_spaceFx()
            fn.menuScreen()
            ms = fn.getMenuSelection()
            if ms !=0:
                if ms == 1:
                    intro_music_playing = 0
                    if sound_on == 1: 
                        intro_music.fadeout(700)
                state = ms
        
            fn.refreshStage()
            screen.fill(black)

        elif state == 1: #game rolling

            if game_music_playing == 0:
                if sound_on == 1:
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

                #maybe this will be moved on functions.py...maybe...
                fn.renderMessage2("WARNING!",32, yellow, screen_width //2, 200)
                fn.renderMessage2("MYSTERIOUS ALIEN STRUCTURES KNOWN AS \"SPACE WALLS\"",24, red, screen_width //2, 230)
                fn.renderMessage2("ARE FORMING IN YOUR SECTOR. DONT GET TRAPPED INSIDE! ",24, red, screen_width //2, 260)
                fn.renderMessage2("FLY CAREFULLY THROUGH THE WALLS AND ESCAPE TO HYPERSPACE... ",24, red, screen_width //2, 290)


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
                pygame.time.wait(6000)
                x = 1

            screen.fill(black)

        elif state == 2: # quit game       
            pygame.quit()
            sys.exit()
            
        elif state == 3: #show credits
            space.roll_spaceFx()
            fn.roll_Credits()
            fn.refreshStage()
            screen.fill(black)
            m = fn.escapeCreds()
            # print(ms)
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
    
            fn.showSettings(sound_on)
            fn.refreshStage()
            screen.fill(black)
            m = fn.escapeCreds()
            if m:
                state = 0
    
        elif state == 666: # Failure Screen
            resetGame()   

        elif state == 667: # Failure Screen
            endGame()          