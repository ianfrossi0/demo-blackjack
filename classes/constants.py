import pygame
import os
import tkinter

root = tkinter.Tk()

# Graphic relevant constants
SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
IMG_PATH = os.path.join("img")
CARD_WIDTH = 167.5
CARD_HEIGHT = 243
SCALE = (SCREEN_WIDTH * 0.035, SCREEN_HEIGHT * 0.035)  # Will have to check if the float value is okay
CARD_SCREEN_CENTER_X = ((SCREEN_WIDTH - (CARD_WIDTH * SCALE[0] // 100)) / 2)
CARD_SCREEN_CENTER_Y = ((SCREEN_HEIGHT - (CARD_HEIGHT * SCALE[1] // 100)) / 2)
BAHNSCHRIFT = 'Bahnschrift SemiLight'
FONT_SIZE = int(SCALE[0])

# Colors
BLACK = (0, 0, 0)
DARK_GRAY = (34, 34, 34)
DARK_RED = (103, 0, 0)
DARK_LIME = (125, 163, 67)
WHITE = (255, 255, 255)

# Game relevant constants
ACTION_COOLDOWN = 500  # 0.5s
MOVEMENT_KEYS = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN,
                 pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE]
FPS = 60
DECK = pygame.image.load(os.path.join(IMG_PATH, "deck.png"))
TABLE = pygame.image.load(os.path.join(IMG_PATH, "table.png"))
ICONS = ["Hearts", "Tiles", "Clovers", "Pikes"]

# Print relevant constants
HORIZONTAL_LINE = "\n___________________________________________________________________________________\n"
