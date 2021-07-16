import pygame
import sys
from pygame.locals import *
import math
import random
import time

pygame.init()
state = 0
turns = 0
MASTER_POS = [(0, 0), (1, 0), (2, 0), (3, 0),
              (0, 1), (1, 1), (2, 1), (3, 1),
              (0, 2), (1, 2), (2, 2), (3, 2),
              (0, 3), (1, 3), (2, 3), (3, 3)]

positions = [(0, 0), (1, 0), (2, 0), (3, 0),
             (0, 1), (1, 1), (2, 1), (3, 1),
             (0, 2), (1, 2), (2, 2), (3, 2),
             (0, 3), (1, 3), (2, 3), (3, 3)]

board = [
    [0, 0, 0, 0],  # 0,0 | 0,1 | 0,2 | 0,3
    [0, 0, 0, 0],  # 1,0 | 1,1 | 1,2 | 1,3
    [0, 0, 0, 0],  # 2,0 | 2,1 | 2,2 | 2,3
    [0, 0, 0, 0]  # 3,0 | 3,1 | 3,2 | 3,3
]
font_size = []


def max_size(val, text):
    # Returns maximum font size for displaying given text.
    font = pygame.font.SysFont("Times New Roman", val)
    while font.size(text)[0] < 100 and font.size(text)[1] < 100:
        val += 1
        font = pygame.font.SysFont("Times New Roman", val)
    return val - 1

for i in range(0, 6):
    font_size.append(max_size(1, str(pow(10, i))))

class Value(pygame.sprite.Sprite):

    def __init__(self, spot, pos, val):
        super().__init__()
        self.surf = pygame.Surface((100, 100))
        self.rect = self.surf.get_rect(center=(spot[0]+50,spot[1]+50))
        self.value = val
        self.font = pygame.font.SysFont("Times New Roman", 89)
        self.text = self.font.render((str(self.value)), True, (255, 255, 255))
        self.pos = pos  # Position in the board array

    def resize(self):
        global font_size
        key = math.log(self.value, 10)
        # Resizes the font of tiles as needed
        self.font = pygame.font.SysFont("Times New Roman", font_size[int(key)])

    def draw(self, surface):
        # draws the values onto the board
        self.resize()
        self.text = self.font.render((str(self.value)), True, (255, 255, 255))
        # Placeholder - TODO: determine size of font and change rect to reflect it
        params = self.font.size(str(self.value))
        surface.blit(self.text, self.rect)

    def __repr__(self):
        return repr(self.value)

def initial(bor, pos):
    # Places initial 2 values on board
    one = random.choice(pos)
    positions.remove(one)
    two = random.choice(pos)
    positions.remove(two)
    bor[one[0]][one[1]] = Value(((one[1] + 1) * 100, (one[0] + 1) * 100), one, 2)
    bor[two[0]][two[1]] = Value(((two[1] + 1) * 100, (two[0] + 1) * 100), two, 2)


def add(turns):
    # Used to add tiles after each turn
    global positions
    global board
    # Subject to balance changes
    key = 2
    if turns % 40 == 0:  # Occasionally adds a 4 to slightly accelerate gameplay.
        key = 4

    # TESTING VALUE, REMOVE IN FINAL
    # key = 512

    if len(positions) > 0:
        # Only adds if possible
        spot = random.choice(positions)
        board[spot[0]][spot[1]] = Value(((spot[1] + 1) * 100, (spot[0] + 1) * 100), (spot[0], spot[1]), key)
        positions.remove(spot)


def printB(bo):
    # Note: Unneeded in final build
    # Prints the board as an array to console.
    for e in bo:
        print(e)
    print()


def changes(oldB, newB):
    # Returns False if there are no changes between the two
    # True if any changes are detected
    for i in range(len(oldB)):
        for j in range(len(oldB)):
            if oldB[i][j] and newB[i][j]:
                if oldB[i][j].value != newB[i][j].value:
                    return True
            elif not oldB[i][j] and not newB[i][j]:
                pass
            else:
                return True
    return False


display = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Game")
FPS = pygame.time.Clock()
FPS.tick(60)

RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
GREEN = pygame.Color(0, 255, 0)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

# Place starting 2 items
positions = MASTER_POS.copy()
initial(board, positions)
old = []
score = 0
printB(board)
scoreF = pygame.font.SysFont("Times New Roman", 32)


def scoreDisplay(display, score):
    # Puts score on main display
    global scoreF
    scoreText = scoreF.render(("Score: " + (str(score))), True, RED)
    scoreRect = scoreText.get_rect()
    display.blit(scoreText, scoreRect)


