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
pygame.display.set_caption("Pang game")

#   FPS
clock = pygame.time.Clock()

#############################################

# 1. Background, Game image, Character, Position of image, Font
current_path = os.path.dirname(__file__)    # current file path
image_path = os.path.join(current_path, "images")

#   Background, Character, 
background = pygame.image.load(os.path.join(image_path, "background.png"))

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height

to_x_LEFT = 0
to_x_RIGHT = 0

character_speed = 5

#   weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 5

#   ball (we have 4 different ball size images)
ball_images = [
    pygame.image.load(os.path.join(image_path, "enemy1.png")),
    pygame.image.load(os.path.join(image_path, "enemy2.png")),
    pygame.image.load(os.path.join(image_path, "enemy3.png")),
    pygame.image.load(os.path.join(image_path, "enemy4.png"))]

#   default ball_speed for different size
ball_speed_y = [-18, -15, -12, -9]

balls = []

#   first ball
balls.append({
    "pos_x" : 50,
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3,
    "to_y" : -6,
    "init_speed_y" : ball_speed_y[0]})

weapon_to_remove = -1
ball_to_remove = -1


#   event loop
running = True 
while running:
    dt = clock.tick(60) #frame per second

    # 2. Event handling (keyboard, mouse, etc)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # when user click the close button
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                to_x_LEFT -= character_speed
                character = pygame.image.load(os.path.join(image_path, "character2.png"))
            elif event.key == pygame.K_RIGHT:
                to_x_RIGHT += character_speed
                character = pygame.image.load(os.path.join(image_path, "character.png"))
            elif event.key == pygame.K_SPACE:
                character = pygame.image.load(os.path.join(image_path, "character3.png"))
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
                
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

    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] 

    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    #   ball position
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
        
        if ball_pos_y >= screen_height - ball_height:
            ball_val["to_y"] = ball_val["init_speed_y"]
        else:
            ball_val["to_y"] += 0.5
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
    # 4. Collision handling
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    #   ball colliding with character
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        if character_rect.colliderect(ball_rect):
            running = False
            break

    #   weapon colliding with ball
    for weapon_idx, weapon_val in enumerate(weapons):
        weapon_x_pos = weapon_val[0]
        weapon_y_pos = weapon_val[1]

        weapon_rect = weapon.get_rect()
        weapon_rect.left = weapon_x_pos 
        weapon_rect.top = weapon_y_pos

        if weapon_rect.colliderect(ball_rect):
            weapon_to_remove = weapon_idx
            ball_to_remove = ball_idx
            break
    
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    
    
    
    # 5. Display it in window
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))


    screen.blit(character, (character_x_pos, character_y_pos))
    
    

    pygame.display.update()

pygame.time.delay(1500)

pygame.quit()