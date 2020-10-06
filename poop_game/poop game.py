import random
import os
import pygame, time
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
#   FPpS
clock = pygame.time.Clock()

game_font = pygame.font.Font(None, 40)
pause = False
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")
#############################################

def paused():
    global pause
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf = game_font.render("Paused", True, (255, 0, 0))
    TextRect = TextSurf.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
    draw_screenRect(TextSurf, TextRect)
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            #   when user unpause the game with pressing p
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                    break

        pygame.display.update()
        
class Poop(object):
    def __init__(self, width, height, x_pos, y_pos):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.speed = 10

    def set_x(self, x):
        self.x_pos = x

    def set_y(self, y):
        self.y_pos = y

    def get_x(self):
        return int(self.x_pos)

    def get_y(self):
        return int(self.y_pos)
    
    def get_speed(self):
        return int(self.speed)

def draw_screen(image, x, y):
    screen.blit(image, (x, y))

def draw_screenRect(image, rect):
    screen.blit(image, rect)

def game_loop():
    global pause
    # 1. Background, Game image, Character, Position of image, Font
    #   Background

    start_ticks = pygame.time.get_ticks()
    timer = pygame.time.get_ticks()

    background = pygame.image.load(os.path.join(image_path, "background.png"))
    character = pygame.image.load(os.path.join(image_path, "dog.png"))
    poop_image = pygame.image.load(os.path.join(image_path, "poop.png"))

    poops = []

    character_size = character.get_rect().size
    character_width = character_size[0]
    character_height = character_size[1]
    character_x_pos = (screen_width / 2) - (character_width / 2)
    character_y_pos = screen_height - character_height

    to_x_LEFT = 0
    to_x_RIGHT = 0
    character_speed = 8

    poop_size = poop_image.get_rect().size
    poop_width = poop_size[0]
    poop_height = poop_size[1]
    poop_speed = 10
    dodged_poop = 0

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
                    character = pygame.image.load(os.path.join(image_path, "dog_left.png"))
                elif event.key == pygame.K_RIGHT:
                    to_x_RIGHT += character_speed
                    character = pygame.image.load(os.path.join(image_path, "dog_right.png"))
                elif event.key == pygame.K_p:
                        pause = True
                        paused()
            
            if event.type == pygame.KEYUP:
                character = pygame.image.load(os.path.join(image_path, "dog.png"))
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
        if elapsed_time - timer > 10:
                random_num = random.randint(0, 2)
                if random_num == 1:
                    poo = Poop(poop_width, poop_height, random.randint(0, screen_width - poop_width), -50)
                    poops.append(poo)
                timer = elapsed_time

        for poo_idx, poo in enumerate(poops):
            
            poo.set_y(poo.y_pos + poo.speed)
            poo_x_pos = poo.x_pos
            poo_y_pos = poo.y_pos
            if poo_y_pos >= screen_height:
                del poops[poo_idx]
                dodged_poop += 1
            #   By a random possibility, make poop at random place every second 

        # 4. Collision handling
        character_rect = character.get_rect()
        character_rect.left = character_x_pos
        character_rect.top = character_y_pos

        for poop_idx, poo in enumerate(poops):
            poop_rect = poop_image.get_rect()
            poop_x_pos = poo.x_pos
            poop_y_pos = poo.y_pos
            poop_rect.left = poop_x_pos
            poop_rect.top = poop_y_pos

            if poop_rect.colliderect(character_rect):
                running = False
                break
                

        
        # 5. Display it in window
        draw_screen(background, 0, 0)
        draw_screen(character, character_x_pos, character_y_pos)

        for idx, poo in enumerate(poops):
            poop_x_pos = poo.x_pos
            poop_y_pos = poo.y_pos
            draw_screen(poop_image, poop_x_pos, poop_y_pos)

        score = game_font.render("Score : {}".format(dodged_poop), True, (0,0,0))
        draw_screen(score, 10, 10)
        pygame.display.update()

    msg = game_font.render("Game Over", True, (0, 0, 0))
    msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
    draw_screenRect(msg, msg_rect)
    pygame.display.update()

    pygame.time.delay(1500)

#   event loop
game_loop()
pygame.quit()
quit()
