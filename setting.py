from pygame.math import Vector2 as vec
#screen setting

#game width
WIDTH, HEIGHT = 610, 670
SCREEN_WIDTH = WIDTH + 100
FPS = 60
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH- TOP_BOTTOM_BUFFER, HEIGHT- TOP_BOTTOM_BUFFER

ROWS = 30
COLS = 28
#color
BLACK = (0,0,0)
RED = (255, 0, 0)
GREY = (110, 110, 104)
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (0,0,139)
PINK = (255,188,217)
CYAN = (0,255,255)
ORANGE = (255,165,0)


#font
START_TEXT_SIZE = 26
START_FONT = 'Bauhaus 93'

#image
START_ICON = "pacmanLogo.png"
#player setting
PLAYER_START_POSITION = vec(14,29)
PACMAN_OPEN = "PacmanOpen.png"
PACMAN_CLOSE = "PacmanClose.png"
PACMAN_SCALE= ((HEIGHT//ROWS) - 3, (WIDTH//COLS-3))

#ghost setting
GHOST_SCALE = ((HEIGHT//ROWS) - 3, (WIDTH//COLS-3))



# The year and course code
COURSE_YEAR = "2021"
# Students:
STUDENT_SIZE = 20
STUDENT_FRONT = "Cooper Std"
STUDENTS = [("PHUC THIEN VUONG", "S5193954","2805ICT"),
("ANH TRUONG NGUYEN", "S5168384","2805ICT"),
("HIEN DAT CHU", "S5223891","3815ICT")
]

#Button setting
BUTTON_W = 150
BUTTON_H = 80

BUTTON_WORD_SIZE = 30
BUTTON_WORD_FONT = "Bauhaus 93"

#sound setting
INTRO_SOUND ="pacman_beginning.wav"
INTRO_SOUND_LENGTH = 4 #4 seconds

#ghost character
BLINKY = {
    "id" : 2,
    "colour": RED,
    "Character": "Scared",
    "firstPic": "BLINKY1.png",
    "secondPic" :"BLINKY2.png"
}
PINKY = {
    "id" : 3,
    "colour": PINK,
    "Character": "Speedy",
    "firstPic": "PINKY1.png",
    "secondPic" :"PINKY2.png"
}
INKY = {
    "id" : 4,
    "colour": CYAN,
    "Character": "Random",
    "firstPic": "INKY1.png",
    "secondPic" :"INKY2.png"
}
CLYDE = {
    "id" : 5,
    "colour": ORANGE,
    "Character": "Slow",
    "firstPic": "CLYDE1.png",
    "secondPic" :"CLYDE2.png"
}