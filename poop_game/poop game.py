import random
import pygame
#############################################
#   Must have
pygame.init() # reset 

#   initialize the window
screen_width = 640 # x-axis
screen_height = 480 # y-axis
screen = pygame.display.set_mode((screen_width, screen_height))

#   Title 
pygame.display.set_caption("Poop escape")
pygame.image
#   FPS
clock = pygame.time.Clock()

#############################################

# 1. Background, Game image, Character, Position of image, Font
#   Background

background = pygame.image.load("/Users/jaewoocho/Desktop/Code/demoGame/images/background1.jpg")

character = pygame.image.load("/Users/jaewoocho/Desktop/Code/demoGame/images/character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

to_x_LEFT = 0
to_x_RIGHT = 0
character_speed = 10

poop = pygame.image.load("/Users/jaewoocho/Desktop/Code/demoGame/images/poop.png")
poop_size = poop.get_rect().size
poop_width = poop_size[0]
poop_height = poop_size[1]
poop_x_pos = random.randint(0, screen_width - poop_width)
poop_y_pos = 0
poop_speed = 10


#   event loop
running = True 
while running:
    dt = clock.tick(30) #frame per second

    # 2. Event handling (keyboard, mouse, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # when user click the close button
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x_RIGHT += character_speed
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: 
                to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                to_x_RIGHT = 0

    # 3. Character location
    character_x_pos += to_x_LEFT + to_x_RIGHT

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = screen_width - character_width

    poop_y_pos += poop_speed

    if poop_y_pos > screen_height:
        poop_x_pos = random.randint(0, screen_width - poop_width)
        poop_y_pos = 0
    # 4. Collision handling
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    poop_rect = poop.get_rect()
    poop_rect.left = poop_x_pos
    poop_rect.top = poop_y_pos

    if character_rect.colliderect(poop_rect):
        print("Game over")
        running = False

    
    # 5. Display it in window
    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    screen.blit(poop, (poop_x_pos, poop_y_pos))

    pygame.display.update()

pygame.time.delay(1500)

pygame.quit()