from tetris import *
import pygame

if __name__ == "__main__":
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')
    main_menu(win)