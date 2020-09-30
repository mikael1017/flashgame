import random
import os
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
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

start_ticks = pygame.time.get_ticks()
timer = pygame.time.get_ticks()

background = pygame.image.load(os.path.join(image_path, "background.png"))
character = pygame.image.load(os.path.join(image_path, "character.png"))
poop = pygame.image.load(os.path.join(image_path, "poop.png"))

poops = []

character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

to_x_LEFT = 0
to_x_RIGHT = 0
character_speed = 10

poop_size = poop.get_rect().size
poop_width = poop_size[0]
poop_height = poop_size[1]
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

    elapsed_time = pygame.time.get_ticks()
    # #   add poop every 30ms 
    # print ("elapsed time " , elapsed_time)
    # print("timer " , timer)
    if elapsed_time - timer > 20:
            random_num = random.randint(0, 1)
            if random_num == 1:
                poops.append({
                    "poop_width" : poop_width,
                    "poop_height" : poop_height,
                    "poop_x_pos" : random.randint(0, screen_width - poop_width),
                    "poop_y_pos" : -50,
                    "poop_speed" : poop_speed})
            timer = elapsed_time


    for poop_idx, poop_val in enumerate(poops):
        poop_val["poop_y_pos"] += poop_speed
        poop_x_pos = poop_val["poop_x_pos"]
        poop_y_pos = poop_val["poop_y_pos"]
        if poop_y_pos >= screen_height:
            del poops[poop_idx]


        #   By a random possibility, make poop at random place every second 
        
    # print(len(poops))

    # 4. Collision handling
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for poop_idx, poop_val in enumerate(poops):
        poop_rect = poop.get_rect()
        poop_x_pos = poop_val["poop_x_pos"]
        poop_y_pos = poop_val["poop_y_pos"]
        poop_rect.left = poop_x_pos
        poop_rect.top = poop_y_pos

        if poop_rect.colliderect(character_rect):
            running = False
            

    
    # 5. Display it in window
    screen.blit(background, (0,0))
    screen.blit(character, (character_x_pos, character_y_pos))

    for idx, val in enumerate(poops):
        poop_x_pos = val["poop_x_pos"]
        poop_y_pos = val["poop_y_pos"]
        screen.blit(poop, (poop_x_pos, poop_y_pos))

    pygame.display.update()

pygame.time.delay(1500)

pygame.quit()