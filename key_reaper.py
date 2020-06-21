""" Ben Chin

Key Reaper

2/11/20
"""

import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (125, 125, 125)
RED = (255, 0 , 0)

SCORE = 0
SOULS = []

SPAWN_RATE = 30
SOUL_SIZE = 20

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
STILL = 'still'

START = 'start'
GAME_OVER = 'gameover'
PLAYING = 'playing'
STATE = START


GENERATE = pygame.USEREVENT + 1
TIMER = pygame.USEREVENT + 2

up_pressed = False
left_pressed = False
right_pressed = False
down_pressed = False

BOARD = []
TIME_LEFT = 60

reaperx = WINDOW_WIDTH / 2 - 32
reapery = WINDOW_HEIGHT / 2 - 32
REAPER = pygame.Rect(reaperx, reapery, 32, 32)
   
def main():
    global SCREEN, STATE, SCORE, SOULS, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Key Reaper')

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()


def terminate():
    pygame.quit()
    sys.exit()


def show_start_screen():
    title_font = pygame.font.Font('freesansbold.ttf', 100)
    title_surf = title_font.render('Key Reaper', True, WHITE)
    title_rect = title_surf.get_rect()
    title_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    SCREEN.blit(title_surf, title_rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                SCREEN.fill(BLACK)
                return


def run_game():
    global up_pressed, left_pressed, down_pressed, right_pressed
    global SCREEN, STATE, FPSCLOCK, BOARD, TIME_LEFT , REAPER, reaperx, reapery

    pygame.time.set_timer(GENERATE, int(SPAWN_RATE / FPS * 1000))
    pygame.time.set_timer(TIMER, 1000)
   
    key_pressed = False
    direction = STILL # Dummy value
    curent_direction = direction
    while True: # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == GENERATE:
                if STATE == PLAYING:
                    BOARD += generate_souls(1)
            if event.type == TIMER:
                if STATE == PLAYING:
                    TIME_LEFT -= 1
            elif event.type == KEYDOWN:
                key_pressed = True
                if event.key == K_LEFT:
                    left_pressed = True
                elif event.key == K_RIGHT:
                    right_pressed = True
                elif event.key == K_UP:
                    up_pressed = True
                elif event.key == K_DOWN:
                    down_pressed = True
   
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    left_pressed = False
                elif event.key == K_RIGHT:
                    right_pressed = False
                elif event.key == K_UP:
                    up_pressed = False
                elif event.key == K_DOWN:
                    down_pressed = False
               
       
        if STATE == START:
            if key_pressed: # Press Key to Start
                STATE = PLAYING
                BOARD = generate_souls(10)
   
        elif STATE == PLAYING:
            SCREEN.fill(BLACK)

            if TIME_LEFT == 0:
                return # Game Over
            if up_pressed:
                    reapery -= 3
             
            if down_pressed:
                    reapery += 3
       
            if right_pressed:
                    reaperx += 3
         
            if left_pressed:
                    reaperx -=3

            REAPER.topleft= (reaperx, reapery)    
            for i in range(len(BOARD) - 1, -1, -1):
               
                if BOARD[i].colliderect(REAPER) == True:
                    BOARD.remove(BOARD[i])
                    print("REMOVED")
   
         
        pygame.draw.rect(SCREEN, RED, (reaperx, reapery, 32, 32))
        for soul_rect in BOARD:
            pygame.draw.rect(SCREEN, WHITE, soul_rect)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generate_souls(num):
    result = []

    for i in range(num):
        while True:
            left = random.randint(0, WINDOW_WIDTH - SOUL_SIZE)
            top = random.randint(20, WINDOW_HEIGHT - SOUL_SIZE)
            new_soul = pygame.Rect(left, top, SOUL_SIZE, SOUL_SIZE)
            if new_soul.collidelist(BOARD) == -1 and \
                    new_soul.collidelist(result) == -1 and \
                    new_soul.colliderect(REAPER) == False:  # If no collisions
                result.append(new_soul)
                break
    return result


 

if __name__ == '__main__':
    main()