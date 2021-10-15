import pygame
import random
import time
from pygame import transform

from pygame.constants import SHOWN, VIDEOEXPOSE
from setting import *

vec = pygame.math.Vector2

class Ghost:
    def __init__ (self, app, pos, ghost_character):
        self.app = app
        self.id = ghost_character["id"]
        self.character = ghost_character["Character"]
        self.first_pic = pygame.image.load(ghost_character["firstPic"])
        self.first_pic = pygame.transform.scale(self.first_pic, GHOST_SCALE)
        self.second_pic = pygame.image.load(ghost_character["secondPic"])
        self.second_pic = pygame.transform.scale(self.second_pic, GHOST_SCALE)
        self.grid_pos = pos
        self.pix_pos = self.get_pix_pos()
        self.change_pic = True
        self.time_change = time.time()
        self.direction = vec(0, 0)
        self.new_direction = vec(0, 0)
        self.speed = self.set_speed()

    def set_speed(self):
        if self.character in ["Scared", "Speedy"]:
            return 2
        return 1

    def change_state(self):
        if time.time() - self.time_change >= 0.2 :
            self.change_pic = not self.change_pic
            self.time_change = time.time()
        
    def draw (self):
        ghost = vec(self.pix_pos.x - self.app.cell_w//2 , self.pix_pos.y-self.app.cell_h//2)
        if self.change_pic:
            self.app.screen.blit(self.first_pic, ghost)
        else:
            self.app.screen.blit(self.second_pic, ghost)

    def update(self):
        self.target = self.find_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction *self.speed
            if self.time_to_move():
                self.move()
        
        self.grid_pos[0] = (self.pix_pos[0]-TOP_BOTTOM_BUFFER + self.app.cell_w//2)//self.app.cell_w+1
        self.grid_pos[1] = (self.pix_pos[1]-TOP_BOTTOM_BUFFER + self.app.cell_h//2)//self.app.cell_h+1

    def time_to_move(self):
        if int(self.pix_pos.x+TOP_BOTTOM_BUFFER//2) % self.app.cell_w == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pix_pos.y+TOP_BOTTOM_BUFFER//2) % self.app.cell_h == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False
    
    def move(self):
        if self.character == "Random":
            self.direction = self.get_random_direction()
        elif self.character == "Slow":
            self.direction = self.get_path_direction(self.target)
        elif self.character == "Speedy":
            self.direction = self.get_path_direction(self.target)
        elif self.character == "Scared":
            self.direction = self.get_path_direction(self.target)


    def get_pix_pos(self):
        return vec((self.grid_pos[0]*self.app.cell_w + 0.5*self.app.cell_w)+TOP_BOTTOM_BUFFER//2,
                   (self.grid_pos[1]*self.app.cell_h + 0.5*self.app.cell_h)+TOP_BOTTOM_BUFFER//2)

    def find_target(self): # defind the targer as character of the ghost
        if self.character in ["Speedy","Slow"]:
            return self.app.player.grid_pos
        else:
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(1, 1)
            if self.app.player.grid_pos[0] > COLS//2 and self.app.player.grid_pos[1] < ROWS//2:
                return vec(1, ROWS-2)
            if self.app.player.grid_pos[0] < COLS//2 and self.app.player.grid_pos[1] > ROWS//2:
                return vec(COLS-2, 1)
            else:
                return vec(COLS-2, ROWS-2)

    def get_random_direction(self): # move randomly
        while True:
            number = random.randint(-2, 1)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.wall:
                break

        return vec(x_dir, y_dir)

    def get_path_direction(self, target): # use AI to find target
        neighbor_grid = self.find_next_neighbor(self.grid_pos, target)
        x = neighbor_grid[0] - self.grid_pos[0]
        y = neighbor_grid[1] - self.grid_pos[1]
        return vec(x,y)

    def find_next_neighbor(self, start,target): # the algorithms to find the target
        start = [int(start[0]) , int(start[1])]
        target = [int(target[0]) , int(target[1])]
        grid = [[0 for x in range(COLS)] for x in range(ROWS)]# making a grid
        for cell in self.app.wall:
            if cell.x < 28 and cell.y < 30:
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        used = []
        while queue:
            current = queue.pop(0)
            used.append(current)
            if current == target:
                break
            else:
                neighbours = [[0,-1] , [1,0], [0,1], [-1,0]]
                for neigh in neighbours:
                    if neigh[0] + current [0] >= 0 and neigh[0] + current [0] < len(grid[0]):
                        if neigh[1] + current [1] >= 0 and neigh[1] + current [1] < len(grid):
                            next_cell = [int(neigh[0] + current [0]), int(neigh[1] + current [1])]
                            if next_cell not in used:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    path.append({"valueNode": current, "nextNode": next_cell})
            
        shortest = [target]
        while target != start:
            for step in path:
                if step["nextNode"] == target:
                    target = step["valueNode"]
                    shortest.insert(0, step["valueNode"])

        # print(result)
        return shortest[1] 

