# Get ready for the world's worst code :sunglasses:

# import the pygame module 
import pygame
import random
# Why are these two here?? I forget
import sys
import os

pygame.init()
pygame.font.init()
system_font = pygame.font.Font("fonts/system-bold.ttf", 50)

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

class Keys:
    left = pygame.K_LEFT
    right = pygame.K_RIGHT
    up = pygame.K_UP
    down = pygame.K_DOWN

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/lil_dude.png")
        self.rect = self.image.get_rect()
        self.velocity_y = 0  
        self.gravity = 0.5
        self.isJumping = False
        self.isGrounded = False
    
    def moveRight(self, pixels):
        if self.rect.x + pixels <= WIDTH - self.rect.width: 
            self.rect.x += pixels
    
    def moveLeft(self, pixels):
        if self.rect.x - pixels >= 0: 
            self.rect.x -= pixels

    def jump(self, velocity):
        if self.isGrounded:
            if not self.isJumping:  
                self.isJumping = True
                self.isGrounded = False  
                self.velocity_y = velocity

    def update(self):  
        # Manage jumping and falling  
        if self.isJumping:  
            self.rect.y += self.velocity_y  
            self.velocity_y += self.gravity
            #It's supposed to stop you from being able to jump while under the platform, but I'm stupid so I'm leaving it how it is
            if self.rect.y >= left_plat_pos[1] and self.rect.x <= left_plat_pos[2]:
                self.isJumping = False
            
            if self.rect.y >= right_plat_pos[1] and self.rect.x >= right_plat_pos[0]:
                self.isJumping = False

            if self.velocity_y > 0:  
                self.isJumping = False

    def moveDown(self, pixels):
        if self.rect.y + pixels <= (ground_pos[1]+10) - self.rect.height:
            self.rect.y += pixels

    # Gravity Gaming :D
    # No shot this works (It did?!?1?)
    def apply_newtons_law(self):  
        self.velocity_y += self.gravity  
        self.rect.y += self.velocity_y  

        # Check if the player is on the floor  
        if self.rect.y > ground_pos[1] - self.rect.height:  
            self.rect.y = ground_pos[1] - self.rect.height  
            self.velocity_y = 0
            self.isGrounded = True

        # Check if the player is on the platform  
        if self.rect.colliderect(left_plat_pos) and self.velocity_y >= 0:  
            self.rect.y = left_plat_pos[1] - self.rect.height  
            self.velocity_y = 0
            self.isGrounded = True

        if self.rect.colliderect(right_plat_pos) and self.velocity_y >= 0:  
            self.rect.y = right_plat_pos[1] - self.rect.height  
            self.velocity_y = 0
            self.isGrounded = True

class Objects():
    def drawCircle(color, center, radius):
        pygame.draw.circle(Window.window, color, center, radius)
    def drawRect(rcolor, rval):
        pygame.draw.rect(Window.window, rcolor, rval)
    def spawn_coin(radius):  
        x = random.randint(0, WIDTH - radius * 2)  
        y = random.randint(0, HEIGHT-100 - radius * 2)  
        return (x, y)

#Create the playable character
player = Player()
player_list = pygame.sprite.Group()
player_list.add(player)
  
coin_radius = 20
coin_pos = Objects.spawn_coin(coin_radius)  
coin_visible = True
score = 0

#x,y,width,height
ground_pos = (0,HEIGHT-100,WIDTH,100)
left_plat_pos = (0, CENTER[1]+40, 200, 20)
right_plat_pos = (880, CENTER[1]+40, 200, 20)

#The game loop
running = True
while running:
    for event in pygame.event.get(): 
        # Check for QUIT event       
        if event.type == pygame.QUIT:  
            running = False
    Player.update(player)
    Player.apply_newtons_law(player)

    pressed = pygame.key.get_pressed()
    if pressed[Keys.left]:
        player.moveLeft(10)   
    if pressed[Keys.right]:
       player.moveRight(10)
    if pressed[Keys.down]: #TODO: Crouch
        player.moveDown(10)
    if pressed[Keys.up]: 
        player.jump(-15)

    Window.window.fill(Window.background_colour)
    player_list.update()
    player_list.draw(Window.window)

    #Make a circle for the player to grab
    if coin_visible:
        circle = Objects.drawCircle((255, 215, 0), coin_pos, coin_radius)
        if player.rect.collidepoint(coin_pos):
            score += 100
            coin_pos = Objects.spawn_coin(coin_radius)
            circle = Objects.drawCircle((255, 215, 0), coin_pos, coin_radius)
    count_text = system_font.render(f'Score: {score}', True, (255, 255, 255))
    Window.window.blit(count_text, (10, 10))

    floor = Objects.drawRect((0,0,0), ground_pos)
    left_plat = Objects.drawRect((0,0,0), left_plat_pos)
    right_plat = Objects.drawRect((0,0,0), right_plat_pos)

    clock.tick(FPS)
    pygame.display.update()