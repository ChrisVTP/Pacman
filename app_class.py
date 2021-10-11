import sys
import pygame
from pygame.mixer import Sound
import time
from player import *
from setting import *
from ghost import *
from wall_class import *
import webbrowser
pygame.init()
pygame.mixer.init()
vec = pygame.math.Vector2

class App :
    def __init__(self):
        self.wallClass = wall()
        self.wallString = self.wallClass.generate()
        self.screen = pygame.display.set_mode((WIDTH +100, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'intro'
        self.score = 0
        self.highest = 0
        self.cell_h = MAZE_HEIGHT //ROWS
        self.cell_w = MAZE_WIDTH //COLS
        self.player = Player(self,PLAYER_START_POSITION)
        self.button = {}
        self.wall = []
        self.ghost = []
        self.points = []
        self.Bpoints = []
        self.close = True
        self.black = time.time()
        self.play_button = {}
        self.quit_button = {}
        self.conf_button = {}
        self.play_sound(INTRO_SOUND)
        self.sound_time = time.time()
        self.load()
    def run(self):
        while self.running :
            if self.state == 'intro':
                self.start_event()
                self.start_update()
                self.start_draw()
                if time.time()- self.sound_time > INTRO_SOUND_LENGTH+2:
                    self.play_sound(INTRO_SOUND)
                    self.sound_time = time.time()
            elif self.state == 'playing':
                self.playing_event()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'configure': #not coded yet
                self.conf_event()
                # self.conf_update()
                self.conf_draw()
            elif self.state == 'game over': #not coded yet
                self.over_event()
                self.over_update()
                self.over_draw()
            elif self.state == 'pausing': 
                self.pause_event()
                self.pause_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        self.save_score()
        pygame.quit()
        sys.exit()
##################### HELP FUNCTION ################################33
    def draw_text(self, word,screen,pos, size, color, font_name, center = False):
        font = pygame.font.SysFont(font_name, size)
        text = font.render(word, False, color)
        text_size = text.get_size()
        if center:
            pos[0] = pos[0] - text_size[0] //2
            pos[1] = pos[1] - text_size[1] //2
        screen.blit(text,pos)
    
    def save_score(self):
        if self.score> self.highest:
            self.highest = self.score
        with open("score.txt", 'w') as file:
            file.write("{}".format(self.highest))

    def load(self):
        self.icon = pygame.image.load(START_ICON)
        # self.reset()
        # background = pygame.image.load('maze.png')
        # self.background = pygame.transform.scale(background,(MAZE_WIDTH, MAZE_HEIGHT))
        # self.food = pygame.image.load('food.png')
        # self.food = pygame.transform.scale(self.food, (200, 200))
        with open("score.txt", 'r') as file:
            x = file.readline()
            if (x.isdigit()):
                self.highest = int(x)
        
        file = self.wallString
        for y,line in enumerate(file):

            for x, char in enumerate(line):
                if char == "1":
                    self.wall.append(vec(x,y))
                elif char == "2":
                    self.ghost.append( Ghost(self, vec(x,y) , BLINKY) )
                elif char == "3":
                    self.ghost.append( Ghost(self, vec(x,y) , PINKY) )
                elif char == "4":
                    self.ghost.append( Ghost(self, vec(x,y) , INKY) )
                elif char == "5":
                    self.ghost.append( Ghost(self, vec(x,y) , CLYDE) )
                elif char =="C" :
                    self.points.append(vec(x, y))
                elif char == "B":
                    self.Bpoints.append(vec(x, y))
                    self.points.append(vec(x, y))
                elif char == "P":
                    PLAYER_START_POSITION = vec(x,y)

        # print(self.wall)
    # def darw_grid(self):
    #     for x in range(WIDTH//self.cell_w):
    #         pygame.draw.line(self.background, GREY , (x*self.cell_w, 0),(x*self.cell_w, HEIGHT))
    #     for y in range(HEIGHT//self.cell_h):
    #         pygame.draw.line(self.background, GREY , (0, y * self.cell_h),(WIDTH, y*self.cell_h))

    def draw_points(self):
        for f in self.points:
            # if (f[0] == 1 and f[1] == 1) or (f[0] == 26 and f[1] == 1) or (f[0] == 1 and f[1] == 29) or (f[0] == 26 and f[1] == 29) or (f[0] == 13 and f[1] == 29):
            if (f in self.Bpoints):
                if self.close :
                    self.point = pygame.draw.circle(self.screen, WHITE, ((f[0] * self.cell_w + TOP_BOTTOM_BUFFER // 2) + self.cell_w//2 , (f[1] * self.cell_h + TOP_BOTTOM_BUFFER // 2)+ self.cell_h//2) , 7)
                # else:
                #     self.point = pygame.draw.circle(self.background, BLACK, ((f[0] * self.cell_w + TOP_BOTTOM_BUFFER // 2) - 15, (f[1] * self.cell_h + TOP_BOTTOM_BUFFER // 2) - 15), 7)
            else:
                self.point = pygame.draw.circle(self.screen, WHITE, ((f[0] *self.cell_w + TOP_BOTTOM_BUFFER//2)+ self.cell_w//2 , (f[1] * self.cell_h +TOP_BOTTOM_BUFFER//2)+ self.cell_h//2) , 4)
        # print("Draw coint")
    def change_state_B(self):
        if (time.time() - self.black) >= 0.2:
            self.close = not self.close
            self.black = time.time()

    def draw_wall(self):
        for w in self.wall:
            pygame.draw.rect(self.screen, BLUE,(w[0]*self.cell_w + TOP_BOTTOM_BUFFER//2, 
                                                w[1]* self.cell_h+ TOP_BOTTOM_BUFFER//2, 
                                                self.cell_w, 
                                                self.cell_h))
            # pygame.draw.circle(self.screen, BLUE, (w[0] *self.cell_w + TOP_BOTTOM_BUFFER//2, w[1] * self.cell_h +TOP_BOTTOM_BUFFER//2),2)
    def in_button (self, button_pos):
        mouse_pos = pygame.mouse.get_pos()
        pos, w,h = button_pos[:3]
        return  mouse_pos[0] > pos[0] and mouse_pos[1]> pos[1] and mouse_pos[0] < pos[0] + w and mouse_pos[1] < pos[1] + h

    def draw_button(self, word, screen, pos, w,h ,default_colour, state, button ):
        # if type(button) != list():
        #     button = self.button
        hollow_colour = self.in_button((pos,w,h))
        rec = pygame.Rect(pos[0], pos[1], w, h)
        
        if hollow_colour:
            default_colour = (default_colour[0]/3, default_colour[1]/3,default_colour[2]/3)
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else: 
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        pygame.draw.rect(screen, default_colour,rec ,  50, 10)
        self.draw_text(word, screen, [(pos[0]+w//2) , (pos[1]+h//2) ], BUTTON_WORD_SIZE, WHITE, BUTTON_WORD_FONT, True)
        if word not in button:
            button[word] = (pos, w,h, state)
        # print(button)
        # self.screen.fill(default_colour, rec)

    def play_sound(self, soundname):
        sound = pygame.mixer.Sound(soundname)
        sound.play()

    def reset(self, replay = False):
        with open("score.txt", 'r') as file:
            x = file.readline()
            if (x.isdigit()):
                self.highest = int(x)
        self.wall = []
        self.ghost = []
        self.points = []
        self.Bpoints = []
        file = self.wallString
        for y,line in enumerate(file):
            for x, char in enumerate(line):
                if char == "1":
                    self.wall.append(vec(x,y))
                elif char == "2":
                    self.ghost.append( Ghost(self, vec(x,y) , BLINKY) )
                elif char == "3":
                    self.ghost.append( Ghost(self, vec(x,y) , PINKY) )
                elif char == "4":
                    self.ghost.append( Ghost(self, vec(x,y) , INKY) )
                elif char == "5":
                    self.ghost.append( Ghost(self, vec(x,y) , CLYDE) )
                elif char =="C" :
                    self.points.append(vec(x, y))
                elif char == "B":
                    self.Bpoints.append(vec(x, y))
                    self.points.append(vec(x, y))
                elif char == "P":
                    PLAYER_START_POSITION = vec(x,y)
        if replay:  self.score = 0
        self.player = Player(self,PLAYER_START_POSITION)
##################### PAUSE FUNCTION ################################33
    def pause_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "playing"
            if event.type == pygame.MOUSEBUTTONUP:
                for key in self.play_button:
                    if self.in_button(self.play_button[key]):
                        # print(self.play_button)
                        self.state = self.play_button[key][-1] #the state in the button tuple
                        break
    def pause_draw(self):
        self.draw_text("PAUSE", self.screen, [SCREEN_WIDTH//2, HEIGHT//2], 100,(250,128,114)   , START_FONT, center = True)
        self.draw_button("HOME", self.screen, [SCREEN_WIDTH- BUTTON_W +40 , HEIGHT//2+50], BUTTON_W - 50, BUTTON_H ,RED, "intro", self.play_button)
        self.draw_button("QUIT", self.screen, [SCREEN_WIDTH- BUTTON_W +40 , HEIGHT//2+150], BUTTON_W - 50, BUTTON_H ,RED, "quit", self.play_button)
        pygame.display.update()

##################### START FUNCTION ################################33
    def start_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                for key in self.button:
                    if self.in_button(self.button[key]):
                        self.state = self.button[key][-1] #the state in the button tuple
                        pygame.mixer.stop()
                        break

    def start_update(self):
        pass
    def start_draw(self):
        self.screen.fill (BLACK)
        icon = pygame.transform.scale(self.icon, (400,100))
        self.screen.blit(icon,[SCREEN_WIDTH//2 -200, HEIGHT//2 -150])

        self.draw_text("2805ICT System and Software Design",self.screen, [SCREEN_WIDTH//2, HEIGHT//2], START_TEXT_SIZE,(25, 73, 215)   , START_FONT, center = True)
        self.draw_text("3815ICT Software Engineering ",self.screen, [SCREEN_WIDTH//2, HEIGHT//2 + 50], START_TEXT_SIZE, (25, 73, 215) , START_FONT, center = True)
        self.draw_text("2021-Trimester 2",self.screen, [SCREEN_WIDTH//2, HEIGHT//2 + 100], START_TEXT_SIZE, (170,132,58), START_FONT, center = True)
        self.draw_text("HIGHEST SCORE: {}".format(self.highest),self.screen, [4, 0], START_TEXT_SIZE, (255,255,255) , START_FONT)

        #Draw Play game button
        self.draw_button("Play", self.screen, [10, HEIGHT//2+150], BUTTON_W, BUTTON_H ,RED, "playing", self.button)
        self.draw_button("Quit", self.screen, [SCREEN_WIDTH- BUTTON_W -10, HEIGHT//2+150], BUTTON_W, BUTTON_H ,RED, "quit", self.button)
        self.draw_button("Confingure", self.screen, [SCREEN_WIDTH//2 - BUTTON_W//2, HEIGHT//2+150], BUTTON_W, BUTTON_H ,RED, "configure", self.button)
        
        # draw student name:
        student_height_pos = HEIGHT - 60
        for i in STUDENTS:
            self.draw_text(i[0], self.screen, [10,student_height_pos], STUDENT_SIZE, (255,255,255), STUDENT_FRONT)
            self.draw_text(i[1], self.screen, [170,student_height_pos], STUDENT_SIZE, (255,255,255), STUDENT_FRONT)
            self.draw_text(i[2], self.screen, [250,student_height_pos], STUDENT_SIZE, (255,255,255), STUDENT_FRONT)
            student_height_pos += 20
        
        pygame.display.update()

    

##################### Playing FUNCTION ################################33
    def playing_event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "pausing"
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1,0))
                elif event.key == pygame.K_RIGHT:
                    self.player.move(vec(1,0))
                elif event.key == pygame.K_UP:
                    self.player.move(vec(0,-1))
                elif event.key == pygame.K_DOWN:
                    self.player.move(vec(0,1))
            if event.type == pygame.MOUSEBUTTONUP:
                for key in self.play_button:
                    if self.in_button(self.play_button[key]):
                        # print(self.play_button)
                        self.state = self.play_button[key][-1] #the state in the button tuple
                        break

    def playing_update(self):
        self.change_state_B()
        self.player.update()
        self.player.change_state()
        if ((not self.points) ):
            self.reset()

        for g in self.ghost:
            g.update()
            g.change_state()
        # for enermy in self.ghost:
        #     if(enermy.grid_pos == self.player.grid_pos):
        #         self.state = "game over"
        #         # self.running = False
        #         self.reset(True)
        #         break
        

    def playing_draw(self):
        self.screen.fill(BLACK)
        # self.screen.blit (self.background,(TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.draw_wall()
        # self.draw_button("HOME", self.screen, [SCREEN_WIDTH- BUTTON_W +40 , HEIGHT//2+50], BUTTON_W - 50, BUTTON_H ,RED, "intro", self.play_button)
        self.draw_button("QUIT", self.screen, [SCREEN_WIDTH- BUTTON_W +40 , HEIGHT//2+150], BUTTON_W - 50, BUTTON_H ,RED, "quit", self.play_button)
        #self.darw_grid()
        #self.draw_wall()
        self.draw_points()
        self.draw_text("CURRENT SCORE: {}".format(self.score),self.screen, [50, 5], 18, WHITE , START_FONT)
        self.draw_text("HIGH SCORE: {}".format(self.highest),self.screen, [WIDTH//2, 5], 18, WHITE , START_FONT)
        self.player.draw()
        for g in self.ghost:
            g.draw()


        pygame.display.update()
        # print(self.play_button)
    
##################### Configuring FUNCTION ################################33


    def conf_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                for key in self.conf_button:
                    if self.in_button(self.conf_button[key]):
                        print(self.conf_button[key][-1])
                        if (self.conf_button[key][-1] == "new"):
                            self.conf_update()
                        elif (self.conf_button[key][-1] == "credit"):
                            webbrowser.open('https://shaunlebron.github.io/pacman-mazegen/', new=1)
                            
                        else:
                            self.state = self.conf_button[key][-1] #the state in the button tuple
                            
                        break

    def conf_update(self):
        self.wallString = self.wallClass.generate()
        self.reset()
    def conf_draw(self):
        self.screen.fill(BLACK)
        self.draw_wall()
        self.draw_button("HOME", self.screen, [SCREEN_WIDTH- BUTTON_W +40 , HEIGHT//2+50], BUTTON_W - 50, BUTTON_H ,RED, "intro", self.conf_button)
        self.draw_button("GENERATE", self.screen, [SCREEN_WIDTH- BUTTON_W +40 , HEIGHT//2+150], BUTTON_W - 50, BUTTON_H ,RED, "new", self.conf_button)
        Credit_POS = HEIGHT - 20
        self.draw_button("", self.screen, [10 , HEIGHT - 25], SCREEN_WIDTH -20 , HEIGHT ,BLACK, "credit", self.conf_button)
        self.draw_text("This Generator is credit for Shaun LeBron(Click here for more information).", self.screen, [10,Credit_POS], STUDENT_SIZE, (255,255,255), STUDENT_FRONT)
        pygame.display.update()

    # def creditTo(self, fromW, fromH, toW, toH):
    #     mouse_pos = pygame.mouse.get_pos()
    #     return  mouse_pos[0] > fromW and mouse_pos[1]> fromH and mouse_pos[0] < toW and mouse_pos[1] <  toH
##################### Configuring FUNCTION ################################33

    def over_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                for key in self.quit_button:
                    if self.in_button(self.quit_button[key]):
                        self.state = self.quit_button[key][-1] #the state in the button tuple
                        # pygame.mixer.stop()
                        break

    def over_update(self):
        pass
    def over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER",self.screen, [SCREEN_WIDTH//2 , HEIGHT//2 - 200], 50,(25, 73, 215)   , START_FONT, center = True)

        self.draw_text("2805ICT System and Software Design",self.screen, [SCREEN_WIDTH//2, HEIGHT//2], START_TEXT_SIZE,(25, 73, 215)   , START_FONT, center = True)
        self.draw_text("3815ICT Software Engineering ",self.screen, [SCREEN_WIDTH//2, HEIGHT//2 + 50], START_TEXT_SIZE, (25, 73, 215) , START_FONT, center = True)
        self.draw_text("2021-Trimester 2",self.screen, [SCREEN_WIDTH//2, HEIGHT//2 + 100], START_TEXT_SIZE, (170,132,58), START_FONT, center = True)
        self.draw_text("HIGHEST SCORE: {}".format(self.highest),self.screen, [4, 0], START_TEXT_SIZE, (255,255,255) , START_FONT)


        self.draw_button("Home", self.screen, [10, HEIGHT//2+150], BUTTON_W, BUTTON_H ,RED, "intro", self.quit_button)
        self.draw_button("Quit", self.screen, [SCREEN_WIDTH- BUTTON_W -10, HEIGHT//2+150], BUTTON_W, BUTTON_H ,RED, "quit", self.quit_button)

        # draw student name:
        student_height_pos = HEIGHT - 60
        for i in STUDENTS:
            self.draw_text(i[0], self.screen, [10,student_height_pos], STUDENT_SIZE, (255,255,255), STUDENT_FRONT)
            self.draw_text(i[1], self.screen, [170,student_height_pos], STUDENT_SIZE, (255,255,255), STUDENT_FRONT)
            self.draw_text(i[2], self.screen, [250,student_height_pos], STUDENT_SIZE, (255,255,255), STUDENT_FRONT)
            student_height_pos += 20
        pygame.display.update()
