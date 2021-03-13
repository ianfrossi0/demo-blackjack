import pygame
import os
import tkinter
import pyautogui

#root = tkinter.Tk()
#get_curr_screen_geometry()
#root.withdraw()


#window = pyautogui.getWindow(0)

# Graphic relevant constants
SCREEN_WIDTH = pyautogui.size()[0]
SCREEN_HEIGHT = pyautogui.size()[1]
IMG_PATH = os.path.join("img")
CARD_WIDTH = 167.5
CARD_HEIGHT = 243
SCALE = (SCREEN_WIDTH * 0.035, SCREEN_HEIGHT * 0.035)  # Will have to check if the float value is okay

# NOTE: Using (SCREEN_WIDTH/HEIGHT - IMG_SIZE) / 2 as X
# or Y position will perfectly center the surface on the screen
CARD_SCREEN_CENTER_X = ((SCREEN_WIDTH - (CARD_WIDTH * SCALE[0] // 100)) / 2)
CARD_SCREEN_CENTER_Y = ((SCREEN_HEIGHT - (CARD_HEIGHT * SCALE[1] // 100)) / 2)
BAHNSCHRIFT = 'Bahnschrift SemiLight'
FONT_SIZE_BIG = int(SCALE[0])
FONT_SIZE_MID = int(SCALE[0]-0.25*SCALE[0])
FONT_SIZE_SMALL = int(SCALE[0]-0.5*SCALE[0])

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (34, 34, 34)
DARK_RED = (103, 0, 0)
DARK_LIME = (125, 163, 67)
WHITE = (255, 255, 255)

# Game relevant constants
ACTION_COOLDOWN = 500  # 0.5s
ENTRY_BET = 200
MOVEMENT_KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                 pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE]
FPS = 60
DECK = pygame.image.load(os.path.join(IMG_PATH, "deck.png"))
TABLE = pygame.image.load(os.path.join(IMG_PATH, "table.png"))
ICONS = ["Hearts", "Tiles", "Clovers", "Pikes"]

# Print relevant constants
HORIZONTAL_LINE = "\n___________________________________________________________________________________\n"


