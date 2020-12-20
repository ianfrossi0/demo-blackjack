import pygame
import os
import tkinter

root = tkinter.Tk()

SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
CARD_WIDTH = 167.5
CARD_HEIGHT = 243
ACTION_COOLDOWN = 500  # 0.5s
SCALE = (SCREEN_WIDTH * 0.035, SCREEN_HEIGHT * 0.035)  # Will have to check if the float value is okay
CARD_SCREEN_CENTER_X = ((SCREEN_WIDTH - (CARD_WIDTH * SCALE[0] // 100)) / 2)
CARD_SCREEN_CENTER_Y = ((SCREEN_HEIGHT - (CARD_HEIGHT * SCALE[1] // 100)) / 2)

IMG_PATH = os.path.join("img")
DECK = pygame.image.load(os.path.join(IMG_PATH, "deck.png"))
TABLE = pygame.image.load(os.path.join(IMG_PATH, "table.png"))

ICONS = ["Hearts", "Tiles", "Clovers", "Pikes"]
