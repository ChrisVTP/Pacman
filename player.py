import pygame
import time
from pygame.constants import HAT_CENTERED
from pygame.sprite import DirtySprite
from setting import *
vec = pygame.math.Vector2

class Player():
    def __init__(self, app ,pos) -> None:
        self.app = app
        self.grid_pos = pos
        self.Pclose = pygame.image.load(PACMAN_CLOSE)
        self.Pclose = pygame.transform.scale(self.Pclose, PACMAN_SCALE)
        self.Popen = pygame.image.load(PACMAN_OPEN)
        self.Popen = pygame.transform.scale(self.Popen, PACMAN_SCALE)
        self.pix_pos = self.get_pix_pos() 
        self.direction = vec(1, 0)
        self.new_direction = vec(1, 0)
        self.just_move = True
        self.close = True
        self.state_close = time.time()
        self.speed = 2
        self.eatSoundTime = time.time()
        # self.stop = False

    def draw(self): # draw the player in map
        pacman = vec(self.pix_pos.x - self.app.cell_w//2 , self.pix_pos.y-self.app.cell_h//2)
        if self.close == True:
            self.app.screen.blit(self.Pclose, pacman)
            pygame.draw.circle(self.app.screen, RED, pacman,2)
        else: 
            self.app.screen.blit(self.Popen, pacman)
            pygame.draw.circle(self.app.screen, RED, pacman,2)


    def get_pix_pos(self): # get the pixel position of player
        return vec((self.grid_pos[0]*self.app.cell_w + 0.5*self.app.cell_w)+TOP_BOTTOM_BUFFER//2,
                   (self.grid_pos[1]*self.app.cell_h + 0.5*self.app.cell_h)+TOP_BOTTOM_BUFFER//2)



    def change_state(self): # player has 2 start and continually changes
        if (time.time() - self.state_close) >= 0.2:
            self.close = not self.close
            self.state_close = time.time()

    def can_turn(self): # check if player can turn yet
        
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_w == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_h == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def update(self): # update player after all event called
        if(self.just_move):
            self.pix_pos += self.direction * self.speed
        if(self.can_turn()):
            self.just_move = self.can_move(self.new_direction)
            old_direction = self.direction
            if (self.just_move):
                if self.direction.x == self.new_direction.y  and self.direction.y == self.new_direction.x*-1:
                    self.moveRight()
                elif self.direction.x == self.new_direction.y*-1  and self.direction.y == self.new_direction.x:
                    self.moveLeft()
                elif self.direction + self.new_direction == vec(0,0):
                    self.moveBack()
                self.direction = self.new_direction
            elif self.can_move(old_direction):
                self.direction = old_direction
                self.just_move = True
            
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER + self.app.cell_w//2)//self.app.cell_w+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER + self.app.cell_h//2)//self.app.cell_h+1
        self.app.score += self.inCoin()
        pass
    def moveRight(self): # rotate the player to the right
        self.Pclose = pygame.transform.rotate(self.Pclose, -90)
        self.Popen = pygame.transform.rotate(self.Popen, -90)

    def moveLeft(self):# rotate the player to the left
        self.Pclose = pygame.transform.rotate(self.Pclose, 90)
        self.Popen = pygame.transform.rotate(self.Popen, 90)

    def moveBack(self): # rotate the player to the back
        self.Pclose = pygame.transform.rotate(self.Pclose, 180)
        self.Popen = pygame.transform.rotate(self.Popen,180)

    def can_move(self, direction): # check if a wall a head or not
        for i in self.app.wall:
            if vec(self.grid_pos + direction) == i:
                return False
        return True

    def move(self, direction): # change the new direction
        self.new_direction = direction
            
    def inCoin(self): # handle when the player eat coin
        coin_index = -1
        for i in range(len(self.app.points)):
            if self.app.points[i] == self.grid_pos:
                coin_index = i
                if time.time() -  self.eatSoundTime >=1:
                    self.app.play_sound("pacman_chomp.wav")
                    self.eatSoundTime = time.time()
                break
        if coin_index>=0:
            coin = self.app.points.pop(coin_index)
            if (coin in self.app.Bpoints):
                return 50
            return 10
        return 0