def drawBox(display, colour):
    # Draws the "container" of the game as well as the grid
    # Big Box
    pygame.draw.rect(display, colour, pygame.Rect(100, 100, 400, 400), 1)
    # Inner grid
    # Vertical
    pygame.draw.line(display, colour, (200, 100), (200, 500))
    pygame.draw.line(display, colour, (300, 100), (300, 500))
    pygame.draw.line(display, colour, (400, 100), (400, 500))
    # Horizontal Lines
    pygame.draw.line(display, colour, (100, 200), (500, 200))
    pygame.draw.line(display, colour, (100, 300), (500, 300))
    pygame.draw.line(display, colour, (100, 400), (500, 400))


while True:
    if state == 0:
        display.fill(BLACK)
        drawBox(display, RED)
        scoreDisplay(display, score)
        for arr in board:
            for e in arr:
                if e:
                    e.draw(display)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                print(positions)
                for e in board:
                    old.append(e.copy())
                if event.key == pygame.K_UP:
                    for i in range(4):
                        for j in range(1, 4):
                            if board[j][i] != 0:
                                for k in range(j, 0, -1):
                                    if board[k - 1][i] == 0:
                                        board[k][i].rect.move_ip(0, -100)
                                        board[k - 1][i] = board[k][i]
                                        board[k][i] = 0
                                        positions.append((k, i))
                                        if (k - 1, i) in positions:
                                            positions.remove((k - 1, i))
                                    elif board[k - 1][i].value == board[k][i].value:
                                        board[k][i].rect.move_ip(0, -100)
                                        board[k - 1][i].value = board[k - 1][i].value * 2
                                        score += board[k - 1][i].value
                                        board[k][i] = 0
                                        positions.append((k, i))
                                        if (k - 1, i) in positions:
                                            positions.remove((k - 1, i))
                                        break
                elif event.key == pygame.K_DOWN:
                    for i in range(4):
                        for j in range(2, -1, -1):
                            if board[j][i] != 0:
                                for k in range(j, 3):
                                    if board[k + 1][i] == 0:
                                        board[k][i].rect.move_ip(0, 100)
                                        board[k + 1][i] = board[k][i]
                                        board[k][i] = 0
                                        positions.append((k, i))
                                        if (k + 1, i) in positions:
                                            positions.remove((k + 1, i))
                                    elif board[k + 1][i].value == board[k][i].value:
                                        board[k][i].rect.move_ip(0, 100)
                                        board[k + 1][i].value = board[k + 1][i].value * 2
                                        score += board[k + 1][i].value
                                        board[k][i] = 0
                                        positions.append((k, i))
                                        if (k + 1, i) in positions:
                                            positions.remove((k + 1, i))
                                        break
                elif event.key == pygame.K_LEFT:
                    for i in range(4):
                        for j in range(1, 4):
                            if board[i][j] != 0:
                                for k in range(j, 0, -1):
                                    if board[i][k - 1] == 0:
                                        board[i][k].rect.move_ip(-100, 0)
                                        board[i][k - 1] = board[i][k]
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k - 1) in positions:
                                            positions.remove((i, k - 1))
                                    elif board[i][k - 1].value == board[i][k].value:
                                        board[i][k].rect.move_ip(-100, 0)
                                        board[i][k - 1].value = board[i][k - 1].value * 2
                                        board[i][k] = 0
                                        score += board[i][k - 1].value
                                        positions.append((i, k))
                                        if (i, k - 1) in positions:
                                            positions.remove((i, k - 1))
                                        break
                elif event.key == pygame.K_RIGHT:
                    for i in range(4):
                        for j in range(2, -1, -1):
                            if board[i][j] != 0:
                                for k in range(j, 3):
                                    if board[i][k + 1] == 0:
                                        board[i][k].rect.move_ip(100, 0)
                                        board[i][k + 1] = board[i][k]
                                        board[i][k] = 0
                                        positions.append((i, k))
                                        if (i, k + 1) in positions:
                                            positions.remove((i, k + 1))
                                    elif board[i][k + 1].value == board[i][k].value:
                                        board[i][k].rect.move_ip(100, 0)
                                        board[i][k + 1].value = board[i][k + 1].value * 2
                                        board[i][k] = 0
                                        score += board[i][k + 1].value
                                        positions.append((i, k))
                                        if (i, k + 1) in positions:
                                            positions.remove((i, k + 1))
                                        break
                if changes(old, board):
                    turns += 1
                    add(turns)
                    print(positions)
                    printB(board)
                old = []
