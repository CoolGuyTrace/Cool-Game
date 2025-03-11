# Get ready for the world's worst code :sunglasses:

# import the pygame module 
import pygame
# Why are these two here?? I forget
import sys
import os

pygame.init()
pygame.font.init()
system_font = pygame.font.Font("fonts/system-bold.ttf", 70)

#Constants
WIDTH = 1080
HEIGHT = 720
CENTER = (WIDTH/2, HEIGHT/2)
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
        self.velocity_y = 0  
        self.gravity = 0.5
    
    def moveRight(self, pixels):
        if self.rect.x + pixels <= WIDTH - self.rect.width: 
            self.rect.x += pixels
    
    def moveLeft(self, pixels):
        if self.rect.x - pixels >= 0: 
            self.rect.x -= pixels

    def jump(self, pixels):
        if self.rect.y + pixels >= 0:
            self.rect.y -= pixels

    def moveDown(self, pixels):
        if self.rect.y + pixels <= (ground_pos[1]+10) - self.rect.height:
            self.rect.y += pixels

    # Gravity Gaming :D
    # No shot this works
    def apply_newtons_law(self):  
        self.velocity_y += self.gravity  
        self.rect.y += self.velocity_y  

        # Check if the player is on the floor  
        if self.rect.y > ground_pos[1] - self.rect.height:  
            self.rect.y = ground_pos[1] - self.rect.height  
            self.velocity_y = 0

class Objects():
    def drawCircle(color, center, radius):
        pygame.draw.circle(Window.window, color, center, radius)
    def drawRect(rcolor, rval):
        pygame.draw.rect(Window.window, rcolor, rval)

#Create the playable character
player = Player()
player_list = pygame.sprite.Group()
player_list.add(player)

coin_pos = CENTER  
coin_radius = 20  
coin_visible = True
coin_count = 0

ground_pos = (0,HEIGHT-100,WIDTH,100)

  

#The game loop
running = True
while running:
    for event in pygame.event.get(): 
      
        # Check for QUIT event       
        if event.type == pygame.QUIT:  
            running = False
    
    Player.apply_newtons_law(player)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.moveLeft(10)   
    if keys[pygame.K_RIGHT]:
       player.moveRight(10)
    if keys[pygame.K_DOWN]: #TODO: Crouch
        player.moveDown(10)
    if keys[pygame.K_UP]: 
        player.jump(10)

    Window.window.fill(Window.background_colour)
    player_list.update()
    player_list.draw(Window.window)  
    #Make a circle for the player to grab
    if coin_visible:
        circle = Objects.drawCircle((255, 215, 0), coin_pos, coin_radius)
        if player.rect.collidepoint(coin_pos):  
            coin_visible = False  
            print("Coin collected!")
            coin_count += 1
    count_text = system_font.render(f'Coins: {coin_count}', True, (255, 255, 255))
    Window.window.blit(count_text, (10, 10))
    floor = Objects.drawRect((0,0,0), ground_pos)
    clock.tick(FPS)
    pygame.display.update()