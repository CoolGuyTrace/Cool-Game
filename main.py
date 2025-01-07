# import the pygame module 
import pygame
import sys
import os

pygame.init()

#Constants
WIDTH = 1080
HEIGHT = 720
FPS = 60
clock = pygame.time.Clock()

class Window:
    #Create the game window
    background_colour = (24, 0, 77) 
    window = pygame.display.set_mode((WIDTH, HEIGHT)) 
    pygame.display.set_caption('Game') 
    window.fill(background_colour)
class Ground:
    #Create the game terrain
    color = (0,0,0)
    x = 0
    y = 650
    size = pygame.Rect(x, y, 1080, 100)
    ground = pygame.draw.rect(Window.window, color, size)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/lil_dude.png")
        self.rect = self.image.get_rect()
#Create the playable character
player = Player()
player.rect.x = 0
player.rect.y = 0
player_list = pygame.sprite.Group()
player_list.add(player)

#The game loop
running = True
while running:
    player_list.draw(Window.window)
    clock.tick(FPS)
    pygame.display.flip()
    for event in pygame.event.get(): 
      
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            running = False