import sys
import pygame
from pygame.mixer import Sound
import pygame_menu
import time
from player import *
from setting import *

pygame.init()
pygame.mixer.init()
vec = pygame.math.Vector2
class App :
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'intro'
        self.score = 0
        self.cell_h = MAZE_HEIGHT //ROWS
        self.cell_w = MAZE_WIDTH //COLS
        self.player = Player(self,PLAYER_START_POSITION)
        self.button = {}
        self.wall = []
        # self.menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_DARK)   
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
                self.start_event()
                self.start_update()
                self.start_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
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
    
    def load(self):
        self.icon = pygame.image.load(START_ICON)
        background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(background,(MAZE_WIDTH, MAZE_HEIGHT))
        with open("wall.txt", 'r') as file:
            for y,line in enumerate(file):
                for x, char in enumerate(line):
                    if char == "1":
                        self.wall.append(vec(x,y))
        print(self.wall)
    def darw_grid(self):
        for x in range(WIDTH//self.cell_w):
            pygame.draw.line(self.background, GREY , (x*self.cell_w, 0),(x*self.cell_w, HEIGHT))
        for y in range(HEIGHT//self.cell_h):
            pygame.draw.line(self.background, GREY , (0, y * self.cell_h),(WIDTH, y*self.cell_h))

    def draw_wall(self):
        for w in self.wall:
            pygame.draw.circle(self.screen, BLUE, (w[0] *self.cell_w + TOP_BOTTOM_BUFFER//2, w[1] * self.cell_h +TOP_BOTTOM_BUFFER//2),2)
    def in_button (self, button_pos):
        mouse_pos = pygame.mouse.get_pos()
        pos, w,h = button_pos[:3]
        return  mouse_pos[0] > pos[0] and mouse_pos[1]> pos[1] and mouse_pos[0] < pos[0] + w and mouse_pos[1] < pos[1] + h

    def draw_button(self, word, screen, pos, w,h ,default_colour, state):
        hollow_colour = self.in_button((pos,w,h))
        rec = pygame.Rect(pos[0], pos[1], w, h)
        if hollow_colour:
            default_colour = (default_colour[0]/3, default_colour[1]/3,default_colour[2]/3)
        pygame.draw.rect(screen, default_colour,rec ,  50, 10)
        self.draw_text(word, screen, [(pos[0]+w//2) , (pos[1]+h//2) ], BUTTON_WORD_SIZE, WHITE, BUTTON_WORD_FONT, True)
        if word not in self.button:
            self.button[word] = (pos, w,h, state)
        # self.screen.fill(default_colour, rec)

    def play_sound(self, soundname):
        sound = pygame.mixer.Sound(soundname)
        sound.play()
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
        self.screen.blit(icon,[WIDTH//2 -200, HEIGHT//2 -150])

        self.draw_text("2805ICT System and Software Design",self.screen, [WIDTH//2, HEIGHT//2], START_TEXT_SIZE,(25, 73, 215)   , START_FONT, center = True)
        self.draw_text("3815ICT Software Engineering ",self.screen, [WIDTH//2, HEIGHT//2 + 50], START_TEXT_SIZE, (25, 73, 215) , START_FONT, center = True)
        self.draw_text("2021-Trimester 2",self.screen, [WIDTH//2, HEIGHT//2 + 100], START_TEXT_SIZE, (170,132,58), START_FONT, center = True)
        self.draw_text("HIGHEST SCORE: {}".format(self.score),self.screen, [4, 0], START_TEXT_SIZE, (255,255,255) , START_FONT)

        #Draw Play game button
        self.draw_button("Play", self.screen, [10, HEIGHT//2+150], BUTTON_W, BUTTON_H ,RED, "playing")
        self.draw_button("Quit", self.screen, [WIDTH- BUTTON_W -10, HEIGHT//2+150], BUTTON_W, BUTTON_H ,RED, "quit")
        self.draw_button("Confingure", self.screen, [WIDTH//2 - BUTTON_W//2, HEIGHT//2+150], BUTTON_W, BUTTON_H ,RED, "configure")
        
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

    def playing_update(self):
        self.player.update()
        self.player.change_state()
    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit (self.background,(TOP_BOTTOM_BUFFER//2, TOP_BOTTOM_BUFFER//2))
        self.darw_grid()
        # self.draw_wall()
        self.draw_text("CURRENT SCORE: {}".format(0),self.screen, [50, 5], 18, WHITE , START_FONT)
        self.draw_text("HIGH SCORE: {}".format(0),self.screen, [WIDTH//2, 5], 18, WHITE , START_FONT)
        self.player.draw()
        pygame.display.update()